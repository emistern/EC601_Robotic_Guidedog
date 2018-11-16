import numpy as np

def append_offset(points, row_size):

    points_row = points[:, 0] + abs(row_size/2) 
    points_col = points[:, 1] 

    return points_row, points_col

def compute_mask(row_num, col_num, row_size, col_size):

    mask_row = 1 / np.array(range(col_num))
    mask_row = mask_row * col_num / row_size

    mask_col = 1 / np.array(range(row_num))
    mask_col = mask_col * row_num / col_size

    return mask_row, mask_col

def decomp(points_row, points_col, row_num, col_num, mask_row, mask_col):

    grid = np.zeros((row_num, col_num))

    for i in range(0, len(points_col), 2):
        x_f = points_row[i]
        y_f = points_col[i]
        try:
            _x = x_f * mask_row
            x_i = np.max(np.where( _x > 1 ))
            _y = y_f * mask_col
            y_i = np.max(np.where( _y > 1 ))
        
            grid[y_i, x_i]  += 1
        except:
            pass

    return grid

def thresholding(grid, thresh=20):

    row_num = grid.shape[0]
    col_num = grid.shape[1]

    for i in range(row_num):
        for j in range(col_num):
            if (grid[i, j] > thresh):
                grid[i, j] = 1
            else:
                grid[i, j] = 0
    
    return grid

def decomposite(obstacle_points, center,
                row = 10, col = 7, 
                col_size = 5, row_size = 5,
                thresh = 20,  show = True):

    # decomposite points into grid
    grid = np.zeros((row, col))

    # some constants
    row_min = min(obstacle_points[:, 0])
    col_min = min(obstacle_points[:, 1])
    row_max = max(obstacle_points[:, 0])
    col_max = max(obstacle_points[:, 1])

    print("point cloud range from", row_min, " ", col_min, " to ", row_max, " ", col_max)

    points_row = obstacle_points[:, 0] + abs(row_size/2) + 0.0001
    points_col = obstacle_points[:, 1] + 0.0001

    if show:
        plt.scatter(points_row, points_col)
    
    row_min = min(points_row)
    col_min = min(points_col)
    row_max = max(points_row)
    col_max = max(points_col)

    print ("append offset")
    print("point cloud range from", row_min, " ", col_min, " to ", row_max, " ", col_max)

    w = row_max
    h = col_max

    mask_row = 1 / np.array(range(col))
    mask_row = mask_row * col / row_size

    mask_col = 1 / np.array(range(row))
    mask_col = mask_col * row / col_size

    print ("with row mask: ", mask_row)
    print ("with column mask: ", mask_col)

    st_time = time.time()
    # loop through the obstacle points
    for i in range(0, len(obstacle_points), 2):
        x_f = points_row[i]
        y_f = points_col[i]
        try:
            _x = x_f * mask_row
            x_i = np.max(np.where( _x > 1 ))
            _y = y_f * mask_col
            y_i = np.max(np.where( _y > 1 ))
        
            grid[y_i, x_i]  += 1
        except:
            pass
        #print(x_f, y_f)
        #print(x_i, y_i)
        #quit()
    print(grid)

    # find the target
    x_f = center[0] + abs(row_size/2)
    y_f = center[1]
    _x = x_f * mask_row
    x_i = np.max(np.where( _x > 1 ))
    _y = y_f * mask_col
    y_i = np.max(np.where( _y > 1 ))
    target = [y_i, x_i]

    grid[y_i, x_i] = 0

    for i in range(row):
        for j in range(col):
            if (grid[i, j] > thresh):
                grid[i, j] = 1
            else:
                grid[i, j] = 0
    ed_time = time.time()
    print("in ", ed_time - st_time, " second, the map: ")
    print(grid)
    if show:
        plt.show()

    return grid, target