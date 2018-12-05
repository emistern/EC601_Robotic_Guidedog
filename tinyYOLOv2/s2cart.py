import numpy as np

def sphere2cart(x, y, z, map_len, map_width, x_max, y_max, pcmap, hfov = 69.4, vfov = 42.5, resolution_x = 1280, resolution_z = 720):
    origin_x = (map_width+1)/2
    xc = y/1000*np.cos((resolution_z/2-z)*vfov/resolution_z*np.pi/180)*np.sin((x-resolution_x/2)*hfov/resolution_x*np.pi/180)
    # print("xc is: "+str(xc))
    yc = y/1000*np.cos((resolution_z/2-z)*vfov/resolution_z*np.pi/180)
    #zc = y/1000*np.cos((resolution_x/2-x)*hfov/resolution_x*np.pi/180)*np.cos((resolution_z/2-z)*vfov/resolution_z*np.pi/180)
    xm = int((xc/x_max+0.5)*map_width)+1
    ym = int(yc/y_max*map_len)-2
    if ym > map_len-1:
        ym = map_len-1
    angle = (xm-origin_x)/ym
    if angle <= 1 and angle >= -1:
        while pcmap[ym][int(xm)]:
            ym -= 1
            xm -= angle
    else:
        while pcmap[int(ym)][xm]:
            xm -= 1
            ym -= 1/angle
    xm = int(xm)
    ym = int(ym)
    print("xm is: "+str(xm))
    print("ym is: "+str(ym))
    return ym, xm
'''
def sphere2map(x, y, hfov = 69.4, vfov = 42.5, resolution_x = 1280, resolution_z = 720):
    x = x/1000
    y = y/1000
    y_max = 6
    x_map = -10000
    y_map = y_map_n
    x_map_n = 11
    y_map_n = 14
    if y <= y_map_n:
        y_map = round(y/y_max*y_map_n)
    avail_width = np.tan(hfov/2*np.pi/180)*y_map
    if x >= -1*avail_width and x <= avail_width:
        x_map = int((x/(2*avail_width)*x_map_n))
    return x_map, y_map
    '''

if __name__ == '__main__':
    print(sphere2cart(0, 12500, 0, 14, 11, 10, 13))
