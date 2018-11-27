## Point Cloud Utils for Robotics Guide Dog

* This folder contains utility code for processing point cloud data used by our system. by using point cloud, we can get a more accurate map from depth camera. 

### Subfolders:

    1. experiments: MATLAB code for experiments on point cloud(Conputer Vision Systame Toolbox)
    2. sample: sample point cloud data in .ply format
   
### Experiments:

#### Generate point cloud from .bag file

use the **save_pointcloud_to_ply** function in **rs_depth_util.py** under **realsense** folder

#### Use MATLAB to process and show the point cloud

Remember first to put code and sample to a directory that is visible to MATLAB.

1. use RANSAC to fit the ground plane with a pre-defined normal vector:
   
    pipline_fit()

<img src="../images/pointcloud_to_map.jpg" height=500>

2. crop the point cloud with a ROI(region of interest):

    pipline_crop()

<img src="../images/pointcloud_crop.jpg" height=250>

#### Use Python to perform simple point cloud processing

list of python modules useful to process point cloud

1. pipeline_pc.py
   
   A top level wrapper for all the modules
2. downsample_pc.py
   
   Downsamplgin function
3. processing_pc.py
   
   Filting, Cropping, Casting point cloud
4. find_target.py
   
   Find a target position (using linear programming to solve Chebyshev Center)
5. decomposite.py

   transform the points into a grid of occupency

utilities

1. display_pc.py

    display point cloud and 2D obstacle points
2. get_pointcloud.py

    generate points from bag file

## Point Cloud Registration and Stitching

(11/21)
trying to perform point cloud registration in MATLAB, with samples taken from bag file