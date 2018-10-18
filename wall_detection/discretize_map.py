#Copyright Emily Stern emistern@bu.edu
#This file will import a numpy matrices and then discretize each matrix based on ranges of data.

#Import numpy array
import numpy as np


#Load in one depth data matrix
frame1_depth_data = np.load('./calibration/calibration_1.npy')

#the actual depth was about 28.3" to the cardboard box.


print(np.unique(frame1_depth_data))
print('size: ', frame1_depth_data.shape)
print(frame1_depth_data)

#find indices where != 0?



# Start with three ranges of data to look into

# Top left corner (350, 135), top right (702, 131), bottom left (376, 401), bottom right (693, 370)
print(frame1_depth_data[:,380])
print(frame1_depth_data[:,381])
print(frame1_depth_data[:,382])
print(frame1_depth_data[:,383])

# split thresholds based on an average person's gate. 
# values of around 630 - 720 represent around 28". 

# maybe get the scale depth data from Yu and then i can start to discretize the map?
# assuming the depth values scale linearly then i can just divide the values into individual step sizes.
# since the cardboard box was about 28.3 inches away and that has valuse from 630 - 715 can just assume that a
# step is the same as a depth value of 500?