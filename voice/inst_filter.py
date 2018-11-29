# Instruction Filter
import numpy as np
import operator

class InstructionFilter(object):

    def __init__(self, buf_size = 10, thresh = 0.5):

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
            "s": []
        }

        self.return_dict = {
            "l": -1,
            "r": 1,
            "f": 0,
            "s": [],
            "w": 2
        }
        self.l_buf = np.zeros(buf_size)
        self.r_buf = np.zeros(buf_size)
        self.f_buf = np.zeros(buf_size)
        self.s_buf = np.zeros(buf_size)

        self.buffers = {
            "l" : self.l_buf, 
            "r" : self.r_buf, 
            "f" : self.f_buf, 
            "s" : self.s_buf
        }

        self.buf_size = buf_size
        self.thresh = thresh

    def update(self, inst):

        """
        update the filter with incoming data
        """
        # step 1: remove the tail element in every buffer
        #         and insert a new data point to every buffer in front
        for name, buf in self.buffers.items():
            buf = np.delete(buf, buf.shape[0]-1)
            if (self.token_dict[name] == inst):  # if this instruction refer to this buffer
                buf = np.insert(buf, 0, 1)  # insert 1 in front
            else:
                buf = np.insert(buf, 0, 0)  # insert 0 in front
            self.buffers[name] = buf        # update 
        
        # step 2: pass current data through a low pass filter for smoothing
        filt_dict = {}  # use a dict to hold data
        for name in self.buffers.keys():
            filt_data = np.zeros(self.buf_size)
            raw_data = self.buffers[name]
            for i in range(self.buf_size):
                if i == 0:
                    filt_data[i] = (0 + raw_data[i] + raw_data[i+1]) / 3
                elif i == self.buf_size - 1:
                    filt_data[i] = (0 + raw_data[i] + raw_data[i-1]) / 3
                else:
                    filt_data[i] = (raw_data[i+1] + raw_data[i] + raw_data[i-1]) / 3
            filt_dict[name] = filt_data

        # step 3: integrate each channel
        intg_dict = {}
        for name, filt_data in filt_dict.items():
            _sum = np.sum(filt_data)
            intg_dict[name] = _sum / self.buf_size
        
        # find the dominant instruction
        max_inst = max(intg_dict.items(), key=operator.itemgetter(1))[0]
        max_val  = intg_dict[max_inst]
        # threshold the dominant instruction value and return
        if (max_val > self.thresh):
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