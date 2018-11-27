import numpy as np

def inflate(grid, num_row, num_col, diag=False):
    #print (grid)
    inflate_grid = np.zeros((num_row, num_col))
    for i in range(num_row):
        for j in range(num_col):
            if (grid[i, j] > 0):
                if (i > 0 and j > 0) and (i < num_row-1 and j < num_col-1):
                    
                    inflate_grid[i-1,  j ] = 1
                    inflate_grid[ i,  j-1] = 1
                    inflate_grid[i+1,  j ] = 1
                    inflate_grid[ i,  j+1] = 1
                    inflate_grid[ i ,  j ] = 1

                    if diag:
                        inflate_grid[i-1, j+1] = 1
                        inflate_grid[i+1, j-1] = 1
                        inflate_grid[i+1, j+1] = 1
                        inflate_grid[i-1, j-1] = 1

    return inflate_grid