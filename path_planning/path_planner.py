import sys
import cv2
import numpy as np
m_v = float("inf")

class path_planner(object):

    def __init__(self, map):

        self.map = map

        self.nodes = [[2, 1, 2], 
                      [m_v, m_v, m_v], 
                      [m_v, m_v, m_v], 
                      [m_v, m_v, m_v],
                      [m_v, m_v, m_v]]

        self.prevs = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.values = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.paths = [
                        [
                            [m_v, 2,   m_v],
                            [m_v, 1,   2  ],
                            [m_v, 2,   1  ]
                        ],
                        [
                            [m_v, m_v, m_v],
                            [2,   1,   2  ],
                            [m_v, 2,   1  ]
                        ],
                        [
                            [1,   m_v, m_v],
                            [2,   m_v, 2  ],
                            [m_v, m_v, 1  ]
                        ],
                        [
                            [1,   2,   m_v],
                            [m_v, m_v, m_v],
                            [m_v, 2,   m_v],
                        ]
                    ]
    
    def gen_buffer_mats(self):

        height = len(self.map)
        width = len(self.map[0])
        
        self.values = []
        for i in range(height):
            new_row = []
            for j in range(width):
                new_row.append(m_v)
            self.values.append(new_row)

        self.prevs = []
        for i in range(height):
            new_row = []
            for j in range(width):
                new_row.append(0)
            self.prevs.append(new_row)

    def gen_paths(self):

        paths = []
        height = len(self.map)
        width = len(self.map[0])
        for i in range(height - 1):
            # generate the matrxi from ith row to i+1throw
            cur_row = self.map[i]
            nxt_row = self.map[i+1]
            trans_mat = []
            for j in range(len(cur_row)):
                # generate path weights for each of nodes in this layer
                if (cur_row[j] == 1):
                    trans = [m_v] * width
                else:
                    trans = [0] * width
                    for k in range(len(nxt_row)):
                        # generate path weight to each of nodes in the next layer
                        if nxt_row[k] == 1:
                            trans[k] = m_v
                        else:
                            if k == j:
                                trans[k] = 1
                            elif (abs(k - j) == 1 and (cur_row[k] == 0 or nxt_row[j] == 0)):
                                trans[k] = 20
                            else:
                                trans[k] = m_v
                            # add obstacle avoiding weights
                            if (k < width -1):
                                if (nxt_row[k+1] == 1):
                                    trans[k] += 15
                            if (k > 0):
                                if (nxt_row[k-1] == 1):
                                    trans[k] += 15
                            if (i == height - 2): # check last row
                                continue
                            fur_row = self.map[i+2]
                            if (fur_row[k] == 1):
                                trans[k] += 50
                            if (k < width -1):
                                if (fur_row[k+1] == 1):
                                    trans[k] += 15
                            if (k > 0):
                                if (fur_row[k-1] == 1):
                                    trans[k] += 15
                trans_mat.append(trans.copy())
            paths.append(trans_mat)
        self.paths = paths

    def gen_nodes(self):

        nodes = []

        # Check if map is valid
        if len(self.map[1]) % 2 == 0:
            print("map in invalid shape!")
        width = len(self.map[1])
        center = int(int(width) / int(2)) 

        # Generate node representation from map
        for i, row in enumerate(self.map):

            new_row = [m_v] * width

            # Assign initial value to each node
            if (i == 0):
                for j, e in enumerate(row):
                    if e == 0:
                        if j == center:
                            new_row[j] = 1
                        elif (abs(j - center) == 1):
                            new_row[j] = 20
                        else:
                            new_row[j] = m_v
                    else:
                        new_row[j] = m_v
            
            nodes.append(new_row.copy())
        
        self.nodes = nodes


    def plan(self):
        
        # Transer into numpy array
        nodes = np.array(self.nodes)
        paths = np.array(self.paths)

        # Dynamic Programming
        finish = False
        while(not finish):
            
            # Extract min node
            min_index = np.unravel_index(np.argmin(nodes, axis=None), nodes.shape)
            layer = min_index[0]
            pos = min_index[1]
            val = nodes[layer][pos]
            
            # Loop though all outgoing archs
            if (layer != nodes.shape[0]-1):
                outs = paths[layer][pos]
                for i, out in enumerate(outs):
                    prev_v = self.values[layer+1][i]
                    curr_v = val + out
                    if (curr_v < prev_v):
                        nodes[layer+1][i] = curr_v
                        self.values[layer+1][i] = curr_v
                        self.prevs[layer+1][i] = pos

            # Save the optimal path length
            self.values[layer][pos] = nodes[layer][pos]
            nodes[layer][pos] = m_v

            # Check finish
            finish = True
            for row in nodes:
                for e in row:
                    if (e != m_v):
                        finish = False
                        break
        
            #print(nodes)
            #print(paths[layer])
            #input()

    def find_optimal_path(self, target):
        # find the optimal path
        
        # Target node
        t_layer = target[0]
        t_pos = target[1]

        opt_path = []
        opt_path.append(t_pos)
        for i in range(t_layer, 0, -1):
            if (i == t_layer):
                prev_pos =int(self.prevs[i][t_pos])
            else:
                prev_pos = int(self.prevs[i][prev_pos])
            opt_path.insert(0, prev_pos)
        return opt_path

    def find_default_target(self):
        # find the default target based on minimal distances
        height = np.array(self.values).shape[0]
        width = np.array(self.values).shape[1]

        center = int((width - 1) / 2)
        for i in range(height-1, 0, -1):
            if (self.values[i][center] != m_v):
                return [i, center]

        return None

    def check_target_valid(self, target):
        # check if the target is valid in current map
        return (not self.values[target[0]][target[1]] == m_v)

    def draw_path(self, path):

        unit_size = 60
        height = len(self.map)
        width = len(self.map[0])
        t_h = unit_size * height
        t_w = unit_size * width
        world = np.array([[[240] * 3] * (t_w)] * (t_h)).astype(np.uint8)

        for x in range(0, t_w, unit_size):
            pt1 = (x, 0)
            pt2 = (x, t_h)
            world = cv2.line(world, pt1, pt2, (255, 0, 0))
        
        for y in range(0, t_h, unit_size):
            pt1 = (0, y)
            pt2 = (t_w, y)
            world = cv2.line(world, pt1, pt2, (255, 0, 0))

        # Draw Obstacles
        ofs = int(unit_size / 5)
        for i, row in enumerate(self.map):
            for j, e in enumerate(row):
                if (e == 1):
                    # Draw an obstacle in world
                    pt1 = (j * unit_size + ofs, i * unit_size + ofs)
                    pt2 = ((j+1) * unit_size - ofs, (i+1) * unit_size - ofs)
                    cv2.rectangle(world, pt1, pt2, (0, 0, 255), 5)

        # Draw Optimal Path 
        x_ofs = int(unit_size / 2)
        y_ofs = int(unit_size / 2)
        for i in range(len(path)-1):
            
            f_p = path[i]
            t_p = path[i+1]

            pt1 = (f_p * unit_size + x_ofs, i * unit_size + y_ofs)
            pt2 = (t_p * unit_size + x_ofs, (i+1) * unit_size + y_ofs)

            world = cv2.line(world, pt1, pt2, (0, 255, 0), 5)

            if i == len(path) - 2:
                # draw target
                world = cv2.circle(world, pt2, int(unit_size / 3), (255, 0, 255), 10)

        world = np.flip(np.array(world), 0)
        cv2.imshow("path", world)

if __name__ == "__main__":
    default_map = [
            [0, 0, 1],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 1]
        ]

    big_map = [
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0]
    ]

    debug_map = [
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 1., 1., 0., 0., 0., 0.],
        [0., 0., 1., 1., 1., 0., 0., 0., 0.],
        [0., 0., 1., 1., 0., 0., 1., 0., 0.],
        [0., 1., 1., 1., 1., 1., 1., 0., 0.],
        [0., 1., 1., 1., 1., 1., 0., 0., 0.],
        [0., 1., 1., 1., 1., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.]
        ]
    p = path_planner(debug_map)

    p.gen_nodes()
    print(p.nodes)
    p.gen_paths()
    p.gen_buffer_mats()
    p.plan()
    target = p.find_default_target()
    if len(target) > 0:
        print(p.paths)
        print(p.values)
        print(p.prevs)
        path = p.find_optimal_path([3,4])
        p.draw_path(path)

        cv2.waitKey(0)
                      