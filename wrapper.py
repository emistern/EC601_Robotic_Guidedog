from wall_detection import image2birdview
from path_planning import path_planner
from voice import voice_class
import time
import numpy as np
from realsense.rs_depth_util import *
class ModuleWrapper(object):

    def __init__(self):
        
        # Parameters used by map builder
        num_slice = 10    # how many slices of the depth matrix
        nun_section = 7   # how many section to quantilize
        max_per_occ = 0.3 # percentage of 1s in a section to judge as occupied

        # Specify the depth matrix you want to use
        dep_mat_fn = 'wall_detection/samples/depth0009.npy'
        dep_mat = np.load(dep_mat_fn)

        # Instantiate a depth worker object to display depth matrix
        dw = depth_worker()
        dw.show_depth_matrix(dep_mat_fn)

        # slice and quantilize the depth matrix
        self.squeeze = image2birdview.depth_bird_view()

        t_sq_s = time.time()
        squeezed_matrix = self.squeeze.squeeze_matrix(dep_mat, num_slice=num_slice)
        t_sq_e = time.time()

        t_qu_s = time.time()
        map_depth = self.squeeze.quantilize(squeezed_matrix, n_sec=nun_section, max_per_occ=max_per_occ)
        t_qu_e = time.time()

        # perform path planning on the map
        t_plan_s = time.time()
        p = path_planner.path_planner(map_depth)
        p.gen_nodes()
        p.gen_paths()
        p.gen_buffer_mats()
        p.plan()
        target = p.find_default_target()
        if len(target) > 0:
            path = p.find_optimal_path(target)
            t_plan_e = time.time()
            p.draw_path(path)
            print("squeeze time " + str(t_sq_e - t_sq_s))
            print("quantilize time " + str(t_qu_e - t_qu_s))
            print("plan time" + str(t_plan_e - t_plan_s))

        cv2.waitKey(0)
        i = voice_class.VoiceInterface(straight_file='voice/straight.mp3',
                                       turnleft_file = 'voice/turnleft.mp3',
                                        turnright_file = 'voice/turnright.mp3',
                                        hardleft_file = 'voice/hardleft.mp3',
                                        hardright_file = 'voice/hardright.mp3',
                                        STOP_file = 'voice/STOP.mp3',
                                        noway_file = 'voice/noway.mp3')
        i.play(path,nun_section)

if __name__ == "__main__":

    m = ModuleWrapper()
