from wall_detection import image2birdview
from path_planning import path_planner, path_filter
from path_planning.path_planner_aStar import path_planner as path_planner_aStar
from voice import voice_class
from voice.inst_filter import InstructionFilter
import time
import cv2
import numpy as np
from realsense.rs_depth_util import depth_worker
from get_frame import get_frame
import sys
sys.path.append("./pointcloud/")
sys.path.append("./postprocess/")
from pointcloud.get_pointcloud import get_pointcloud_frame
from pointcloud.pipeline_pc import pointcloud_pipeline
from postprocess.fuzzyfilter import FuzzyFilter
from door_coord import find_door_pointcloud
from tinyYOLOv2 import obj_det
from s2cart import sphere2cart
import argparse

use_tensor = True


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
    if args.count_grid:
        grid_count = 0

    # arrow images
    arrow_f = cv2.imread("./images/arrow_f.png")
    arrow_l = cv2.imread("./images/arrow_l.png")
    arrow_r = cv2.imread("./images/arrow_r.png")
    stop_sn = cv2.imread("./images/stop.png")
    wait_sn = cv2.imread("./images/wait.jpg")

    # Specify the depth matrix you want to use
    dep_mat_fn = 'wall_detection/samples/depth0009.npy'
    dep_mat_static = np.load(dep_mat_fn)

    # Instantiate a depth worker object to display depth matrix
    dw = depth_worker()

    # initialize the camera frame iterator
    if use_bag:
        img_gen = get_pointcloud_frame("./realsense/dense.bag")
    else:
        img_gen = get_frame()

    # instantiate an interface
    if args.stereo:
        interface = voice_class.VoiceInterface(
            straight_file ='sounds/steel_bell.wav',
            turnleft_file = 'sounds/left.wav',
            turnright_file = 'sounds/right.wav',
            hardleft_file = 'voice/hardleft.mp3',
            hardright_file = 'voice/hardright.mp3',
            STOP_file = 'voice/STOP.mp3',
            noway_file = 'sounds/guitar.wav',
            wait_file = 'sounds/ice_bell.wav'
        )
    else:
        interface = voice_class.VoiceInterface(straight_file = 'voice/straight.mp3',
                                            turnleft_file = 'voice/turnleft.mp3',
                                            turnright_file = 'voice/turnright.mp3',
                                            hardleft_file = 'voice/hardleft.mp3',
                                            hardright_file = 'voice/hardright.mp3',
                                            STOP_file = 'voice/STOP.mp3',
                                            noway_file = 'voice/noway.mp3')

    # slice and quantilize the depth matrix
    squeeze = image2birdview.depth_bird_view()

    # instruction temporal filter
    inst_filt = InstructionFilter()

    fuzzy_filter = FuzzyFilter(size_col, num_row, num_col, 0.75, roi_mtr)

    if use_tensor:
        t = obj_det.obj_det()

    while(True):
        if timing:
            print("------ frame", frame_count," ------")
        facing_wall = False
        target = None

        # fetch an image from camera
        if show or use_tensor:
            col_mat, dep_mat, pointcloud = next(img_gen)
        else:
            _, dep_mat, pointcloud = next(img_gen)

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
                                                            timing=timing, no_mask=args.no_mask, no_inflate=args.no_inflate)


             # Coord is the coordinate of the target
            if use_tensor:
                coord = t.detect_frame(col_mat)
                print(coord)

                # find the coordinate in map with depth matrix and bounding box
                if(len(coord)!=0):
                    print("In the coord")
                    cv2.rectangle(col_mat,(coord[0],coord[2]),(coord[1],coord[3]),(0,255,0),3)
                    target_door = find_door_pointcloud(dep_mat, coord)
                    print("size_row: "+str(size_row))
                    print("y is: "+str(target_door[1]))
                    print("num_row is: "+str(num_row))
                    print("num_col is: "+str(num_col))
                    target = sphere2cart(target_door[0], target_door[1], target_door[2], num_row, num_col, size_row, size_col,map_depth, hfov = 69.4, vfov = 42.5, resolution_x = 640, resolution_z = 480)
                    print(target)
                print(target)


        t_map_e = time.time()  # mapping time end

        if args.count_grid:
            # count the number of 1s in grid map
            count = np.sum(np.matrix(map_depth))
            grid_count += count
            print("number of 1s in grid map: ", count, "; total suqare: ", num_row*num_col, "; percentage: ", count/(num_row*num_col))

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
            if target is not None:
                a_star_plan = path_planner_aStar(map_depth, target)
            else:
                a_star_plan = path_planner_aStar(map_depth, [])
            if len(a_star_plan.goal)==0:
                path = []
            else:
                a_star_plan.gen_heuristics(2)
                a_star_plan.gen_graph()
                startpos = a_star_plan.pick_start_pos()
                path = a_star_plan.path_search(startpos)

        t_plan_e = time.time() # planning time end
        if timing:
                map_time = t_map_e - t_map_s
                plan_time = t_plan_e - t_plan_s

        t_ds_st = time.time() # displaying time start

        if not args.astar:
            if (target != None and djikstra_planner.check_target_valid(target)):
                path = djikstra_planner.find_optimal_path(target)
            else:
                path = []
            djikstra_planner.draw_path(path)
        else:
            pass # put astar path findind and drawing here
            a_star_plan.draw_path(path)

        if show:
            dw.show_depth_matrix("depth image", cv2.resize(dep_mat, (640, 480)))
        cv2.imshow("color image", cv2.resize(col_mat, (640, 480)))

        t_ds_ed = time.time() # displaying time end
                    
        roi_sqr = int(roi_mtr / (size_col / num_row))

        if args.fuzzy:
            direc = fuzzy_filter.update(path)
        elif len(path) > 0:
            direc = path_filter.compute_weighted_average(path, num_row, num_col, roi_sqr, thresh=args.path_thresh)
            direc = inst_filt.update(direc)
        else:
            direc = inst_filt.update(path)
            if direc != []:
                direc = 2

        if (direc == 0):
            cv2.imshow("direction", arrow_f)
        elif (direc == 1):
            cv2.imshow("direction", arrow_r)
        elif (direc == -1):
            cv2.imshow("direction", arrow_l)
        elif (direc == []):
            cv2.imshow("direction", stop_sn)
            direc = 3
        elif (direc == 2):
            cv2.imshow("direction", wait_sn)
        if use_voice:
            interface.play_on_edge(direc)

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

        cv2.waitKey(20)

        if(num_frames != 0 and frame_count >= num_frames-1):   # check limited number for playing
            print("------ Print Running Stats ------")
            print("Total frame number:    ", num_frames)
            print("Average planning time: ", plan_time_buf / num_frames,  " standard deviation: ", np.std(time_record[:, 1]))
            print("Average mapping time:  ", map_time_buf  / num_frames,  " standard deviation: ", np.std(time_record[:, 0]))
            #print("Average display time:  ", disp_time_buf / num_frames)
            if args.count_grid:
                avr_count = grid_count / num_frames
                print("average 1s in grid map: ", avr_count, "; total suqare: ", num_row*num_col, "; percentage: ", avr_count/(num_row*num_col))
            quit()
        else:
            if timing and num_frames > 0:
                map_time_buf += map_time
                plan_time_buf += plan_time
                #disp_time_buf += disp_time
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
    parser.add_argument("-r", "--downsamplerate", help="downsampling rate", default=120, type=int)
    parser.add_argument("-s", "--stereo", help="if use stereo sound", default=True, type=bool)
    parser.add_argument("--row", help="number of rows in map", default=26, type=int)
    parser.add_argument("--col", help="number of columns in map", default=39, type=int)
    parser.add_argument("--row_size", help="size of each row in meters", default=6, type=int)
    parser.add_argument("--col_size", help="size of each column in meters", default=4, type=int)
    parser.add_argument("--roi", help="region of interest in meters", default=1.5, type=float)
    parser.add_argument("--astar", help="wether use astar path planning algorithm", default=False, type=bool)
    parser.add_argument("--path_thresh", help="threshold for path filter", default=0.8, type=float)
    parser.add_argument("--no_mask", default=False)
    parser.add_argument("--no_inflate", default=False)
    parser.add_argument("--inflate_diag", default=False, type=bool)
    parser.add_argument("--fuzzy", default=False, type=bool)
    parser.add_argument("--count_grid", default=False, type=bool)
    args = parser.parse_args()
    
    print("-------- PRINT ARGUMENTS --------")
    arg_data = parser.parse_args()
    for key, value in vars(arg_data).items():
        print("{:<15}".format(key), " : ", value)
    print("---------------------------------")
    print("press ENTER to start:")
    input()

    ModuleWrapper(args)