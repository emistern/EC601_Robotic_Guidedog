import sys
import cv2
import numpy as np
import os
import time
m_v = float("inf")
class VoiceInterface(object):

  def __init__(self):
    self.straight_file= 'straight.mp3'
    self.turnleft_file= 'turnleft.mp3'
    self.turnright_file='turnright.mp3'
    self.hardleft_file='hardleft.mp3'
    self.hardright_file='hardright.mp3'
    self.STOP_file='STOP.mp3'
    self.noway_file='noway.mp3'

  def play(self, pat, width):
    b=10
    center=width/2-0.5
    if len(pat)==0:
        cmd = 'play' + ' ' + self.noway_file
        os.system(cmd)
        time.sleep(1)
        return
    path=[]
    path.append(pat[0]-center)
    for i in range (1,len(pat)):
        path.append(pat[i]-pat[i-1])
    print(path)
    for step in path:
        if step == 1 and step!=b:
            cmd = 'play' + ' ' + self.turnleft
            os.system(cmd)
        if step == 2 and step!=b:
            cmd = 'play' + ' ' + self.hardleft_file
            os.system(cmd)
        if step == -1 and step!=b:
            cmd = 'play' + ' ' + self.turnright_file
            os.system(cmd)
        if step == -2 and step!=b:
            cmd = 'play' + ' ' + self.hardright_file
            os.system(cmd)
        if step == 0 and step!=b:
            cmd = 'play' + ' ' + self.straight_file
            os.system(cmd)
        b=step
        time.sleep(1)
    cmd = 'play' + ' ' + self.STOP_file
    os.system(cmd)
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
                new_row.append(0)
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
            cur_row = self.map[i]
            nxt_row = self.map[i+1]
            trans_mat = []
            for j in range(len(cur_row)):
                if (cur_row[j] == 1):
                    trans = [m_v] * width
                else:
                    trans = [0] * width
                    for k in range(len(nxt_row)):
                        if nxt_row[k] == 1:
                            trans[k] = m_v
                        else:
                            if k == j:
                                trans[k] = 1
                            elif (abs(k - j) == 1):
                                trans[k] = 2
                            else:
                                trans[k] = m_v
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
                            new_row[j] = 2
                        else:
                            new_row[j] = m_v
                    else:
                        new_row[j] = m_v
            
            nodes.append(new_row.copy())
        
        self.nodes = nodes


    def plan(self, target):
        
        # Transer into numpy array
        nodes = np.array(self.nodes)
        paths = np.array(self.paths)

        # Target node
        t_layer = target[0]
        t_pos = target[1]

        # Check if the target node is valid
        if (t_layer >= nodes.shape[0] or t_pos >= nodes.shape[1] or self.map[t_layer][t_pos] ==1):
            print("Invalid target")
            return

        # Dynamic Programming
        while(m_v in nodes):
            
            # Extract min node
            min_index = np.unravel_index(np.argmin(nodes, axis=None), nodes.shape)
            layer = min_index[0]
            pos = min_index[1]
            val = nodes[layer][pos]
            
            # Loop though all outgoing archs
            if (layer != nodes.shape[0]-1):
                outs = paths[layer][pos]
                for i, out in enumerate(outs):
                    prev_v = nodes[layer+1][i]
                    curr_v = val + out
                    if (curr_v < prev_v):
                        nodes[layer+1][i] = curr_v
                        self.prevs[layer+1][i] = pos

            # Save the optimal path length
            self.values[layer][pos] = nodes[layer][pos]
            nodes[layer][pos] = m_v
            if (layer == t_layer and pos == t_pos):
                break
        
        # find the optimal path
        opt_path = []
        opt_path.append(t_pos)
        for i in range(t_layer, 0, -1):
            if (i == t_layer):
                prev_pos =int(self.prevs[i][t_pos])
            else:
                prev_pos = int(self.prevs[i][prev_pos])
            opt_path.insert(0, prev_pos)
        print (opt_path)
        return opt_path

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

        cv2.imshow("path", world)
        cv2.waitKey(0)

if __name__ == "__main__":
    default_map = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 0]
        ]

    big_map = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0]
    ]
    p = path_planner(big_map)

    p.gen_nodes()
    p.gen_paths()
    p.gen_buffer_mats()
    path = p.plan([4, 0])
    p.draw_path(path)
    interface = VoiceInterface()
    interface.play(path,5)
                      
