import numpy as np

def find_door( view_in_3D, coord, slice_distance = 500, numsec = 7):

    # The input coord is in shape of[x_left,x_right,y_lower,y_upper]
    distance_array = view_in_3D
    print("the [0] is ",distance_array.shape[0])
    print("the [1] is ",distance_array.shape[1])
    width = view_in_3D.shape[1]
    print('coord is ',coord)

    # The output coord is in shape of [x_center,distance]
    ret_coor = [0,0]

    dist_min = 2000000
    for door_coord in coord:
        orig_x = int((door_coord[0] + door_coord[1])/2)
        h_cent = int((door_coord[2] + door_coord[3])/2)

        '''
        Below is for the goal detection of solid mono.
        '''

        # Find out the range of the points we wants to go through
        leftmost = door_coord[0]
        if(leftmost < 0):
            leftmost = 0
        rightmost = door_coord[1]
        if(rightmost > distance_array.shape[1]-1):
            rightmost = distance_array.shape[1]-1

        # Set up the uppermost and lowermost side of the distance detection
        lowermost = door_coord[2]
        if(lowermost < 0):
            lowermost = 0
        #uppermost = coord[0][3]
        #if(uppermost > distance_array.shape[0]-1):
            #uppermost = distance_array.shape[0]-1

        distance = 2000000

        for i in range (lowermost,h_cent):
            for j in range (leftmost,rightmost):
                if(distance_array.item(i,j) < distance):
                    if(distance_array.item(i,j) != 0):
                        distance = distance_array.item(i,j)

        if(distance < dist_min):
            dist_min = distance
            orig_x_min = orig_x
            h_cent_min = h_cent
            coord_print = door_coord

    layer = int((dist_min-250)/slice_distance)

    ret_coor[1] = int((orig_x_min * numsec)/width)

    ret_coor[0] = layer

    return ret_coor, coord_print

def find_door_pointcloud( view_in_3D, coord):

    # The input coord is in shape of[x_left,x_right,y_lower,y_upper]
    distance_array = view_in_3D
    width = view_in_3D.shape[1]

    # The output coord is in shape of [x_center,distance,height]
    ret_coor = [0,0,0]
    dist_min = 2000000
    for door_coord in coord:
        orig_x = int((door_coord[0] + door_coord[1])/2)
        h_cent = int((door_coord[2] + door_coord[3])/2)

        '''
        Below is for the goal detection of solid objects.
        '''

        # Find out the range of the points we wants to go through
        leftmost = door_coord[0]
        if(leftmost < 0):
            leftmost = 0
        rightmost = door_coord[1]
        if(rightmost > distance_array.shape[1]-1):
            rightmost = distance_array.shape[1]-1

        # Set up the uppermost and lowermost side of the distance detection
        lowermost = door_coord[2]
        if(lowermost < 0):
            lowermost = 0
        #uppermost = coord[0][3]
        #if(uppermost > distance_array.shape[0]-1):
            #uppermost = distance_array.shape[0]-1

        distance = 2000000

        # Find the distance to the chair and the ground where the chair stands on.
        for i in range (lowermost,h_cent):
            for j in range (leftmost,rightmost):
                if(distance_array.item(i,j) < distance):
                    if(distance_array.item(i,j) != 0):
                        distance = distance_array.item(i,j)
        if(distance<dist_min):
            orig_x_min = orig_x
            h_cent_min = h_cent
            dist_min = distance
            coord_print = door_coord
    
    ret_coor[0] = orig_x_min

    ret_coor[2] = h_cent_min

    ret_coor[1] = dist_min

    return ret_coor , coord_print
