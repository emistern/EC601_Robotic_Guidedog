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

def compute_weighted_average(path, num_row, num_col, roi_rate=0.3, thresh=0.5):

    """
    compute the weighted average of path with roi
    """
    print(path)
    center = int((num_col - 1) / 2)
    roi = int(roi_rate * num_row)
    norm_path = np.array(path.copy(), dtype=np.int32) - center
    print(norm_path)
    weights = compute_exp_weights(len(path), roi=roi)
    direc = np.dot(norm_path, weights)
    print(direc)
    if (direc > thresh):
        return 1
    elif (direc < -thresh):
        return -1
    else:
        return 0