import numpy as np
import matplotlib.pyplot as plt
from open3d import PointCloud, Vector3dVector, draw_geometries

def show_pointcloud(points):

    """
    using open3d to show point cloud
    Input:
    points: a list of points in points cloud with shape (m, 3)
    """

    assert np.asanyarray(points).shape[1] == 3 # make sure the shape is correct

    pc_cropped = PointCloud()
    pc_cropped.points = Vector3dVector(np.asanyarray(points))
    draw_geometries([pc_cropped])

def show_points2D(points):

    """
    using matplotlib to show points in 2D
    Input:
    points: a list of points in points cloud with shape (m, 2)
    """

    assert np.asanyarray(points).shape[1] == 2

    plt.scatter(points[:, 0], points[:, 1])
    plt.show()
