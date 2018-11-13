import time
import numpy as np
from open3d import *
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from ChebyshevCenter import *
from polygon import *

import sys
sys.path.append("./pointcloud")

def downsample(pc_raw):

    points = np.zeros((len(pc_raw), 3))
    for i in range(0, len(pc_raw), 50):
        p = pc_raw[i]
        points[i, 0] = p[0]
        points[i, 1] = p[2]
        points[i, 2] = -p[1]
        #print (dir(p))
        #input()
    downsampled_points = points[~np.all(points == 0, axis=1)]

    return downsampled_points

def denoise(downsampled_points, t=0.3):

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
    x_ofs = min(abs(min_bounds[0]), abs(max_bounds[0]))
    x_range = x_ofs * 2 # max_bounds[0] - min_bounds[0]

    return filtered_points, max_z, min_z, x_range, x_ofs

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

def decomposite(obstacle_points, center,
                row = 10, col = 7, 
                col_size = 5, row_size = 5,
                thresh = 20,  show = True):

    # decomposite points into grid
    grid = np.zeros((row, col))

    # some constants
    row_min = min(obstacle_points[:, 0])
    col_min = min(obstacle_points[:, 1])
    row_max = max(obstacle_points[:, 0])
    col_max = max(obstacle_points[:, 1])

    print("point cloud range from", row_min, " ", col_min, " to ", row_max, " ", col_max)

    points_row = obstacle_points[:, 0] + abs(row_size/2) + 0.0001
    points_col = obstacle_points[:, 1] + 0.0001

    if show:
        plt.scatter(points_row, points_col)
    
    row_min = min(points_row)
    col_min = min(points_col)
    row_max = max(points_row)
    col_max = max(points_col)

    print ("append offset")
    print("point cloud range from", row_min, " ", col_min, " to ", row_max, " ", col_max)

    w = row_max
    h = col_max

    mask_row = 1 / np.array(range(col))
    mask_row = mask_row * col / row_size

    mask_col = 1 / np.array(range(row))
    mask_col = mask_col * row / col_size

    print ("with row mask: ", mask_row)
    print ("with column mask: ", mask_col)

    st_time = time.time()
    # loop through the obstacle points
    for i in range(0, len(obstacle_points), 2):
        x_f = points_row[i]
        y_f = points_col[i]
        try:
            _x = x_f * mask_row
            x_i = np.max(np.where( _x > 1 ))
            _y = y_f * mask_col
            y_i = np.max(np.where( _y > 1 ))
        
            grid[y_i, x_i]  += 1
        except:
            pass
        #print(x_f, y_f)
        #print(x_i, y_i)
        #quit()
    print(grid)

    # find the target
    x_f = center[0] + abs(row_size/2)
    y_f = center[1]
    _x = x_f * mask_row
    x_i = np.max(np.where( _x > 1 ))
    _y = y_f * mask_col
    y_i = np.max(np.where( _y > 1 ))
    target = [y_i, x_i]

    grid[y_i, x_i] = 0

    for i in range(row):
        for j in range(col):
            if (grid[i, j] > thresh):
                grid[i, j] = 1
            else:
                grid[i, j] = 0
    ed_time = time.time()
    print("in ", ed_time - st_time, " second, the map: ")
    print(grid)
    if show:
        plt.show()

    return grid, target

def cheb(points):

    # preprocessing points
    y = points[:, 1]

    mean_y = (np.max(y) - np.min(y)) / 2
    points[:, 1] = points[:, 1] - mean_y

    p = polygon(points)

    #hull = ConvexHull(p)

    c = ChebyshevCenter(p)

    c._transform()

    #c.showPolygon()

    center = c.solve(show=False)
    center[1] += mean_y
    points[:, 1] = points[:, 1] + mean_y

    return center
    #quit()

def add_fake(obstacle_points):

    obstacle_points = np.append(obstacle_points, np.array([[-0.1, 3], [0.1, 3]]), 0)

    return obstacle_points

def pipeline(pc_raw, row = 14, col = 11, row_size = 6, col_size = 10, show=False, debug=True):

    downsampled_points = downsample(pc_raw)

    filtered_points, max_z, min_z, w_range, w_ofs = denoise(downsampled_points)

    cropped_points = crop(filtered_points, max_z, min_z)

    obstacle_points = cast(cropped_points, show=False)

    obstacle_points = add_fake(obstacle_points)

    if debug:
        center = cheb(obstacle_points)
        print(center)

    grid, target = decomposite(obstacle_points, center, row = row, col = col, 
                       row_size = row_size, col_size = col_size, 
                       show=show)
    if show:
        #print(obstacle_points)
        show_pointcloud(cropped_points)

    facing_wall = (target[0] < 2)
    print("target: ", target)
    return grid, target, facing_wall

if __name__ == "__main__":
    from get_pointcloud import *

    # define a tolerance for cropping
    t = 0.3

    # instantiate a cloud point generattor
    pc_gen = get_pointcloud_frame("../realsense/20181011_223353.bag")

    # get a frame of point cloud from bag file
    st_time = time.time()
    _, pc_raw = next(pc_gen)

    pipeline(pc_raw, show=True, debug=True)
    quit()

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