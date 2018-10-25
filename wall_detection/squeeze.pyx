import numpy as np

def squeeze(z, height, width, no_ceil_floor_nparray, squeezed_matrix, VERTICAL_SIZE_THRESHOLD):
    
    for x in range(width):
        pixel_count = 0
        column = no_ceil_floor_nparray[:, x]
        for y in range(height):
            if column[y] > 0:
                pixel_count += 1
                if pixel_count > VERTICAL_SIZE_THRESHOLD:
                    squeezed_matrix[x] = 1
                    break
            else:
                pixel_count = 0
    return squeezed_matrix

def slicer(fn, WIDTH, HEIGHT, TOTAL_LAYER_NUMBER):
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