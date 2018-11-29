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

import pandas as pd
import matplotlib.pyplot as plt


# evenly sampled time at 200ms intervals
x = range(0, 5, 1)

# Read in Data
df = pd.read_csv("results_1129.csv")


# red dashes, blue squares and green triangles
plt.figure(1)
plt.plot(x, 100*df['Open Time']/df['Open Time DJK'], 'ro', label='Open Space')
plt.plot(x, 100*df['Hallway TIme']/df['Hallway TIme DJK'], 'bs', label='Hallway')
plt.plot(x, 100*df['Sparse Time']/df['Sparse Time DJK'], 'g^', label='Sparse Obstacles')
plt.plot(x, 100*df['Dense Time']/df['Dense Time DJK'], 'c*', label='Dense Obstacles')
plt.legend()
plt.xlabel('Scale')
plt.xticks(x, ['Super Coarse', 'Coarse', 'Average', 'Fine', 'Super Fine'])
plt.ylabel('A*/Dijkstra (%)')


## Individual Timed Plots



plt.figure(2)
plt.plot(x, df['Open Time'], 'bo', label='Open A*')
plt.plot(x, df['Hallway TIme'], 'bx', label='Hallway A*')
plt.plot(x, df['Sparse Time'], 'b^', label='Sparse Obstacles A*')
plt.plot(x, df['Dense Time'], 'b*', label='Dense Obstacles A*')
plt.plot(x, df['Open Time DJK'], 'go', label='Open Dijkstra')
plt.plot(x, df['Hallway TIme DJK'], 'gx', label='Hallway Dijkstra')
plt.plot(x, df['Sparse Time DJK'], 'g^', label='Sparse Dijkstra')
plt.plot(x, df['Dense Time DJK'], 'g*', label='Dense Dijkstra')
# Color Differences
# first_legend =plt.legend(handles=['Open A*', 'Hallway A*', 'Sparse Obstacles A*', 'Dense Obstacles A'])
# second_legend = plt.legend(handles=['Open Dijkstra', 'Hallway Dijkstra', 'Sparse Dijkstra', 'Dense Dijkstra'])
plt.legend()
plt.xlabel('Scale')
plt.xticks(x, ['Super Coarse', 'Coarse', 'Average', 'Fine', 'Super Fine'])
plt.ylabel('Planning Time (s)')


########### BAR GRAPH #############
 
# data to plot
# n_groups = 4
# means_astar = (0.0933, 0.0574, 0.0378, .02)
# means_dijkstra = (0.2828, 0.2343, 0.1357, .09)
 
# # create plot

# fig, ax = plt.subplots()
# index = np.arange(n_groups)
# bar_width = 0.35
# opacity = 0.8


# rects1 = plt.bar(index, means_astar, bar_width,
#                  alpha=opacity,
#                  color='b',
#                  label='A*')
 
# rects2 = plt.bar(index + bar_width, means_dijkstra, bar_width,
#                  alpha=opacity,
#                  color='g',
#                  label='Dijkstra')
 
# # plt.xlabel('Path Planner')
# plt.ylabel('Time (seconds)')
# plt.title('Time for Path by Planner')
# plt.xticks(index + bar_width/2, ('Open Space', 'Hallway', 'Sparse Obstacles', 'Dense Obstacles'))
# plt.legend()
 
# plt.tight_layout()
plt.show()
