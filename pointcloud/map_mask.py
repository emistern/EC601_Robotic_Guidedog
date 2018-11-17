import numpy as np

def gen_mask(row_num, col_num):

    """
    generate a default mask for map builder
    """

    mask = np.zeros((row_num, col_num))
    bound1 = min([row_num, col_num]) / 2 
    t = 2
    slope = 1.5
    for i in range(row_num):
        for j in range(col_num):
            if ((i + slope * float(j)) / (0.5 + slope/2) < bound1 - t + 1):
                mask[i, j] = 1
            if ((i + slope * float(col_num - 1 - j)) / (0.5 + slope/2) < bound1 - t + 1):
                mask[i, j] = 1
    return mask