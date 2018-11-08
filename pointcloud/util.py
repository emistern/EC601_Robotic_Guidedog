import time
import numpy as np
from open3d import *
from get_pointcloud import *
import matplotlib.pyplot as plt

def downsample(pc_raw):

    points = np.zeros((len(pc_raw), 3))
    for i in range(0, len(pc_raw), 50):
        p = pc_raw[i]
        points[i, 0] = -p[0]
        points[i, 1] = p[2]
        points[i, 2] = -p[1]
        #print (dir(p))
        #input()
    downsampled_points = points[~np.all(points == 0, axis=1)]

    return downsampled_points

def denoise(downsampled_points):

    # construct a point cloud object in open3d
    pc = open3d.PointCloud()
    pc.points = open3d.Vector3dVector(np.asanyarray(downsampled_points))

    st_time = time.time()

    # remove radius outliers
    pc_filtered,ind = radius_outlier_removal(pc,
            nb_points=10, radius=0.2)

    # get the data back from point cloud
    filtered_points = np.asanyarray(pc_filtered.points)

    # get bounds from point cloud
    max_bounds = pc_filtered.get_max_bound()
    min_bounds = pc_filtered.get_min_bound()
    max_z = max_bounds[2] - t
    min_z = min_bounds[2] + t

    return filtered_points, max_z, min_z

def crop(filtered_points, max_z, min_z):

    # crop the point cloud with roi
    cropped_points = np.zeros((len(filtered_points), 3))
    for i, p in enumerate(filtered_points):
        if (p[2] < max_z and p[2] > min_z):
            cropped_points[i] = p
    cropped_points = cropped_points[~np.all(cropped_points == 0, axis=1)]

    return cropped_points

def cast(cropped_points, show=False):

    # cast the point cloud into 3d plane
    obstacle_points = np.matmul(cropped_points, np.array([[1, 0], [0, 1], [0, 0]]))
    if show:
        plt.scatter(obstacle_points[:, 0], obstacle_points[:, 1])
        plt.show()

    return obstacle_points

def show_pointcloud(cropped_points):
    # show the cropped point cloud
    pc_cropped = open3d.PointCloud()
    pc_cropped.points = open3d.Vector3dVector(np.asanyarray(cropped_points))
    open3d.draw_geometries([pc_cropped])

def pipeline(pc_raw, show=False):

    downsampled_points = downsample(pc_raw)

    filtered_points, max_z, min_z = denoise(downsampled_points)

    cropped_points = crop(filtered_points, max_z, min_z)

    obstacle_points = cast(cropped_points, show=show)

    if show:
        show_pointcloud(cropped_points)

    return obstacle_points

if __name__ == "__main__":

    # define a tolerance for cropping
    t = 0.3

    # instantiate a cloud point generattor
    pc_gen = get_pointcloud_frame("../realsense/20181011_223353.bag")

    # get a frame of point cloud from bag file
    st_time = time.time()
    pc_raw = next(pc_gen)

    pipeline(pc_raw, show=True)
    input()



    points = np.zeros((len(pc_raw), 3))
    for i in range(0, len(pc_raw), 50):
        p = pc_raw[i]
        points[i, 0] = -p[0]
        points[i, 1] = p[2]
        points[i, 2] = -p[1]
        #print (dir(p))
        #input()
    downsampled_points = points[~np.all(points == 0, axis=1)]

    ed_time = time.time()
    print("downsample from ", points.shape, " to ", downsampled_points.shape, " in ", st_time - ed_time)

    # construct a point cloud object in open3d
    pc = open3d.PointCloud()
    pc.points = open3d.Vector3dVector(np.asanyarray(downsampled_points))

    st_time = time.time()

    # remove radius outliers
    pc_filtered,ind = radius_outlier_removal(pc,
            nb_points=10, radius=0.2)

    # visualize the point cloud using open3d
    #open3d.draw_geometries([pc_filtered])

    # get the data back from point cloud
    filtered_points = np.asanyarray(pc_filtered.points)

    # get bounds from point cloud
    max_bounds = pc_filtered.get_max_bound()
    min_bounds = pc_filtered.get_min_bound()
    max_z = max_bounds[2] - t
    min_z = min_bounds[2] + t

    # crop the point cloud with roi
    cropped_points = np.zeros((len(filtered_points), 3))
    for i, p in enumerate(filtered_points):
        if (p[2] < max_z and p[2] > min_z):
            cropped_points[i] = p
    cropped_points = cropped_points[~np.all(cropped_points == 0, axis=1)]

    ed_time = time.time()

    print("crop from ", filtered_points.shape, " to ", cropped_points.shape, " in ", ed_time - st_time)

    # cast the point cloud into 3d plane
    obstacle_points = np.matmul(cropped_points, np.array([[1, 0], [0, 1], [0, 0]]))
    plt.scatter(obstacle_points[:, 0], obstacle_points[:, 1])
    plt.show()

    # show the cropped point cloud
    pc_cropped = open3d.PointCloud()
    pc_cropped.points = open3d.Vector3dVector(np.asanyarray(cropped_points))
    open3d.draw_geometries([pc_cropped])