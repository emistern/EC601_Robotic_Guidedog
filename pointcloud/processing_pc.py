import numpy as np
from open3d import PointCloud, Vector3dVector, radius_outlier_removal

def construct_pointcloud(points):

    """
    construct a point cloud object in open3d
    Input:
    points: a list of points in points cloud with shape (m, 3)
    where m is the number of points
    Output:
    pc: a point cloud object of PointCloud class from open3d, with points
    """

    pc = PointCloud()
    pc.points = Vector3dVector(np.asanyarray(points))

    return pc

def filt_pointcloud(pc):

    """
    remove outliers in point cloud using open3d
    Input:
    pc: a point cloud object of PointCloud class from open3d
    """

    # remove radius outliers
    pc_filtered, _ = radius_outlier_removal(pc,
            nb_points=5, radius=0.1)

    return pc_filtered

def get_bound(pc, t = 0.3):

    """
    get the bounds of 3 axis in the point cloud
    Input:
    pc: a point cloud object of PointCloud class from open3d
    Output:
    """

    # get bounds from point cloud
    max_bounds = pc.get_max_bound()
    min_bounds = pc.get_min_bound()
    max_z = max_bounds[2] - t
    min_z = min_bounds[2] + t
    x_ofs = min(abs(min_bounds[0]), abs(max_bounds[0]))
    x_range = x_ofs * 2 # max_bounds[0] - min_bounds[0]

    return max_z, min_z, x_range, x_ofs

def get_points(pc):

    # get the data back from point cloud
    filtered_points = np.asanyarray(pc.points)

    return filtered_points

def crop_points(points, max_z, min_z):

    """
    crop the points along z-axis based on given bounds, 
    discard the points out of bounds
    """

    # crop the point cloud with roi
    cropped_points = np.zeros((len(points), 3))
    for i, p in enumerate(points):
        if (p[2] < max_z and p[2] > min_z):
            cropped_points[i] = p
    cropped_points = cropped_points[~np.all(cropped_points == 0, axis=1)]

    return cropped_points

def crop_points_np(points, max_z, min_z):

    """
    try to improve cropping performance with numpy functions
    crop the points along z-axis based on given bounds, 
    discard the points out of bounds
    """

    # crop the point cloud with roi 
    z = points[:, 2]
    idx = np.where((z > min_z) & (z < max_z))
    idx = np.array(idx)
    idx = np.ndarray((idx.shape[1]), dtype=np.int32, buffer=idx)
    crop_pts = np.take(points, idx, axis=0)

    return crop_pts

def cast_points(points):

    """
    cast the points from 3D space into a 2D plane
    obstacle points in 3D space become obetacle points in 2D space
    """

    # cast the point cloud into 3d plane
    obstacle_points = np.matmul(points, np.array([[1, 0], [0, 1], [0, 0]]))

    return obstacle_points