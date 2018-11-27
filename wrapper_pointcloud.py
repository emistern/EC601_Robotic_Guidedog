from wall_detection import image2birdview
from path_planning import path_planner, path_filter
from path_planning.path_planner_aStar import path_planner as path_planner_aStar
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
    inflate_diag = args.inflate_diag

    # local variables
    frame_count = 0
    map_time_buf = 0
    plan_time_buf = 0
    disp_time_buf = 0
    if num_frames > 0: # if run a finite number of frames
        time_record = np.zeros((num_frames, 2)) # init a buffer for storing running time

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
    interface = voice_class.VoiceInterface(straight_file='voice/straight.wav',
                                            turnleft_file = 'voice/turnleft.wav',
                                            turnright_file = 'voice/turnright.wav',
                                            hardleft_file = 'voice/hardleft.mp3',
                                            hardright_file = 'voice/hardright.mp3',
                                            STOP_file = 'voice/STOP.mp3',
                                            noway_file = 'voice/noway.mp3')

    # slice and quantilize the depth matrix
    squeeze = image2birdview.depth_bird_view()

    while(True):
        if timing:
            print("------ frame", frame_count," ------")
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
                                                            show=show, cheb=use_chebyshev, inflate_diag=inflate_diag,
                                                            timing=timing)

        t_map_e = time.time()  # mapping time end

        # perform path planning on the map
        t_plan_s = time.time() # planning time start
        
        if not args.astar:
            djikstra_planner = path_planner.path_planner(map_depth)
            djikstra_planner.gen_nodes()   # path planner initializetion
            djikstra_planner.gen_paths()   # path planner initializetion
            djikstra_planner.gen_buffer_mats() # path planner initializetion
            djikstra_planner.plan()        # path planner planning
            if target is None:  # if not using chebyshev center to find target, use default target
                target = djikstra_planner.find_default_target(int(num_row/size_col))
        else:
            pass # put astar planning here
            a_star_plan = path_planner_aStar(map_depth, [])
            if len(a_star_plan.goal)==0:
                path = []
            else:
                print(a_star_plan.goal)
                a_star_plan.gen_heuristics(2)
                a_star_plan.gen_graph()
                startpos = a_star_plan.pick_start_pos()
                path = a_star_plan.path_search(startpos)
                print(startpos, path)

        t_plan_e = time.time() # planning time end
        if timing:
                map_time = t_map_e - t_map_s
                plan_time = t_plan_e - t_plan_s
        
        if not facing_wall: # if there is a valid target

            t_ds_st = time.time() # displaying time start

            if not args.astar:
                if (djikstra_planner.check_target_valid(target)):
                    path = djikstra_planner.find_optimal_path(target)
                else:
                    path = []
                djikstra_planner.draw_path(path)
            else:
                pass # put astar path findind and drawing here
                a_star_plan.draw_path(path)

            #dw.show_depth_matrix("", dep_mat)

            t_ds_ed = time.time() # displaying time end
            
            roi_sqr = int(roi_mtr / (size_col / num_row))
            direc = path_filter.compute_weighted_average(path, num_row, num_col, roi_sqr, thresh=args.path_thresh)

            if (direc == 0):
                cv2.imshow("direction", arrow_f)
            elif (direc == 1):
                cv2.imshow("direction", arrow_r)
            else:
                cv2.imshow("direction", arrow_l)

            if timing:
                map_time = t_map_e - t_map_s
                plan_time = t_plan_e - t_plan_s
                disp_time = t_ds_ed - t_ds_st
                print("map  time  " + str(map_time))
                print("plan time  " + str(plan_time))
                print("disp time  " + str(disp_time))
                print("total time " + str(t_plan_e - t_map_s))
                if(num_frames != 0):
                    pass
            
            if use_voice:
                interface.play2([direc])
        else:  # there is not valid target
            if use_voice:
                interface.play2([])
            if not args.astar:
                djikstra_planner.draw_path([])
            else:
                a_star_plan.draw_path([])
            cv2.imshow("direction", stop_sn)
            #dw.show_depth_matrix("", dep_mat)

            print("no path")
        
        cv2.waitKey(20)

        if(num_frames != 0 and frame_count >= num_frames):   # check limited number for playing
            print("------ Print Running Stats ------")
            print("Total frame number:    ", num_frames)
            print("Average planning time: ", plan_time_buf / num_frames,  " standard deviation: ", np.std(time_record[:, 1]))
            print("Average mapping time:  ", map_time_buf  / num_frames,  " standard deviation: ", np.std(time_record[:, 0]))
            #print("Average display time:  ", disp_time_buf / num_frames)
            quit()
        else:
            if timing:
                map_time_buf += map_time
                plan_time_buf += plan_time
                #disp_time_buf += disp_time
                if num_frames > 0:
                    time_record[frame_count, 0] = map_time
                    time_record[frame_count, 1] = plan_time
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
    parser.add_argument("--row", help="number of rows in map", default=26, type=int)
    parser.add_argument("--col", help="number of columns in map", default=39, type=int)
    parser.add_argument("--row_size", help="size of each row in meters", default=6, type=int)
    parser.add_argument("--col_size", help="size of each column in meters", default=4, type=int)
    parser.add_argument("--roi", help="region of interest in meters", default=1.5, type=float)
    parser.add_argument("--astar", help="wether use astar path planning algorithm", default=False, type=bool)
    parser.add_argument("--path_thresh", help="threshold for path filter", default=0.8, type=float)
    parser.add_argument("--inflate_diag", default=False, type=bool)
    args = parser.parse_args()
    
    print("-------- PRINT ARGUMENTS --------")
    arg_data = parser.parse_args()
    for key, value in vars(arg_data).items():
        print("{:<15}".format(key), " : ", value)
    print("---------------------------------")
    print("press ENTER to start:")
    input()

    ModuleWrapper(args)
