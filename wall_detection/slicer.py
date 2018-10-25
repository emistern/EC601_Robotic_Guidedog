import numpy as np
import cv2
'''
Take one frame of depth image and slice it into pieces, return a 3-d matrix [y,x,layer]
'''
#.np file addr
file_name = './depth0003.npy'
WIDTH = 1280
HEIGHT = 720
TOTAL_LAYER_NUMBER = 10
def slicer():
    a = np.load(file_name)

    b = np.zeros((HEIGHT,WIDTH,TOTAL_LAYER_NUMBER))

    for i in range (HEIGHT):
        for j in range (WIDTH):
            if(a.item(i,j)!=0):
                if(a.item(i,j)<TOTAL_LAYER_NUMBER*500+250):
                    c = int((a.item(i,j)-250)/500)
                    a[i,j] = 0
                    b[i,j,c] = 1
    return b
'''
    for k in range (TOTAL_LAYER_NUMBER):
        cv2.imshow("Verify", b[:,:,k])
        cv2.waitKey(20)
        input()
'''