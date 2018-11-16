from wall_detection import image2birdview
from path_planning import path_planner
from voice import voice_class
import time
import numpy as np
from realsense.rs_depth_util import *
from get_frame import *
import sys
sys.path.append("./pointcloud/")
from pointcloud.get_pointcloud import *
from pointcloud.util import *
from pointcloud.pipeline_pc import pointcloud_pipeline


def ModuleWrapper():
    
    # Parameters used by map builder
    num_slice = 14    # how many slices of the depth matrix
    num_section = 11   # how many section to quantilize
    max_per_occ = 0.3 # percentage of 1s in a section to judge as occupied

    use_pointcloud = True
    use_bag = True

    # Specify the depth matrix you want to use
    dep_mat_fn = 'wall_detection/samples/depth0009.npy'
    dep_mat_static = np.load(dep_mat_fn)

    # Instantiate a depth worker object to display depth matrix
    dw = depth_worker()
    #dw.show_depth_matrix(dep_mat_fn)

    # initialize the camera frame iterator
    if use_bag:
        img_gen = get_pointcloud_frame("./realsense/20181011_223353.bag")
    else:
        img_gen = get_frame()

    # instantiate an interface
    interface = voice_class.VoiceInterface(straight_file='voice/straight.mp3',
                                            turnleft_file = 'voice/turnleft.mp3',
                                            turnright_file = 'voice/turnright.mp3',
                                            hardleft_file = 'voice/hardleft.mp3',
                                            hardright_file = 'voice/hardright.mp3',
                                            STOP_file = 'voice/STOP.mp3',
                                            noway_file = 'voice/noway.mp3')

    while(True):
        facing_wall = False

        # fetch an image from camera
        dep_mat, pointcloud = next(img_gen)

        t_map_s = time.time()

        # slice and quantilize the depth matrix
        squeeze = image2birdview.depth_bird_view()

        if not use_pointcloud:

            squeezed_matrix = squeeze.squeeze_matrix(dep_mat, num_slice=num_slice)

            map_depth = squeeze.quantilize(squeezed_matrix, n_sec=num_section, max_per_occ=max_per_occ)
        else:

            #map_depth, target, facing_wall = pipeline(pointcloud, row = num_slice, col = num_section, row_size = 6, col_size = 10, show=True)
            map_depth, target, facing_wall = pointcloud_pipeline(pointcloud, row_num = num_slice, col_num = num_section, row_size = 6, col_size = 6, show=True)

        t_map_e = time.time()

        # perform path planning on the map
        t_plan_s = time.time()
        #print(map_depth)
        p = path_planner.path_planner(map_depth)
        p.gen_nodes()
        p.gen_paths()
        p.gen_buffer_mats()
        p.plan()
        if target is None:
            target = p.find_default_target()
        if not facing_wall:
            if (p.check_target_valid(target)):
                path = p.find_optimal_path(target)
            else:
                path = []
            t_plan_e = time.time()
            p.draw_path(path)
            dw.show_depth_matrix("", dep_mat)
            print("map time  " + str(t_map_e - t_map_s))
            print("plan time " + str(t_plan_e - t_plan_s))
            print("total time" + str(t_plan_e - t_map_s))
            cv2.waitKey(200)
            
            #interface.play3(path,num_section)
        else:
            #interface.play3([],num_section)
            print("no path")
        #quit()
        #input()

if __name__ == "__main__":

    ModuleWrapper()
