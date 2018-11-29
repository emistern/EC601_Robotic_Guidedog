# This program will plot the timed results for 
# both A* and Dijkstra path planners for pre-recorded
# videos.

# Recorded approciamtely 10 second long videos. Videos will run on repeat until the wrapper
# has gone through 200 frames. 


# Hallway
# Scale 26 rows x 39 columns (Avg Scale)
# A Star 
# Planning Time Avg: 0.1695 seconds Std Dev 0.0349
# Dijkstra

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# evenly sampled time at 200ms intervals
x = np.arange(0., 5., 1)
#super fine -> coarse
astar_hallway = [0.0083, 0.0108, 0.0378, 0.0574, 0.0933]
dijkstra_hallway  = [0.015, 0.0208, 0.1357, 0.2343,0.2828]
astar_sparse = [0.0097, 0.0202, 0.0352, 0.069, 0.1303]
dijkstra_sparse = [0.0115, 0.0514, 0.0762, 0.2214, 0.4565]
astar_dense = [0.0076, 0.0165, 0.0368, 0.0683,0.0944]
dijkstra_dense = [0.0152, 0.0486, 0.118, 0.2127, 0.4231]

# red dashes, blue squares and green triangles
plt.figure(1)
plt.plot(x, [.2, .2, .2, .2, .2], 'r--', label='Open Space')
plt.plot(x, [100*astar/dijk for astar,dijk in zip(astar_hallway,dijkstra_hallway)], 'bs', label='Hallway')
plt.plot(x, [100*astar/dijk for astar,dijk in zip(astar_sparse,dijkstra_sparse)], 'g^', label='Sparse Obstacles')
plt.plot(x, [100*astar/dijk for astar,dijk in zip(astar_dense,dijkstra_dense)], 'c*', label='Dense Obstacles')
plt.legend()
plt.xlabel('Scale')
plt.xticks(x, ['Super Coarse', 'Coarse', 'Average', 'Fine', 'Super Fine'])
plt.ylabel('A*/Dijkstra (%)')


## Individual Timed Plots



plt.figure(2)
plt.plot(x, [.2, .2, .2, .2, .2], 'b--', label='Open Space A')
plt.plot(x, astar_hallway, 'bs', label='Hallway A')
plt.plot(x, astar_sparse, 'b^', label='Sparse Obstacles A')
plt.plot(x, astar_dense, 'b*', label='Dense Obstacles A')
plt.plot(x, [.2, .2, .2, .2, .2], 'g--', label='Open Space D')
plt.plot(x, dijkstra_hallway, 'gs', label='Hallway D')
plt.plot(x, dijkstra_sparse, 'g^', label='Sparse Obstacles D')
plt.plot(x, dijkstra_dense, 'g*', label='Dense Obstacles D')
blue_patch = mpatches.Patch(color='blue', label='A*')
green_patch = mpatches.Patch(color='green', label='Dijkstra')
plt.legend(handles=[blue_patch, green_patch])
plt.xlabel('Scale')
plt.xticks(x, ['Super Coarse', 'Coarse', 'Average', 'Fine', 'Super Fine'])
plt.ylabel('Planning Time (s)')
########### BAR GRAPH #############
 
# data to plot
n_groups = 4
means_astar = (0.0933, 0.0574, 0.0378, .02)
means_dijkstra = (0.2828, 0.2343, 0.1357, .09)
 
# create plot

fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8


rects1 = plt.bar(index, means_astar, bar_width,
                 alpha=opacity,
                 color='b',
                 label='A*')
 
rects2 = plt.bar(index + bar_width, means_dijkstra, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Dijkstra')
 
# plt.xlabel('Path Planner')
plt.ylabel('Time (seconds)')
plt.title('Time for Path by Planner')
plt.xticks(index + bar_width/2, ('Open Space', 'Hallway', 'Sparse Obstacles', 'Dense Obstacles'))
plt.legend()
 
plt.tight_layout()
plt.show()
