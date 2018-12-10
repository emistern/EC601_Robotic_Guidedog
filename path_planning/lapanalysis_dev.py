import numpy as np
import time
from draw import draw_max_conn
import cv2

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

def reorder_laplacian(lap):

    # reorder the graph laplacian
    diag_blocks = [[0, 1, 2]]

    mtx_size = lap.shape[0]

    for i in range(1, mtx_size):
        # loop through all the nodes
        if (lap[i, i] == 0):
            # a node with degree 0
            diag_blocks.append([i])
        else:
            in_block = False
            for j in range(i):
                # loop through possible connections
                for k, block in enumerate(diag_blocks):
                    if (lap[j, i] == -1) and (j in block) and (i not in block):
                        block.append(i)
                        diag_blocks[k] = block
                        in_block = True
                        break
                #if (in_block):
                #    break
            if (not in_block):
                diag_blocks.append([i])

    return diag_blocks

def pick_laplacian(lap, idx):
    print(idx)
    pick_idx = np.array(idx[0])

    pick_lap = np.take(lap, pick_idx, axis=0)
    pick_lap = np.take(pick_lap, pick_idx, axis=1)

    for i in range(pick_lap.shape[0]):
        #print(np.sum(pick_lap[i], axis=0))
        pick_lap[i, i] -= np.sum(pick_lap[i], axis=0)

    return pick_lap

if __name__ == "__main__":

    debug_map = [
        [1., 1., 1., 0., 0., 0., 1., 1., 1.],
        [0., 0., 1., 1., 0., 0., 0., 0., 0.],
        [0., 0., 1., 1., 0., 0., 0., 0., 0.],
        [0., 0., 1., 0., 0., 0., 1., 0., 0.],
        [0., 1., 1., 0., 0., 1., 1., 0., 0.],
        [0., 1., 1., 0., 0., 1., 0., 0., 0.],
        [0., 1., 1., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 1., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [1., 1., 1., 1., 1., 1., 1., 1., 1.],
        [0., 0., 0., 0., 0., 0., 1., 0., 0.],
        [0., 0., 0., 0., 0., 0., 1., 0., 0.]
        ]

    big_map = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]]

    sml_map = [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]

    test_map = debug_map

    st = time.time()
    adj, dgr = compute_adjacency_degree(test_map)

    lap = compute_laplacian(adj, dgr)

    diag_idx = reorder_laplacian(lap)

    sml_lap = pick_laplacian(lap, diag_idx)

    print(sml_lap)
    #compute_eig(sml_lap)
    ed = time.time()
    print("in time: ", ed-st)

    world = draw_max_conn(test_map, diag_idx[0])
    cv2.imshow("max conn", world)
    cv2.waitKey(0)