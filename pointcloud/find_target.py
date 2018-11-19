import numpy as np
from ChebyshevCenter import ChebyshevCenter
from polygon import polygon

def cheb(points, show=False):

    # preprocessing points
    y = points[:, 1]

    ofs_y = (np.max(y) - np.min(y)) / 2 + abs(np.min(y))
    points[:, 1] = points[:, 1] - ofs_y

    p = polygon(points)

    c = ChebyshevCenter(p)

    c._transform()

    #c.showPolygon()

    center = c.solve(show=show)
    center[1] += ofs_y
    points[:, 1] = points[:, 1] + ofs_y

    return center

def find_target(center, row_size, mask_row, mask_col):

    # find the target
    x_f = center[0] + abs(row_size/2)
    y_f = center[1]
    _x = x_f * mask_row
    x_i = np.max(np.where( _x > 1 ))
    _y = y_f * mask_col
    y_i = np.max(np.where( _y > 1 ))
    target = [y_i, x_i]

    return target