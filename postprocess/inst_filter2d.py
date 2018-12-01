# Instruction Filter
import numpy as np
from scipy import signal
import operator

class InstructionFilter2D(object):

    def __init__(self, num_step, thresh = 0.015):

        """
        This is a temporal filter for instruction selection
        translate a language of four words:
        {left(-1), forward(0), right(1), stop()}
        to a language of five words:
        {left(-1), forward(0), right(1), stop(), wait(2)}
        scheme:
            split the incoming data into 4 channels
            perform low pass filtering on each channel
            integrate each channel and pick the max
            thresholding the maximum value
        initialization:
            buffer for each channel(0 init)
        shorthands:
            l - left
            r - right
            f - forward
            s - stop
            w - wait
        """
        self.token_dict = {
            "l": -1,
            "r": 1,
            "f": 0,
        }

        self.return_dict = {
            "l": -1,
            "r": 1,
            "f": 0,
            "s": [],
            "w": 2
        }
        self.l_buf = np.zeros((num_step, num_step))
        self.r_buf = np.zeros((num_step, num_step))
        self.f_buf = np.zeros((num_step, num_step))
        self.s_buf = np.zeros((num_step, num_step))

        self.direc_buffers = {
            "l" : self.l_buf, 
            "r" : self.r_buf, 
            "f" : self.f_buf, 
        }

        self.thresh = thresh
        self.num_step = num_step

        self.lpf_kernel = np.array([
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]
        ])

    def update(self, sig_dict):

        """
        update the filter with incoming data
        """
        # step 1: remove the tail element in every buffer
        #         and insert a new data point to every buffer in front
        for name, buf in self.direc_buffers.items():
            sig = sig_dict[name]
            buf = np.delete(buf, buf.shape[0]-1, axis=0)
            buf = np.insert(buf, 0, sig, axis=0)  # insert 1 in front
            self.direc_buffers[name] = buf        # update 

        self.s_buf = np.delete(self.s_buf, self.s_buf.shape[0]-1, axis=0)
        self.s_buf = np.insert(self.s_buf, 0, sig_dict['s'], axis=0)

        # step 2: pass current data through a low pass filter for smoothing
        filt_dict = {}  # use a dict to hold data
        for name, sig in self.direc_buffers.items():
            filt_data = signal.convolve2d(sig, self.lpf_kernel, mode='valid')
            filt_dict[name] = filt_data

        filt_dict['s'] = signal.convolve2d(self.s_buf, self.lpf_kernel, mode='valid')
        
        # step 3: integrate each channel
        intg_dict = {}
        for name, filt_data in filt_dict.items():
            tri_mat = np.tril(filt_data)
            _sum = np.sum(np.matrix(np.multiply(tri_mat, tri_mat)))
            intg_dict[name] = _sum*2 / (self.num_step ** 2)
        
        # find the dominant instruction
        max_inst = max(intg_dict.items(), key=operator.itemgetter(1))[0]
        max_val  = intg_dict[max_inst]
        print(intg_dict)
        # threshold the dominant instruction value and return
        if (intg_dict['s'] > self.thresh*0.9):
            return self.return_dict['s']
        elif (max_val > self.thresh):
            return self.return_dict[max_inst]
        else:
            return self.return_dict['w']

if __name__ == "__main__":

    f = InstructionFilter()
    fake_data = [[], 0, 0, 0, [], [], [], [], []] 
    for datum in fake_data:
        print("--- new inst ---")
        i = f.update(datum)
        print(i)