#Copyright Emily Stern emistern@bu.edu
#This file will import a numpy matrices and then discretize each matrix based on ranges of data.

#Import numpy array
import numpy as np


#Load in one depth data matrix
frame1_depth_data = np.load('depth0000.npy')


print(np.unique(frame1_depth_data))

# Potentially real sense library could show us what the conversion is between actual distance
# the values in the depth matrix. 

# Start with three ranges of data to look into
