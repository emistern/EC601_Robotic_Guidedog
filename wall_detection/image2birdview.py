import cv2
import numpy as np
from os import listdir
import slicer
import math

'''Put this py file in the same folder where 1280*960 jpg files (fake data) are saved
   Simply run the program
   The white pieces of the line are the places without obstacles. 
   You can imagine that the pictures are vertically squeezed''' 
VERTICAL_FOV = 58/180*math.pi
TOP_THRESHOLD = 0.6
BOTTOM_THRESHOLD = 0.6
NO_CEIL = TOP_THRESHOLD/math.sin(VERTICAL_FOV/2)
NO_FLOOR = BOTTOM_THRESHOLD/math.sin(VERTICAL_FOV/2)

class depth_bird_view():

    def __init__(self, path = './', img_width = 1280, img_height = 720):
        self.path = path
        self.width = 1280
        self.height = 720

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

    def squeeze_matrix(self):
        raw_matrix = slicer.slicer()
        squeezed_matrix = np.ones([slicer.TOTAL_LAYER_NUMBER, self.width])
        for z in range(slicer.TOTAL_LAYER_NUMBER):
            no_ceil_floor_nparray = self.remove_ceiling_floor(raw_matrix[:,:,z], z)
            #self.show_image(no_ceil_floor_nparray)
            for x in range(self.width):
                for y in range(self.height):
                    if no_ceil_floor_nparray[y, x] > 0:
                        squeezed_matrix[slicer.TOTAL_LAYER_NUMBER-1-z, x] = 0
                        break
        self.show_image(squeezed_matrix)

    def remove_ceiling_floor(self, nparray, layer_number):
        no_ceil_floor_nparray = nparray
        distance = 0.25+layer_number*0.5
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

def main():
    squeeze = depth_bird_view()
    squeeze.squeeze_matrix()
    #squeeze.squeeze_jpg()
if __name__ == "__main__":
    main()
