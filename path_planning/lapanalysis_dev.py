import numpy as np
import time

def compute_adjacency_degree(grid_map):

    map_np = np.array(grid_map)
    map_shape = map_np.shape
    height = map_shape[0] 
    width = map_shape[1]

    adj_size = height * width
    adj_mtx = np.zeros((adj_size, adj_size))
    dgr_mtx = np.zeros((adj_size, adj_size))

    free_sqr = []

    for i in range(height):
        for j in range(width):
            if (map_np[i, j] == 0):
                if (i < height - 1):
                    if (map_np[i+1, j] == 0):
                        adj_mtx[i*width+j, (i+1)*width+j] = 1
                        adj_mtx[(i+1)*width+j, i*width+j] = 1
                        dgr_mtx[i*width+j, i*width+j] += 1
                        dgr_mtx[(i+1)*width+j, (i+1)*width+j] += 1
                    if (j > 0):
                        if (map_np[i+1, j-1] == 0):
                            adj_mtx[i*width+j, (i+1)*width+j-1] = 1
                            adj_mtx[(i+1)*width+j-1, i*width+j] = 1
                            dgr_mtx[i*width+j, i*width+j] += 1
                            dgr_mtx[(i+1)*width+j-1, (i+1)*width+j-1] += 1
                    if (j < width - 1):
                        if (map_np[i+1, j+1] == 0):
                            adj_mtx[i*width+j, (i+1)*width+j+1] = 1
                            adj_mtx[(i+1)*width+j+1, i*width+j] = 1
                            dgr_mtx[i*width+j, i*width+j] += 1
                            dgr_mtx[(i+1)*width+j+1, (i+1)*width+j+1] += 1
    for i in range(adj_size):
        # if dgr_mtx[i, i] > 0:
        _i = int(i / width)
        _j = i - _i * width
        if (map_np[_i, _j] == 0):
            free_sqr.append(i)             

    free_sqr = np.array(free_sqr)

    adj_mtx = np.take(adj_mtx, free_sqr, axis=0)
    adj_mtx = np.take(adj_mtx, free_sqr, axis=1)

    dgr_mtx = np.take(dgr_mtx, free_sqr, axis=0)
    dgr_mtx = np.take(dgr_mtx, free_sqr, axis=1)

    return adj_mtx, dgr_mtx

def compute_laplacian(adj_mtx, dgr_mtx):

    graph_lap = dgr_mtx - adj_mtx

    return graph_lap

def compute_eig(lap):

    eig_vals = np.linalg.eigvals(lap)

    print(np.sort(eig_vals))

if __name__ == "__main__":

    debug_map = [
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 1., 0., 0., 0., 0., 0.],
        [0., 0., 1., 1., 0., 0., 0., 0., 0.],
        [0., 0., 1., 0., 0., 0., 1., 0., 0.],
        [0., 1., 1., 0., 0., 1., 1., 0., 0.],
        [0., 1., 1., 0., 0., 1., 0., 0., 0.],
        [0., 1., 1., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 1., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.]
        ]

    big_map = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0]]

    sml_map = [
        [0, 0, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]

    st = time.time()
    adj, dgr = compute_adjacency_degree(big_map)

    lap = compute_laplacian(adj, dgr)

    compute_eig(lap)
    ed = time.time()
    print("in time: ", ed-st)