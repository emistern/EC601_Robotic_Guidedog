# Path Planner with A* algorith

#######################################################
#################### Assumptions ######################
#######################################################

# - the starting position is the center position of the map, one layer above.
# - the first step the person can take is directly in front of them or
#	the diagonal in front of them 
# - the first row of the list is the first step someone will take.
# - 0 in a map represents free space
# - 1 in a map represents an obstacle
# - User can more straight, diagonal left, or diagonal right 
# - in the path planner, the cost given to a 
#	straight motion is 1 and the cost given to diagonal motions is 2
# - if there is no path available, the planner will return []
# - the planner also needs to return the size of the map (just width)

#######################################################
#######################################################

#######################################################
################ Things to Consider ###################
#######################################################
# - if there is a row filled with obstacles and the goal 
#	is behind the row of obstacles then pass back an empty
#	path or should we pass back a path that gets you closest
#	to it?
# - need to add in extra costs to open positions that are
#	near obstacles (as we are building the graph when you
#	are looking at a given position, check if it is next 
#	an obstacle on the map. if it is, then give it a value 
#	of 50!)
# - The goal is an actual obstacle on the map. So I need
#	to find the location closest to there?



#Import Libraries
import sys
import cv2
import numpy as np
import math
m_v = float("inf")

#######################################################
############ Define Path Planner Class ################
#######################################################

class path_planner(object):
	def __init__(self, map, goal=None):
		self.map = map

		height = len(map)
		width = len(map[1])
		center = int(int(width) / int(2))
		self.center = center
		self.height = height
		self.width = width

		# If no goal provided, then assume the goal is the center position
		# at the end of the map.
		if goal == None:
			goal = [height-1, center]
		else:
			self.goal = goal

		# Initialize the heuristics map
		m_v_map = []
		[m_v_map.append([m_v]*width) for x in range(0,height)]
		self.heuristics = m_v_map.copy()
		self.heuristics[goal[0]][goal[1]] = 0 

		# Initialize the graph map with infs, the same size as the given map
		one_layer = []
		[one_layer.append([m_v]*width) for x in range(0,width)]
		self.graph=[one_layer.copy()]

		# Initialize the openset with a starting location. For us this will be the center point
		# of the first row.
		self.openset = [[0,center]]

		self.closedsed = []

		# Initialize the path list
		self.path = []

	def __str__(self):
		return str(self.map)

	def __repr__(self):
		return str(self.map)

	def gen_heuristics(self, heuristic_function=1):
		# loop over the heuristics map adding distances to each cell from the goal 
		# get the list of neighbors that are decided
		# If the heuristic_function is 1 then use diagonal distance max(abs(x-x_goal), abs(y-y_goal)),
		# otherwise use the euclidean distance
		for iHeight in range(len(self.heuristics)):
			for iWidth in range(len(self.heuristics)):
				# Use the diagonal distance as the heuristic function
				if heuristic_function==1:
					self.heuristics[iHeight][iWidth] = max(abs(iHeight-self.goal[0]), abs(iWidth-self.goal[1]))
				else:
					self.heuristics[iHeight][iWidth] = math.sqrt((iHeight-self.goal[0])**2 + (iWidth-self.goal[1])**2)
		return self.heuristics


		# Get the 8 nearest neighbors to NQuery (i,j)
		# Need each point to be within the boundary
		# | (i-1, j-1) | (i-1, j,) |  (i-1, j+1) |
		# | (i, j-1)   |  (i, j,)  |  (i, j+1)   |
		# | (i+1, j-1) | (i+1, j,) |  (i+1, j+1) |

		
	def get_next_2_you_neighbors(self, row_val, NQuery_j):
		next2you = [[row_val, NQuery_j-1], [row_val+1, NQuery_j], [row_val, NQuery_j+1]]
		count_next2you_obstacles = 0
		for a_point in range(len(next2you)):
			# First check if you're within the boundary
			if (next2you[a_point][0] >= 0 and next2you[a_point][1] >= 0 and
				next2you[a_point][0] <= self.height-1 and next2you[a_point][1] <= self.width-1):
				if self.map[next2you[a_point][0]][next2you[a_point][1]] == 1:
					count_next2you_obstacles+=1
		return count_next2you_obstacles

	def get_diag_2_you(self, row_val, NQuery_j):
		diag2you = [[row_val+1, NQuery_j-1], [row_val+1, NQuery_j+1]]
		count_diag2you_obstacles = 0
		for a_point in range(len(diag2you)):
			# Verify the point is on the map!
			if (diag2you[a_point][0] >= 0 and diag2you[a_point][1] >= 0 and
				diag2you[a_point][0] <= self.height-1 and diag2you[a_point][1] <= self.width-1):
				if self.map[diag2you[a_point][0]][diag2you[a_point][1]] == 1:
					count_diag2you_obstacles+=1
		return count_diag2you_obstacles


	def gen_graph(self):
		# Set up the graph 
		# if either of the first step positions (first row), center, center-1, or center+1 
		# is an obstacle then set that position on the graph to be m_v. If there are no 
		# obstacles then set the first row to be 2 1 2 centered at center

		# Initialize the three steps surround center in the first row to be 2, 1, 2
		
		self.graph[0][self.center][self.center-1] = 2
		self.graph[0][self.center][self.center] = 1
		self.graph[0][self.center][self.center+1] = 2
		if self.map[0][self.center] == 1:
			self.graph[0][self.center][self.center] = m_v
		if self.map[0][self.center+1] == 1:
			self.graph[0][self.center][self.center+1] = m_v
		if self.map[0][self.center-1] == 1:
			self.graph[0][self.center][self.center-1] = m_v
		
		# For every additional pair of rows in the map (loop height - 1) create the graph
		# for the given pair of rows. Then append this to the start of the graph!
		for i_row in range(self.height-1):
			new_layer = []
			print("The row is: ", i_row)
			[new_layer.append([m_v]*self.width) for x in range(0,self.width)]
			for i_col in range(self.width):
				for j_col in range(self.width):
					if self.map[i_row+1][j_col] == 1: #is this location on the map an obstacle?
						new_layer[i_col][j_col] = m_v
					else:
						diff = abs(j_col-i_col)
						next2you_obstacles = self.get_next_2_you_neighbors(i_row+1, j_col)
						if diff == 0:
							# Need to get the number of diag's that are obstacles
							# and the number of next2you's that are obstacles
							new_layer[i_col][j_col] = 1 
						elif diff == 1:
							new_layer[i_col][j_col] = 2
						else:
							new_layer[i_col][j_col] = m_v
			self.graph.append(new_layer)
		return self.graph


	def path_planner(self):
		# The starting location is always from the row beneath, so our first row
		# will always be the heuristics + cost for the immediate three positions. need to add the 
		# center position to the open list. 

		# If there is an obstacle in the center, center-1, and center + 1 then 
		# return self.path as an empty list
		if (self.map[0][self.center]==1) and (self.map[0][self.center-1]==1) and (self.map[0][self.center+1]==1):
			# then return self.path = []
			self.path = []
			return self.path
		else:
			# there is a possible path. so go find it :)
			self.path = [2, 1]
			return self.path



# Testing Here!
default_map = [
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]

small_map = [
        [0, 0, 0],
        [1, 0, 1],
        [0, 1, 0]]

big_map = [
    [0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0]]

blocked_map = [
        [1, 1, 1],
        [1, 0, 0],
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]


# Test the Class
p = path_planner(small_map, [2,2])
#print(p.map)
#print(p.graph)
#print(p.heuristics)
# print(p.graph)
t = p.gen_graph()
diags = p.get_diag_2_you(0, 1)
print(diags)
#print(t)

#print(p.path_planner())

# for i in range(len(t)):
# 	for j in range(len(t[0])):
# 		print(t[i][j])

