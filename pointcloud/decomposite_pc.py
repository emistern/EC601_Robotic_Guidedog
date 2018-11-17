import numpy as np

def append_offset(points, row_size, col_size):

    points[:, 0] += abs(row_size/2) 
    inlier_row_idx = np.where((points[:, 0] > 0) & (points[:, 0] < row_size))
    points = np.squeeze(np.take(points, inlier_row_idx, axis=0))
    inlier_col_idx = np.where((points[:, 1] > 0) & (points[:, 1] < col_size))
    points = np.squeeze(np.take(points, inlier_col_idx, axis=0))
    pts_row = points[:, 0]
    pts_col = points[:, 1]

    return pts_row, pts_col

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

def thresholding(grid, thresh=10):

    row_num = grid.shape[0]
    col_num = grid.shape[1]

    for i in range(row_num):
        for j in range(col_num):
            if (grid[i, j] > thresh):
                grid[i, j] = 1
            else:
                grid[i, j] = 0
    
    return grid

def append_offset2D(points, row_size):

    points[:, 0] = points[:, 0] + abs(row_size/2) 

    return points

def compute_mask2D(row_num, col_num, row_size, col_size):

    return

def select_points(pts_row, pts_col, row_size, col_size):

    return

def decomp_np(points_row, points_col, row_num, col_num, mask_row, mask_col):

    grid = np.zeros((row_num, col_num))
    mask_row = np.array(mask_row)
    points_row = np.array(points_row)
    mask_col = np.array(mask_col)
    points_col = np.array(points_col) + 0.01

    outer_row = np.matmul(np.expand_dims(points_row, axis=1), 
                      np.expand_dims(mask_row, axis=0))
    outer_col = np.matmul(np.expand_dims(points_col, axis=1), 
                      np.expand_dims(mask_col, axis=0))

    id_p_row, id_m_row = np.where((outer_row > 1))
    id_p_col, id_m_col = np.where((outer_col > 1))
    
    idx_row = []
    for i in range(len(id_p_row)):
        if(i == len(id_p_row) - 1):
            idx_row.append(i)
        elif(id_p_row[i+1] > id_p_row[i]):
            idx_row.append(i)
    idx_row = np.array(idx_row, dtype=np.int32)
    cor_row = np.take(id_m_row, idx_row)

    idx_col = []
    for i in range(len(id_p_col)):
        if(i == len(id_p_col) - 1):
            idx_col.append(i)
        elif(id_p_col[i+1] > id_p_col[i]):
            idx_col.append(i)
    idx_col = np.array(idx_col, dtype=np.int32)
    cor_col = np.take(id_m_col, idx_col)

    assert len(cor_col) == len(cor_row)

    for i in range(len(cor_row)):
        grid[cor_col[i], cor_row[i]] += 1

    return grid