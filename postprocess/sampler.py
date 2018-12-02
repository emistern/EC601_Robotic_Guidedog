# a sampler to generate step masks
import numpy as np
import matplotlib.pyplot as plt

class StepSampler(object):

    def __init__(self, max_dist, num_row, step_size, 
                       roi_mtr, std=1):

        """
        A step sampler to generate masks for calculation directional value on each step
        The first step we use exponential distribution to sample
        the step in the future we use gaussian distribution to sample
        constructor arguments:
            max_dist: the maximum distance reachable by a path,
            num_row : the number of rows in a grid map,
            step_size:the step size you would like to use
            std: determine the shape of
        """

        self.max_dist = max_dist
        self.num_row  = num_row
        self.step_size= step_size
        self.roi_sqr = int(roi_mtr / (max_dist / num_row))
        self.sqr_size = max_dist / num_row
        self.num_step = int(max_dist / step_size)
        
    def gen_sample(self, sigma=0.3):

        """
        calculate sample value for each step
        return a numpy array which each row is a mask for a step
        """

        sample = np.zeros((self.num_step, self.num_row))
        first_step = self.compute_exp_weights(self.num_row, self.roi_sqr)
        for i in range(self.num_step):
            for j in range(self.num_row):
                if i == 0:
                    # the first step use exponential distrubution
                    sample[i, j] = first_step[j]
                else:
                    # the other steps use gaussian distrubution
                    sample[i, j] = self.compute_gaussian(self.step_size*i, sigma, j*self.sqr_size)

        return sample

    def compute_decay_mask(self):
        return self.compute_exp_weights(self.num_step, 1)

    def compute_gaussian(self, mu, sigma, x):
        # compute value of a gaussian function at some point
        v = np.exp(-(((x - mu)/sigma) ** 2) / 2) #  / (sigma * np.sqrt(2 * np.pi))
        return v

    def compute_exp_weights(self, length, roi):

        """
        weights for processing time series(path)
        compute a weights with @length by exponential function
        only the sample within roi(for example, the first 3 samples) is non-trivial
        """

        list_int = range(length)
        list_flo = np.array(list_int) * (3.0/ roi)  # 3 here is a fixed nmber

        return 1.0 / np.exp(list_flo)

if __name__ == "__main__":

    s = StepSampler(4, 26, 0.75, 1.5)
    sample = s.gen_sample()
    for i in range(sample.shape[0]):
        plt.plot(sample[i ,:])
    plt.show()