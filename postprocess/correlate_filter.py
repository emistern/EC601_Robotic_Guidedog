# a correlation filter for precessing pathes over time
import numpy as np

class CorrelateFilter(object):

    def __init__(self, data_size):

        """
        This filter compute the correlate of signal over neigubouring time steps
        """
        
        self.prev_sig = np.zeros(data_size)
        self.conv_knl = np.ones(3)

    def update(self, curr_sig):

        # use a low pass filter to smooth the signal
        filt_sig = np.convolve(curr_sig, self.conv_knl)

        # compute the correlation between current and previous signal
        corr = np.correlate(filt_sig, self.prev_sig, "same")

        # update buffer
        self.prev_sig = filt_sig

        return corr

class CorrelateFilter4Channels(object):

    def __init__(self, data_size, thresh=0.8):

        """
        A four channel correlate filter for path filtering for robotic guide dog
        """

        self.f_filt = CorrelateFilter(data_size)
        self.l_filt = CorrelateFilter(data_size)
        self.r_filt = CorrelateFilter(data_size)
        self.s_filt = CorrelateFilter(data_size)

        self.return_dict = {
            "l": -1,
            "r": 1,
            "f": 0,
            "s": [],
            "w": 2
        }

        self.thresh = thresh

    def update(self, sig_dict):

        """
        update filters with 4 signals
        """
        corr_dict = {}
        corr_dict['f'] = self.f_filt.update(sig_dict['f'])
        corr_dict['l'] = self.l_filt.update(sig_dict['l'])
        corr_dict['r'] = self.r_filt.update(sig_dict['r'])
        corr_dict['s'] = self.s_filt.update(sig_dict['s'])

        # find the signal with maximum correlation value
        max_val_dict = {}
        for sym, sig in corr_dict.items():
            max_val_dict[sym] = max(sig)

        symbol = max(corr_dict.keys(), key=(lambda key: max_val_dict[key]))
        #print(corr_dict)
        if max_val_dict[symbol] > self.thresh:
            return self.return_dict[symbol]
        else:
            return self.return_dict['w']

if __name__ == "__main__":

    pass