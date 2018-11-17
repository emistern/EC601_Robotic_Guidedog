import numpy as np

def compute_exp_weights(length, roi):

    """
    weights for processing time series(path)
    compute a weights with @length by exponential function
    only the sample within roi(for example, the first 3 samples) is non-trivial
    """

    list_int = range(length)
    list_flo = np.array(list_int) * (3.0/ roi)  # 3 here is a fixed nmber

    return 1.0 / np.exp(list_flo)