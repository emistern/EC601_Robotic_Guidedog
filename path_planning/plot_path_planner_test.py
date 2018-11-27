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

# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', label='Open Space')
plt.plot(t, t**2, 'bs', label='Hallway')
plt.plot(t, t**3, 'g^', label='Sparse Obstacles')
plt.plot(t, t**4, 'c*', label='Dense Obstacles')
plt.legend()
plt.xlabel('Scale')
plt.ylabel('Dijkstra/A* (%)')

########### BAR GRAPH #############
 
# data to plot
n_groups = 4
means_frank = (90, 55, 40, 65)
means_guido = (85, 62, 54, 20)
 
# create plot

fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8


rects1 = plt.bar(index, means_frank, bar_width,
                 alpha=opacity,
                 color='b',
                 label='A*')
 
rects2 = plt.bar(index + bar_width, means_guido, bar_width,
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
