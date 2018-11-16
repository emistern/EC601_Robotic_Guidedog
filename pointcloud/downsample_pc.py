import numpy as np

def downsample(pc_raw, rate = 50):

    """ 
    down sample the raw point cloud
    Input:
    pc_raw: input raw point matrix with size (m, 3)
    where m is the number of points in the point cloud
    rate: input downsample rate
    Output:
    downsampled_points: output downsampled points with size (m/50, 3)
    
    """

    points = np.zeros((len(pc_raw), 3))
    for i in range(0, len(pc_raw), rate):
        p = pc_raw[i]
        points[i, 0] = p[0]
        points[i, 1] = p[2]
        points[i, 2] = -p[1]
        #print (dir(p))
        #input()
    downsampled_points = points[~np.all(points == 0, axis=1)]

    return downsampled_points