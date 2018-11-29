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
    orig_x = int((coord[0] + coord[1])/2)
    h_cent = int((coord[2] + coord[3])/2)

    '''
    Below is for the goal detection of solid mono.
    '''

    # Find out the range of the points we wants to go through
    leftmost = coord[0]
    if(leftmost < 0):
        leftmost = 0
    rightmost = coord[1]
    if(rightmost > distance_array.shape[1]-1):
        rightmost = distance_array.shape[1]-1

    # Set up the uppermost and lowermost side of the distance detection
    lowermost = coord[2]
    if(lowermost < 0):
        lowermost = 0
    #uppermost = coord[0][3]
    #if(uppermost > distance_array.shape[0]-1):
        #uppermost = distance_array.shape[0]-1

    n = 0
    '''
    distance = 0

    # Find the distance to the chair and the ground where the chair stands on.
    for i in range (lowermost,h_cent):
        for j in range (leftmost,rightmost):
            if(distance_array.item(i,j) != 0):
                n = n + 1
                distance = distance + distance_array.item(i,j)    

    distance = distance / n
    '''

    distance = 20000

    # Find the distance to the chair and the ground where the chair stands on.
    for i in range (lowermost,h_cent):
        for j in range (leftmost,rightmost):
            if(distance_array.item(i,j) < distance):
                if(distance_array.item(i,j) != 0):
                    print("It's in the IF.")
                    distance = distance_array.item(i,j)

    layer = int((distance-250)/slice_distance)
    print('distance ',distance,' in ',layer)
    ret_coor[1] = int((orig_x*numsec)/width)

    ret_coor[0] = layer

    '''
    Below is for detecting the hollow goal, such as an opened door.
    '''


    '''
    # Reset the distance in order to find the distance to the door
    distance = math.inf

    # Set up the leftmost and rightmost side of the distance detection
    #leftmost = coord[0][0]-int(0.2*(coord[0][1]-coord[0][0]))
    leftmost = coord[0][0] - 20
    if(leftmost < 0):
        leftmost = 0
    #rightmost = coord[0][1]+int(0.2*(coord[0][1]-coord[0][0]))
    rightmost = coord[0][1] + 20
    if(rightmost > distance_array.shape[1]-1):
        rightmost = distance_array.shape[1]-1

    # Set up the uppermost and lowermost side of the distance detection
    lowermost = h_cent - int(0.2*(coord[0][3]-coord[0][2]))
    if(lowermost < 0):
        lowermost = 0
    uppermost = h_cent + int(0.2*(coord[0][3]-coord[0][2]))
    if(uppermost > distance_array.shape[0]-1):
        uppermost = distance_array.shape[0]-1
        
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
    print(ret_coor)
    '''
    return ret_coor
