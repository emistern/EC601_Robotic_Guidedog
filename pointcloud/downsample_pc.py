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

def downsample_vector(pc_raw, rate = 50, num_pts = 10000):

    """ 
    down sample the raw point cloud(trying to improve performance using at the expense of memory)
    Input:
    pc_raw: input raw point matrix with size (m, 3)
    where m is the number of points in the point cloud
    rate: input downsample rate
    Output:
    downsampled_points: output downsampled points with size (m/50, 3)
    
    """
    pts_size = len(pc_raw)
    smp_range = int(pts_size / rate) - 1
    smp_vec = np.array(range(smp_range)) * rate
    smp_pts = np.take(pc_raw, smp_vec, axis=0)
    swap_mtx = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])

    smp_pts = np.ndarray((len(smp_pts), 3), dtype=np.float32, buffer=smp_pts)
    smp_pts = np.matmul(np.asarray(smp_pts), swap_mtx)  # swap axies

    # add a fixed number random downsample
    num_smp_pts = smp_pts.shape[0]
    if num_smp_pts > num_pts:
        rnd_idx = np.random.randint(num_smp_pts, size=num_pts)
        rnd_pts = np.take(smp_pts, rnd_idx, axis=0)
        return rnd_pts

    return smp_pts    