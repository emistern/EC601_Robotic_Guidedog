import cv2
import numpy as np

def draw_max_conn(grid, idx, lines=False):

    unit_size = 10
    height = len(grid)
    width = len(grid[0])
    t_h = unit_size * height
    t_w = unit_size * width
    world = np.array([[[240] * 3] * (t_w)] * (t_h)).astype(np.uint8)

    if lines:
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
    for i, row in enumerate(grid):
        for j, e in enumerate(row):
            if (e == 1):
                # Draw an obstacle in world
                pt1 = (j * unit_size + ofs, i * unit_size + ofs)
                pt2 = ((j+1) * unit_size - ofs, (i+1) * unit_size - ofs)
                cv2.rectangle(world, pt1, pt2, (0, 0, 200), 3)

    sqr_dict = {}
    count = 0
    for i in range(height):
        for j in range(width):
            if (grid[i][j] == 0):
                sqr_dict[count] = (i, j)
                count += 1
    # Draw connected compoment
    for i in range(len(idx)):
        _id = idx[i]
        _j = sqr_dict[_id][1]
        _i = sqr_dict[_id][0]
        pt1 = (_j * unit_size + ofs, _i * unit_size + ofs)
        pt2 = ((_j+1) * unit_size - ofs, (_i+1) * unit_size - ofs)
        cv2.rectangle(world, pt1, pt2, (200, 0, 0), 3)
    
    world = np.flip(np.array(world), 0)
    #cv2.imshow("path", world)
    return world