from processing_pc import construct_pointcloud, filt_pointcloud, get_bound, get_points, crop_points, cast_points
from downsample_pc import downsample
from find_target import cheb, find_target
from decomposite_pc import append_offset, compute_mask, decomp, thresholding
from display_pc import show_pointcloud, show_points2D
from map_mask import gen_mask

def pointcloud_pipeline(pc_raw, 
                        row_num = 14, col_num = 11, 
                        row_size = 6, col_size = 10, 
                        ds_rate = 50,
                        show=True, cheb=True):
    
    """
    The Point Cloud Map Builder Pipeline
    This Funtion Calls Multiple Modules to Proess Point Cloud Data into Map
    steps:
    1. downsample
    2. denoise(remove outliers)
    3. crop(remove ceiling and floor)
    4. decomposite(use obstacle points to build a occupency grid map)
    5. find target
    """

    ds_pts = downsample(pc_raw, ds_rate)  # downsample the points

    ds_pc = construct_pointcloud(ds_pts)  # instantiate a PointCloud object from Open3D

    filt_pc = filt_pointcloud(ds_pc)      # filt outliers in the point cloud

    max_z, min_z, x_range, x_ofs = get_bound(filt_pc)  # find the bound on z-axis 

    filt_pts = get_points(filt_pc)        # get points back from PointCloud object

    crop_pts = crop_points(filt_pts, max_z, min_z)  # crop the ceiling and floor in points

    obs_pts = cast_points(crop_pts)       # Cast 3D points onto 2D plane

    if cheb:
        center = cheb(obs_pts, show=show)     # find the Chebyshev center of obstacle points in 2D

    pts_row, pts_col = append_offset(obs_pts, row_size)  # prepare for decomposite

    mask_row, mask_col = compute_mask(row_num, col_num, row_size, col_size)  # prepare for decomposite

    grid = decomp(pts_row, pts_col, row_num, col_num, mask_row, mask_col)   # build the grid occupency map

    if cheb:
        target = find_target(center, row_size, mask_row, mask_col)  # find the corresponding suqare in grid map with chebyshev center

        facing_wall = (target[0] < 2)  # check whether you are too close to the wall

    grid = thresholding(grid)      # thresholding the grid map(turn into bit map)

    grid_mask = gen_mask(row_num, col_num)

    grid = grid + grid_mask

    if cheb:
        grid[target[0], target[1]] = 0
    
    print(grid)
    if not cheb:
        target = None
        facing_wall = False

    return grid, target, facing_wall