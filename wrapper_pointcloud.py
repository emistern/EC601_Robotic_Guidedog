from wall_detection import image2birdview
from path_planning import path_planner, path_filter
from voice import voice_class
import time
import cv2
import numpy as np
from realsense.rs_depth_util import depth_worker
from get_frame import get_frame
import sys
sys.path.append("./pointcloud/")
from pointcloud.get_pointcloud import get_pointcloud_frame
from pointcloud.pipeline_pc import pointcloud_pipeline
import argparse


def ModuleWrapper(args):
    
    # Parameters used by map builder
    num_row = args.row    # how many slices of the depth matrix
    num_col = args.col   # how many section to quantilize
    size_row = args.row_size
    size_col = args.col_size
    max_per_occ = 0.3 # percentage of 1s in a section to judge as occupied

    use_pointcloud = args.pointcloud 
    use_bag = args.bagfile
    use_chebyshev = args.chebyshev
    use_voice = args.voice
    show = args.verbose
    timing = args.time
    num_frames = args.frames
    downsample_rate = args.downsamplerate
    roi_mtr = args.roi
    frame_count = 0

    # arrow images
    arrow_f = cv2.imread("./images/arrow_f.png")
    arrow_l = cv2.imread("./images/arrow_l.png")
    arrow_r = cv2.imread("./images/arrow_r.png")
    stop_sn = cv2.imread("./images/stop.png")

    # Specify the depth matrix you want to use
    dep_mat_fn = 'wall_detection/samples/depth0009.npy'
    dep_mat_static = np.load(dep_mat_fn)

    # Instantiate a depth worker object to display depth matrix
    dw = depth_worker()

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

    # slice and quantilize the depth matrix
    squeeze = image2birdview.depth_bird_view()

    while(True):
        print("------ new frame ------")
        facing_wall = False
        target = None

        # fetch an image from camera
        dep_mat, pointcloud = next(img_gen)

        t_map_s = time.time() # mapping time start

        if not use_pointcloud:

            squeezed_matrix = squeeze.squeeze_matrix(dep_mat, num_slice=num_row)

            map_depth = squeeze.quantilize(squeezed_matrix, n_sec=num_col, max_per_occ=max_per_occ)
        else:
            # point cloud map builder pipeline
            map_depth, target, facing_wall = pointcloud_pipeline(pointcloud, 
                                                            ds_rate=downsample_rate,
                                                            row_num = num_row, col_num = num_col, 
                                                            row_size = size_row, col_size = size_col, 
                                                            show=show, cheb=use_chebyshev, timing=timing)

        t_map_e = time.time()  # mapping time end

        # perform path planning on the map
        t_plan_s = time.time() # planning time start
        
        djikstra_planner = path_planner.path_planner(map_depth)
        djikstra_planner.gen_nodes()   # path planner initializetion
        djikstra_planner.gen_paths()   # path planner initializetion
        djikstra_planner.gen_buffer_mats() # path planner initializetion
        djikstra_planner.plan()        # path planner planning

        t_plan_e = time.time() # planning time end

        if target is None:  # if not using chebyshev center to find target, use default target
            target = djikstra_planner.find_default_target(int(num_row/size_col))
        if not facing_wall and target != None: # if there is a valid target
            if (djikstra_planner.check_target_valid(target)):
                path = djikstra_planner.find_optimal_path(target)
            else:
                path = []

            t_ds_st = time.time() # displaying time start

            djikstra_planner.draw_path(path)
            #dw.show_depth_matrix("", dep_mat)

            t_ds_ed = time.time() # displaying time end
            
            roi_sqr = int(roi_mtr / (size_col / num_row))
            direc = path_filter.compute_weighted_average(path, num_row, num_col, roi_sqr)

            if (direc == 0):
                cv2.imshow("direction", arrow_f)
            elif (direc == 1):
                cv2.imshow("direction", arrow_r)
            else:
                cv2.imshow("direction", arrow_l)

            if timing:
                print("map  time  " + str(t_map_e - t_map_s))
                print("plan time  " + str(t_plan_e - t_plan_s))
                print("disp time  " + str(t_ds_ed - t_ds_st))
                print("total time" + str(t_plan_e - t_map_s))
            
            if use_voice:
                interface.play3(path,num_col)
        else:  # there is not valid target
            if use_voice:
                interface.play3([],num_col)
            djikstra_planner.draw_path([])
            cv2.imshow("direction", stop_sn)
            #dw.show_depth_matrix("", dep_mat)

            print("no path")
        
        cv2.waitKey(20)

        if(num_frames != 0 and frame_count >= num_frames):   # check limited number for playing
            quit()
        else:
            frame_count += 1

        if(args.input):   # check input
            input()

        if(args.oneshot):  # check oneshot
            quit()

        

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bagfile", help="if use bagfile", default=False, type=bool)
    parser.add_argument("-p", "--pointcloud", help="if use pointcloud", default=True, type=bool)
    parser.add_argument("-verb", "--verbose", help="display the points", default=False, type=bool)
    parser.add_argument("-t", "--time", help="if timing the program", default=False, type=bool)
    parser.add_argument("-c", "--chebyshev", help="whteter use chebyshev", default=False, type=bool)
    parser.add_argument("-v", "--voice", help="if output voice", default=False, type=bool)
    parser.add_argument("-o", "--oneshot", help="one shot for testing", default=False, type=bool)
    parser.add_argument("-i", "--input", help="press enter for each frame", default=False, type=bool)
    parser.add_argument("-f", "--frames", help="how many frames you want to play", default=0, type=int)
    parser.add_argument("-r", "--downsamplerate", help="downsampling rate", default=60, type=int)
    parser.add_argument("--row", help="number of rows in map", default=20, type=int)
    parser.add_argument("--col", help="number of columns in map", default=29, type=int)
    parser.add_argument("--row_size", help="size of each row in meters", default=6, type=int)
    parser.add_argument("--col_size", help="size of each column in meters", default=4, type=int)
    parser.add_argument("--roi", help="region of interest in meters", default=1.0, type=float)
    args = parser.parse_args()
    print("Using Bag File:    ", args.bagfile)
    print("Using Point Cloud: ", args.pointcloud)
    print("Timing:            ", args.time)
    #quit()
    ModuleWrapper(args)
