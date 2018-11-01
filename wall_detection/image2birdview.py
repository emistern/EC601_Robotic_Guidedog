import cv2
import numpy as np
from os import listdir
import sys
sys.path.append("./wall_detection/wall_detection")
from wall_detection import slicer
import squeeze
import math
import time

'''Put this py file in the same folder where slicer.py is saved
   Simply run the program
   Black = free space, white = obstacle
   You can imagine that the pictures are vertically squeezed
''' 

'''Configuration Constants. Assume the camera is parallel to the ground'''
# The maximum vertical angle (FOV) of realsense camera
VERTICAL_FOV = 58/180*math.pi

# Estimated distance between camera and ceiling/floor, used for removing the ceiling/floor area
# More area will be cut out if the value is lowered
TOP_THRESHOLD = 0.6
BOTTOM_THRESHOLD = 0.6

# Make a slice once every 0.5 meters
STEP_LENGTH = 0.5

# Minimum detection range of realsense camera
MINIMUM_RANGE = 0.25

# Ignore items which are smaller or equal to (5) pixel(s)
VERTICAL_SIZE_THRESHOLD = 5
HORIZONTAL_SIZE_THRESHOLD = 5

# Distances within which no ceiling or floor area needs to be removed
NO_CEIL = TOP_THRESHOLD/math.sin(VERTICAL_FOV/2)
NO_FLOOR = BOTTOM_THRESHOLD/math.sin(VERTICAL_FOV/2)

class depth_bird_view():

    def __init__(self, path = './'):
        self.path = path
        self.width = 320
        self.height = 240
      
    # Used to squeeze jpg files, currently abandoned because we are not saving jpg files locally
    def squeeze_jpg(self):
        filenames = listdir(self.path)
        image = np.empty([self.height, self.width])
        for filename in filenames:
            if filename.endswith(".jpg"):
                print("Processing "+filename)
                raw_jpg = cv2.imread(filename)
                image = np.asarray(raw_jpg)
                bw_image = np.mean(image, -1)/255.0
                self.show_image(bw_image)
                squeezed = np.empty([1, self.width])
                for x in range(self.width):
                    squeezed[0, x] = 1
                    for y in range(self.height):
                        if bw_image[y, x] < 0.1:
                            squeezed[0, x] = 0
                            break
                self.show_image(squeezed)
                print(squeezed)
            else:
                continue
                  
    # Squeeze a depth image (ndarray format), 10 128*72 pictures -> 128*10 birdview map
    def squeeze_matrix(self, depth_mat, num_slice=10, timing=True):
        t_start = time.time()
        #raw_matrix = slicer.slicer('wall_detection/depth0003.npy', self.width, self.height)
        #raw_matrix = squeeze.slicer('wall_detection/depth0003.npy', self.width, self.height, 10)
        raw_matrix = squeeze.slicer(depth_mat, self.width, self.height, num_slice)

        #squeezed_matrix = np.zeros([slicer.TOTAL_LAYER_NUMBER, self.width])
        squeezed_matrix = np.array([[]])
        for z in range(num_slice):
            t_loop_s = time.time()

            no_ceil_floor_nparray = self.remove_ceiling_floor(raw_matrix[:,:,z], z)
            t_loop_mid = time.time()

            #self.show_image(no_ceil_floor_nparray)
            """
            for x in range(self.width):
                pixel_count = 0
                column = no_ceil_floor_nparray[:, x]
                for y in range(self.height):
                    if column[y] > 0:
                        pixel_count += 1
                        if pixel_count > VERTICAL_SIZE_THRESHOLD:
                            squeezed_matrix[z, x] = 1
                            break
                    else:
                        pixel_count = 0
            """
            # Use c function to squeeze
            new_row = [0] * self.width
            new_row = squeeze.squeeze(z, self.height, self.width, 
                                             no_ceil_floor_nparray, 
                                             new_row,
                                             VERTICAL_SIZE_THRESHOLD)
            if z == 0:
                squeezed_matrix = np.array([new_row])
            else:
                squeezed_matrix = np.append(squeezed_matrix, [new_row], axis=0)
            print(squeezed_matrix.shape)
            t_loop_e = time.time()

            black_count = 0
            for x in range(self.width):
                if squeezed_matrix[z, x] == 1:
                    black_count += 1
                elif (black_count <= HORIZONTAL_SIZE_THRESHOLD and black_count > 0):
                    for i in range(black_count):
                        squeezed_matrix[z,x-i-1] = 0
                    black_count = 0
                else:
                    black_count = 0

            if timing:
                print("loop time: " + str(t_loop_e - t_loop_s))
                print("first half: " + str(t_loop_mid - t_loop_s))
                print("second half: " + str(t_loop_e - t_loop_mid))

        #birdmap = cv2.resize(squeezed_matrix,(self.width, 500), interpolation = cv2.INTER_LINEAR)
        #self.show_image(birdmap)
        return squeezed_matrix

    def remove_ceiling_floor(self, nparray, layer_number):
        no_ceil_floor_nparray = nparray
        distance = MINIMUM_RANGE+layer_number*STEP_LENGTH
        if distance > NO_CEIL:
            ceil_percent = (VERTICAL_FOV/2-math.asin(TOP_THRESHOLD/distance))/VERTICAL_FOV
            ceil_vrange = int(ceil_percent*self.height)
            for y in range(ceil_vrange):
                no_ceil_floor_nparray[y,:] = np.zeros(self.width)
        else:
            pass
        if distance > NO_FLOOR:
            floor_percent = (VERTICAL_FOV/2-math.asin(BOTTOM_THRESHOLD/distance))/VERTICAL_FOV
            floor_vrange = int(floor_percent*self.height)
            for y in range(floor_vrange):
                no_ceil_floor_nparray[self.height-1-y,:] = np.zeros(self.width)
        else:
            pass
        return no_ceil_floor_nparray

    def show_image(self, nparray):
        cv2.imshow("show", nparray)
        cv2.waitKey(20)
        input()

    def quantilize(self, sque_mat, n_sec=7, max_per_occ=0.3):

        # Quantilize the squeezed matrix into different sections

        # Check the given argument is valid
        assert max_per_occ <= 1.0

        # generate the bound of each section
        width = sque_mat.shape[1]
        bounds = np.array(range(n_sec + 1)) / n_sec * width

        # generate quantilized map
        quant_map = []
        for row in sque_mat:
            new_row = [0] * n_sec
            for i in range(len(bounds) - 1):
                head = int(bounds[i])
                tail = int(bounds[i+1])
                sec = row[head:tail]

                count = 0
                for e in sec:
                    if (e == 1):
                        count += 1
                per_occ = count / len(bounds)
                if (per_occ > max_per_occ):
                    new_row[i] = 1
            quant_map.append(new_row.copy())
        return np.array(quant_map)

def main():
    squeeze = depth_bird_view()
    squeezed_matrix = squeeze.squeeze_matrix()
    quntilized_matrix = squeeze.quantilize(squeezed_matrix)
    #print(quntilized_matrix)
    #squeeze.show_image(squeezed_matrix)

    #squeeze.squeeze_jpg()
if __name__ == "__main__":
    main()
