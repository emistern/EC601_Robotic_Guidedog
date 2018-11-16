import numpy as np

def gen_mask(row_num, col_num):

    """
    generate a default mask for map builder
    """

    mask = np.zeros((row_num, col_num))
    bound1 = min([row_num, col_num]) / 2 
    t = 2
    for i in range(row_num):
        for j in range(col_num):
            if (i + j < bound1 - t):
                mask[i, j] = 1
            if (i + (col_num - j) < bound1 - t + 1):
                mask[i, j] = 1
    return mask