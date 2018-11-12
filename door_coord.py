import numpy as np
import math

def find_door( view_in_3D_after_filter, coord, slice_distance = 500, numsec = 7):

    # The input coord is in shape of[x_left,x_right,y_lower,y_upper]
    distance_array = view_in_3D_after_filter
    width = view_in_3D_after_filter.shape[0]

    # The output coord is in shape of [x_center,distance]
    ret_coor = [0,0]
    orig_x = int((coord[0][0] + coord[0][1])/2)
    h_cent = int((coord[0][2] + coord[0][3])/2)

    # Set up the leftmost and rightmost side of the distance detection
    #leftmost = coord[0][0]-int(0.2*(coord[0][1]-coord[0][0]))
    leftmost = coord[0][0] - 20
    if(leftmost < 0):
        leftmost = 0
    #rightmost = coord[0][1]+int(0.2*(coord[0][1]-coord[0][0]))
    rightmost = coord[0][1] + 20
    if(rightmost > distance_array.shape[0]-1):
        rightmost = distance_array.shape[0]-1

    # Set up the uppermost and lowermost side of the distance detection
    lowermost = h_cent - int(0.2*(coord[0][3]-coord[0][2]))
    if(lowermost < 0):
        lowermost = 0
    uppermost = h_cent + int(0.2*(coord[0][3]-coord[0][2]))
    if(uppermost > distance_array.shape[1]-1):
        uppermost = distance_array.shape[1]-1

    # Reset the distance in order to find the distance to the door
    distance = math.inf

    # Find the distance to the door
    for i in range (lowermost,uppermost):
        for j in range (leftmost,coord[0][0]):
            if(distance_array.item(i,j) < distance):
                if(distance_array.item(i,j) != 0):
                    distance = distance_array.item(i,j)

    for i in range (lowermost,uppermost):
        for j in range (coord[0][1],rightmost):
            if(distance_array.item(i,j) < distance):
                if(distance_array.item(i,j) != 0):
                    distance = distance_array.item(i,j)

    layer = int((distance-250)/slice_distance)
    ret_coor[1] = int((orig_x*numsec)/width)

    ret_coor[0] = layer
    if(ret_coor[0]>9):
        ret_coor[0]=9

    return ret_coor
