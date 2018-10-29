import numpy as np
import cv2
'''
Take one frame of depth image and slice it into pieces, return a 3-d matrix [y,x,layer]
'''
#.np file addr

file_name = 'wall_detection/depth0003.npy'
WIDTH = 640
HEIGHT = 360
TOTAL_LAYER_NUMBER = 10
def slicer_bak():
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


def slicer(fn, WIDTH, HEIGHT):
    a = np.load(fn)
    #print(a.shape)
    w = int(a.shape[1])
    h = int(a.shape[0])
    step_w = w / WIDTH
    step_h = h / HEIGHT
    #print(step_w, step_h)
    b = np.zeros((HEIGHT,WIDTH,TOTAL_LAYER_NUMBER))

    #for x, i in enumerate(range(0, h, step_h)):
    #    for y, j in enumerate(range(0, w, step_w)):
    p_w = 0
    p_h = 0
    x = y = 0
    while(int(p_h) < h and x < HEIGHT):
        p_w = 0
        y = 0
        while(int(p_w) < w and y < WIDTH):
            i = int(p_h)
            j = int(p_w)
            #print(x, y)
            if(a.item(i,j)!=0):
                if(a.item(i,j)<TOTAL_LAYER_NUMBER*500+250):
                    c = int((a.item(i,j)-250)/500)
                    a[i,j] = 0
                    b[x,y,c] = 1
                    #print ('*')
            p_w += step_w
            y += 1
        p_h += step_h
        x += 1
        #print(b)
    return b

    for k in range (TOTAL_LAYER_NUMBER):
        cv2.imshow("Verify", b[:,:,k])
        cv2.waitKey(20)
        input()

if __name__ == "__main__":
    print(slicer('depth0003.npy'))

