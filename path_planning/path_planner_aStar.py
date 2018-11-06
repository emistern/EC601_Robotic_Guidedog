# Path Planner with A* algorith

#######################################################
#################### Assumptions ######################
#######################################################

# - the starting position is the center position of the map, one layer above.
# - the A* algorithm starts at the min total cost location in the first row
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
# - the graph generator adds additional costs if there are obstacles
#	near the position you are calculating the cost for.

#######################################################
#######################################################

#######################################################
################## Things to Add ######################
#######################################################
# - if there is a row filled with obstacles and the goal 
#	is behind the row of obstacles then pass back an empty
#	path or should we pass back a path that gets you closest
#	to it?
# - need to add an algorithm for finding the goal location
#	if it isn't provided by the mapping team. Need to find the
#	farthest free location.
# - add error check. If the get_neighbors of idxNBest is
#	then return the current path. This basically means
#	there are obstacles preventing you from moving 
#	forwards

#######################################################
#######################################################


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

		# Set the goal location on the map equal to a free space
		self.map[goal[0]][goal[1]] = 0

		# Initialize the heuristics map
		m_v_map = []
		[m_v_map.append([m_v]*width) for x in range(0,height)]
		self.heuristics = m_v_map.copy()
		self.heuristics[goal[0]][goal[1]] = 0 

		# Initialize the graph map with infs, the same size as the given map
		one_layer = []
		[one_layer.append([m_v]*width) for x in range(0,width)]
		self.graph=[one_layer.copy()]

		# Initialize the open and the closed sets
		self.openset = {}
		self.closedset = []

		# Initialize the path list
		self.path = []

	def __str__(self):
		return str(self.map)

	def __repr__(self):
		return str(self.map)

	def gen_heuristics(self, heuristic_function=1):
		# loop over the heuristics map adding distances to each cell from the goal 
		# If the heuristic_function is 1 then use diagonal distance max(abs(x-x_goal), abs(y-y_goal)),
		# otherwise use the euclidean distance
		for iHeight in range(len(self.heuristics)):
			for iWidth in range(len(self.heuristics[0])):
				# Use the diagonal distance as the heuristics function
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

	
	# This method get's all of the neighbors that are directly next to a given query location
	# i.e. if the query is (i,j) then it would return (i, j-1), (i-1, j,), (i, j+1)	
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

	# This method get's all of the neighbors that are diagonal to a given query location
	# i.e. if the query is (i,j) then it would return (i-1, j+1) and (i-1, j-1)	
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


	# This method generates the graph of a given map. It calculates the cost to move from every node
	# to another possible node. It adds extra costs if there are nearby obstacles.
	def gen_graph(self):
		# Set up the graph 
		# if either of the first step positions (first row), center, center-1, or center+1 
		# is an obstacle then set that position on the graph to be m_v. If there are no 
		# obstacles then set the first row to be 2 1 2 centered at center

		#Initialize the three steps surround center in the first row to be 2, 1, 2 + obstacle cost
		first_row = [-1 ,0, 1]
		for a_point in first_row:
			next2you_obstacles = self.get_next_2_you_neighbors(0, self.center+a_point)
			diag2you_obstacles = self.get_diag_2_you(0, self.center+a_point)
			obstacles_cost = next2you_obstacles*25 + diag2you_obstacles*15
			if a_point != 0:
				cost = 2
			else:
				cost = 1
			self.graph[0][self.center][self.center+a_point] = cost + obstacles_cost

		
		# For every additional pair of rows in the map (loop height - 1) create the graph
		# for the given pair of rows. Then append this to the start of the graph!
		for i_row in range(self.height-1):
			new_layer = []
			[new_layer.append([m_v]*self.width) for x in range(0,self.width)]
			for i_col in range(self.width):
				for j_col in range(self.width):
					if self.map[i_row+1][j_col] == 1: #is this location on the map an obstacle?
						new_layer[i_col][j_col] = m_v
					else:
						diff = abs(j_col-i_col)
						# Add extra costs if you are near an obstacle. 15 if the point has
						# diagonal with obstacle, and 25 if the obstacle is next to you.
						next2you_obstacles = self.get_next_2_you_neighbors(i_row+1, j_col)
						diag2you_obstacles = self.get_diag_2_you(i_row+1, j_col)
						obstacles_cost = next2you_obstacles*25 + diag2you_obstacles*15
						if diff == 0:
							# Need to get the number of diag's that are obstacles
							# and the number of next2you's that are obstacles
							new_layer[i_col][j_col] = 1 + obstacles_cost 
						elif diff == 1:
							new_layer[i_col][j_col] = 2 + obstacles_cost
						else:
							new_layer[i_col][j_col] = m_v
			self.graph.append(new_layer)
		return self.graph

	# This function picks the minimum cost index in the first row as the starting position on the map.
	def pick_start_pos(self):
		# If the first row is all obstacles then pass back an empty start list, which
		# should tell the path_planner that there is no start

		# Add in the heuristics for each position and then append it to a total cost list
		# then get the min value and index for it.
		# the first row of the graph
		graph_vals = self.graph[0][self.center]
		total_cost = []
		for a_pos in range(len(graph_vals)):
			if graph_vals[a_pos] != m_v:
				total_cost = total_cost + [graph_vals[a_pos]+self.heuristics[0][a_pos]]

		if (self.map[0][self.center]==1) and (self.map[0][self.center-1]==1) and (self.map[0][self.center+1]==1):
			starting_location = []
			return starting_location
		else:
			starting_location = [total_cost.index(min(total_cost))]
		return starting_location


	def path_planner(self, starting_location):
		# If there is an obstacle in the center, center-1, and center + 1 then 
		# return self.path as an empty list
		if len(self.pick_start_pos())==0:
			self.path = []
			return self.path
		else:
			# there is a possible path. so go find it :)
			# initialize the dictionary to hold all of the neighbors, the key is a given location, and 
			# the values is a list of tuples of all neighbors coordinates
			all_cost_backpointers = {}
			all_neighbors = {}
			
			# Add the starting node to the openset along with its cost
			row = 0 # The row that the starting_position is in.
			starting_location_cost = self.heuristics[0][starting_location[0]] + self.graph[0][self.center][starting_location[0]]
			self.openset[(row, starting_location[0])] = starting_location_cost
			print(self.openset)
			
			# Repeat the following steps until the open set is empty
			# Get the lowest cost item from the open list and add it to the closed list
			#while (len(self.openset)!=0):
			row +=1
			idxNbest=min(self.openset.items(), key=lambda x: x[1])[0]
			self.openset.pop(idxNbest, None)
			print("the idxBest: ",idxNbest)
			self.closedset.append(idxNbest)
			print(self.closedset)

			# Add the information for the starting_location to the cost/backpointer dictionary
			all_cost_backpointers[idxNbest]  = [(), ()]
			
			# Check if idxNBest is the goal
			if idxNbest == self.goal:
				#break # uncomment this line when you turn the while loop back on
				print("break")

			# Get the neighbors of idxNbest
			# get the row on the graph that corresponds to the neighbors of idxNBest
			graph_vals = self.graph[idxNbest[0]+1][idxNbest[1]]
			print("Graph_vals: ",graph_vals)
			available_neighbors = []
			for a_neighbor in range(len(graph_vals)):
				# Loop over each neighbor that is not m_v and check if it is in the closed set
				if graph_vals[a_neighbor]==m_v:
					pass # We only care about free positions
				else:
					# Check if the neighbor is not in the closed set, then do steps 9-16
					if (row, a_neighbor) not in self.closedset:
						available_neighbors.append((row, a_neighbor))
						 
						# now check if this valid neighbor is already in the open set
						if (row, a_neighbor) not in self.openset:
							print(row, a_neighbor)
						# need to think through if the openset should be a dictionary, with the 
						# key as the location and the value as the cost.
						# also maybe need a dictionary to store the backpointers + total cost
			all_neighbors[idxNbest]= (available_neighbors)			
			print(all_neighbors)

				

			# Code for how to use the list for priority queue
			# self.openset.append((1, 25))
			
			# print(self.openset)
			# self.openset.append((2, 5))
			# self.openset.sort(reverse=True)
			# print(self.openset)
			# print(self.openset.pop())

			# Need to figure out how to name each node on the graph, create a dictionary with the node
			# as the key and the coordinates as the data
			# Pick the lowest cost element from the openset

			# test path
			self.path = self.path + starting_location
			return self.path


if __name__ == "__main__":
	# Testing Here!
	default_map = [
	        [0, 0, 0], # this is the starting row
	        [1, 0, 0],
	        [0, 0, 0],
	        [0, 1, 0],
	        [0, 1, 1],
	        [0, 0, 0],
	        [0, 1, 0],
	        [1, 0, 0]
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
	p = path_planner(default_map, [4,2])
	h = p.gen_heuristics(2)
	t = p.gen_graph()
	print(p.graph)
	startpos = p.pick_start_pos()
	print(p.path_planner(startpos))

	# for i in range(len(t)):
	# 	for j in range(len(t[0])):
	# 		print(t[i][j])

