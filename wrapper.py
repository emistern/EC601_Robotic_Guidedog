from wall_detection import image2birdview
from path_planning import path_planner
import time

class ModuleWrapper(object):

    def __init__(self):

        self.squeeze = image2birdview.depth_bird_view()

        t_sq_s = time.time()
        squeezed_matrix = self.squeeze.squeeze_matrix()
        t_sq_e = time.time()

        t_qu_s = time.time()
        map_depth = self.squeeze.quantilize(squeezed_matrix)
        t_qu_e = time.time()

        # calculate default target
        #print(map_depth.shape)
        target_row = map_depth.shape[0] - 3
        target_col = (map_depth.shape[1] - 1) / 2
        target = [int(target_row), int(target_col)]
        #print(map_depth)
        #print(target)

        t_plan_s = time.time()
        p = path_planner.path_planner(map_depth)
        p.gen_nodes()
        p.gen_paths()
        p.gen_buffer_mats()
        path = p.plan(target)
        t_plan_e = time.time()
        #print(path)
        p.draw_path(path)
        print("squeeze time " + str(t_sq_e - t_sq_s))
        print("quantilize time " + str(t_qu_e - t_qu_s))
        print("plan time" + str(t_plan_e - t_plan_s))

if __name__ == "__main__":

    m = ModuleWrapper()