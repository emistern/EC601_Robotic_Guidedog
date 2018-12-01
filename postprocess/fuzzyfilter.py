# A series of filter for post-processing pathes
# Yu Xiao (12/1/2018)
import numpy as np
import skfuzzy as fuzzy
from sampler import StepSampler
from inst_filter2d import InstructionFilter2D
import matplotlib.pyplot as plt

class FuzzyFilter(object):

    def __init__(self, max_dist, num_row, num_col, step_size, 
                       roi_mtr):
        """
        This is a reformation of the previous path filter and instruction filter
        The idea behind this reformation is to use the framework of fuzzy logic
        In addition this filter is supposed to include:
        1. taking multiple foot steps from a path into consideration over multiple time steps
        2. use fuzzy logic to form signals for different instructions
        This filter contains following sub-modules:
        1. a sampler which generate a series of masks to calculate value for each step
        2. a fuzzify module to translate directional value to signal for different channel
        3. 
        utils:
        1. appending stop value to non-full pathes
        """

        self.num_row = num_row
        self.num_col = num_col
        self.num_step = int(max_dist / step_size)
        sampler = StepSampler(max_dist, num_row, step_size, roi_mtr)

        self.samples = sampler.gen_sample()
        self.decay_mask = sampler.compute_decay_mask()
        self.inst_filter = InstructionFilter2D(self.num_step)

    def update(self, path, show=False):

        # step 0: append stop token to path
        norm_path = self.normalize_path(path)

        # step 1: apply masks to normalized pathes
        direc_vals = np.zeros(self.num_step)
        stop_vals = np.zeros(self.num_step)
        for i in range(self.num_step):
            direc_vals[i] = np.dot(self.samples[i, :], norm_path[:, 0])
            stop_vals[i] = np.dot(self.samples[i, :], norm_path[:, 1])
        
        if show:
            plt.plot(direc_vals)
            plt.plot(stop_vals)

        f, l, r, s = self.fuzzify_direc_val(direc_vals, stop_vals)

        if show:
            plt.figure()
            plt.plot(f)
            plt.plot(l)
            plt.plot(r)
            plt.plot(s)

        sig_dict = {
            'f': np.multiply(f, self.decay_mask),
            'l': np.multiply(l, self.decay_mask),
            'r': np.multiply(r, self.decay_mask),
            's': np.multiply(s, self.decay_mask)
        }

        comm = self.inst_filter.update(sig_dict)

        if show:
            plt.show()
        
        return comm
        
    def normalize_path(self, path):

        # normalize path to some (-1, 0, 1)
        len_path = len(path)
        center = int((self.num_col - 1) / 2)
        norm_path = np.zeros((self.num_row, 2))

        for i in range(len_path):
            norm_path[i, 0] = path[i] - center

        for i in range(len_path, self.num_row):
            norm_path[i, 1] = 1.0

        return norm_path

    def fuzzify_direc_val(self, direc_vals, stop_vals):
        
        direc_f = fuzzy.trimf(direc_vals, [-1, 0, 1])
        direc_l = fuzzy.zmf(direc_vals, -1, 0)
        direc_r = 1.0 - fuzzy.zmf(direc_vals, 0, 1)
        stop = 1.0 - fuzzy.zmf(stop_vals, 0.5, 1.5)

        return direc_f, direc_l, direc_r, stop

if __name__ == "__main__":

    f = FuzzyFilter(4, 26, 39, 0.5, 1.5)
    path = [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 19, 19, 19, 19, 19, 19, 19, 19, 19]
    path1 = [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 19, 19, 19]
    f.update(path1)