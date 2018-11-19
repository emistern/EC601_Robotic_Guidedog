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
# - If there is an obstacle directly infront of you and next to you
#	you cannot pass through diagonally between the two obstacles

#######################################################
#######################################################

#######################################################
################## Things to Add ######################
#######################################################
# - if there is a row filled with obstacles and the goal 
#	is behind the row of obstacles then pass back an empty
#	path or should we pass back a path that gets you closest
#	to it?
# - add error check. If the get_neighbors of idxNBest is []
#	then return the current path. This basically means
#	there are obstacles preventing you from moving 
#	forwards
# - Figure out why on the big_map[4.4] is failing
# - run this same example. It should find a goal location
#	maybe change the if statements to look for where each
#	pattern is free rather than an obstacle. (if directly
#	underneath you and two underneath you are both free
#	then set that as the goal)


#######################################################
#######################################################


#Import Libraries
import cv2
import numpy as np
m_v = float("inf")

#######################################################
############ Define Path Planner Class ################
#######################################################

class path_planner(object):
	def __init__(self, map, goal=None):
		self.map = map

		self.center = int(int(len(map[1])) / int(2))
		self.height = len(map)
		self.width = len(map[1])

		# If no goal provided, then assume the goal is the center position
		# at the end of the map.
		self.get_goal_location(goal)
		if len(self.goal) != 0:
			# Initialize the heuristics map
			m_v_map = []
			[m_v_map.append([m_v]*self.width) for x in range(0,self.height)]
			self.heuristics = m_v_map.copy()
			self.heuristics[self.goal[0]][self.goal[1]] = 0 

		# Initialize the graph map with infs, the same size as the given map
		one_layer = []
		[one_layer.append([m_v]*self.width) for x in range(0,self.width)]
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

	def get_goal_location(self, goal):
		if len(goal) == 0:
			# run an algorithm to find a good goal location starting from the end
			# Generate samples around the center line.
			samples = [self.center, self.center-1, self.center+1]
			
			# Now check these samples in the last row and check if their
			# neighbors and diag-neighbors are obstacles
			goal_flag = False
			row = self.height
			while goal_flag==False:
				row -=1
				if row == 0:
					self.goal = []
					return self
				
				for a_sample in samples:
					# print(row, a_sample)
					if self.map[row-1][a_sample]==0 and self.map[row-2][a_sample]==0:
						goal_flag  = True
						
						break
					# Now count the obstacles nearby, check for the specific situations
					if a_sample-1>=0:
						if self.map[row][a_sample-1]==1 and self.map[row-1][a_sample]==1:
							pass
						if self.map[row-1][a_sample-1]==1 and self.map[row-1][a_sample]==1:
							pass
					if a_sample+1 <= self.width-1:
						if self.map[row-1][a_sample]==1 and self.map[row][a_sample+1]==1:
							pass
						if self.map[row-1][a_sample]==1 and self.map[row-1][a_sample+1]==1:
							pass

				
			#### LEFT OFF HERE ###
			if goal_flag == True:
				goal = [row, a_sample]

			else:
				goal =[]
		else:
			# The goal was provided by the object detection algorithm
			self.goal = goal
		self.goal = goal
		# print("Self.goal", self.goal)
		self.map[goal[0]][goal[1]]=0
			# need to update this with what happens if the goal does not exist
		return self


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
					self.heuristics[iHeight][iWidth] = np.sqrt((iHeight-self.goal[0])**2 + (iWidth-self.goal[1])**2)
		return self.heuristics

	
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

	def get_diag_and_next(self, row_val, NQuery_i, diff):
		# if diff is less than zero then check the diag [row_val, NQuery_i-1] and 
		#[row_val+1, NQuery_i] for obstacles
		if diff < 0:
			if row_val >=0 and row_val <= self.height-1 and NQuery_i-1>=0 and NQuery_i-1<=self.width-1:
				# now that we checked the boundaries, check if the two positions are obstacles 
				if self.map[row_val][NQuery_i-1] ==1 and self.map[row_val+1][NQuery_i]==1:
					return True
		elif diff > 0:
			if row_val >=0 and row_val <= self.height-1 and NQuery_i+1>=0 and NQuery_i+1<=self.width-1:
				if self.map[row_val][NQuery_i+1] ==1 and self.map[row_val+1][NQuery_i]==1:
					return True
		else:
			return False
				

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
			# Add boundary cost
			boundary_cost = 0
			if self.center+a_point == 0 or self.center+a_point == self.width-1:
				boundary_cost = 200
			obstacles_cost = next2you_obstacles*25 + diag2you_obstacles*15 + boundary_cost
			
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
						diff = j_col-i_col
						# Add extra costs if you are near an obstacle. 15 if the point has
						# diagonal with obstacle, and 25 if the obstacle is next to you.
						next2you_obstacles = self.get_next_2_you_neighbors(i_row+1, j_col)
						diag2you_obstacles = self.get_diag_2_you(i_row+1, j_col)
						# Add boundary cost as well
						boundary_cost = 0
						if j_col == 0 or j_col == self.width-1:
							boundary_cost = 50
						obstacles_cost = next2you_obstacles*25 + diag2you_obstacles*15 + boundary_cost
						if abs(diff) == 0:
							# Need to get the number of diag's that are obstacles
							# and the number of next2you's that are obstacles
							new_layer[i_col][j_col] = 1 + obstacles_cost 
						elif abs(diff) == 1:
							# add a check here if the position directly underneath the diagonal
							# and right next to the diagonal (same row) then set 
							if self.get_diag_and_next(i_row, i_col, diff): #is this location on the map an obstacle?
							 	new_layer[i_col][j_col] = m_v
							else:
								new_layer[i_col][j_col] = 2 + obstacles_cost
						else:
							new_layer[i_col][j_col] = m_v
			self.graph.append(new_layer)
		return self.graph


	# This function picks the minimum cost index in the first row as the starting position on the map.
	def pick_start_pos(self):
		# Add in the heuristics for each position and then append it to a total cost list
		# then get the min value and index for it.
		# the first row of the graph
		graph_vals = self.graph[0][self.center]
		total_cost = []
		for a_pos in range(len(graph_vals)):
			if graph_vals[a_pos] != m_v:
				total_cost = total_cost + [graph_vals[a_pos]+self.heuristics[0][a_pos]]
		# If the first row is all obstacles then pass back an empty start list, which
		# should tell the path_planner that there is no start
		if (self.map[0][self.center]==1) and (self.map[0][self.center-1]==1) and (self.map[0][self.center+1]==1):
			starting_location = []
		else:
			starting_location = [total_cost.index(min(total_cost))]
		return starting_location

	# this function moves through the backpointers of the map and creates a path
	def get_path_from_backpointers(self, starting_location, all_cost_backpointers):
	# Now loop through all of the backpointers starting from the goal location and add that to the path
		try:
			backpointer = (self.goal[0], self.goal[1])
			while (backpointer != (0, starting_location[0])):
				self.path.append(backpointer[1])
				backpointer = all_cost_backpointers[backpointer][0]
			self.path.append(starting_location[0])
			
			return self.path[::-1]
		# If the goal location has no backpointers then there is likely obstacles all the way through
		except:
			return []

	def priority_queue(self):
		idxNbest=min(self.openset.items(), key=lambda x: x[1])[0]
		self.openset.pop(idxNbest, None)
		self.closedset.append(idxNbest)
		return idxNbest


	def path_search(self, starting_location):
		# If there is an obstacle in the center, center-1, and center + 1 then 
		# return self.path as an empty list
		if len(starting_location)==0:
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
			g_x = 0
			f_x = self.heuristics[0][starting_location[0]] + g_x
			self.openset[(row, starting_location[0])] = f_x
			# Add the information for the starting_location to the backpointer/cost dictionary
			all_cost_backpointers[(row, starting_location[0])]  = [(), 0]
			

			# Repeat the following steps until the open set is empty
			while (len(self.openset)!=0):
				# print("open Set: ", self.openset)
				# Get the lowest cost item from the open list
				idxNbest=self.priority_queue()
				
				# Check if idxNBest is the goal
				if idxNbest == (self.goal[0], self.goal[1]):
					break
				# Update the row
				row = idxNbest[0] + 1

				# Do error checking, if the row == self.height -1 then skip 
				# also check if you're at the goal
				while row == self.height:
					# print(idxNbest)
					idxNbest=self.priority_queue()
					# Update the row
					row = idxNbest[0] + 1
					# If you're at the goal location then run through the backpointers
					if idxNbest == (self.goal[0], self.goal[1]):
						return self.get_path_from_backpointers(starting_location, all_cost_backpointers)


				# Get the neighbors of idxNbest
				# get the row on the graph that corresponds to the neighbors of idxNBest
				graph_vals = self.graph[row][idxNbest[1]]
				available_neighbors = []
				for a_neighbor in range(len(graph_vals)):
					# Loop over each neighbor that is not m_v and check if it is in the closed set
					if graph_vals[a_neighbor]==m_v:
						pass # We only care about free positions
					else:
						# Check if the neighbor is not in the closed set, then do steps 9-16
						if (row, a_neighbor) not in self.closedset:
							if row==self.height and a_neighbor != self.goal[1]:
								pass 
							# now check if this valid neighbor is already in the open set
							if (row, a_neighbor) not in self.openset:
								available_neighbors.append((row, a_neighbor))
								# Update the g(x) to be g(idxNbest) + c(idxNBest, x) (the cost to move from idxnbest to x)
								g_x = all_cost_backpointers[idxNbest][1] + self.graph[row][idxNbest[1]][a_neighbor]
								# Update the backpointer and g(x) into the dictionary
								all_cost_backpointers[(row, a_neighbor)] = [idxNbest, g_x]
								# Update the total cost to be h(x)+g(x)
								f_x = self.heuristics[row][a_neighbor] + g_x
								# Add x to the openset with f(x)
								self.openset[(row, a_neighbor)] = f_x
								# add this neighbor to the openset
							elif all_cost_backpointers[idxNbest][1] + self.graph[row][idxNbest[1]][a_neighbor] < all_cost_backpointers[(row, a_neighbor)][1]:
							 	g_x = all_cost_backpointers[idxNbest][1] + self.graph[row][idxNbest[1]][a_neighbor]
							 	all_cost_backpointers[(row, a_neighbor)] = [idxNbest, g_x]


				all_neighbors[idxNbest]= (available_neighbors)		

			
			# Now loop through all of the backpointers starting from the goal location and add that to the path
			return self.get_path_from_backpointers(starting_location, all_cost_backpointers)


	def draw_path(self, path):

		unit_size = 60
		height = len(self.map)
		width = len(self.map[0])
		t_h = unit_size * height
		t_w = unit_size * width
		world = np.array([[[240] * 3] * (t_w)] * (t_h)).astype(np.uint8)

		for x in range(0, t_w, unit_size):
			pt1 = (x, 0)
			pt2 = (x, t_h)
			world = cv2.line(world, pt1, pt2, (255, 0, 0))
        
		for y in range(0, t_h, unit_size):
			pt1 = (0, y)
			pt2 = (t_w, y)
			world = cv2.line(world, pt1, pt2, (255, 0, 0))

        # Draw Obstacles
		ofs = int(unit_size / 5)
		for i, row in enumerate(self.map):
			for j, e in enumerate(row):
				if (e == 1):
					# Draw an obstacle in world
					pt1 = (j * unit_size + ofs, i * unit_size + ofs)
					pt2 = ((j+1) * unit_size - ofs, (i+1) * unit_size - ofs)
					cv2.rectangle(world, pt1, pt2, (0, 0, 255), 5)

		# Draw Optimal Path 
		x_ofs = int(unit_size / 2)
		y_ofs = int(unit_size / 2)
		for i in range(len(path)-1):

			f_p = path[i]
			t_p = path[i+1]

			pt1 = (f_p * unit_size + x_ofs, i * unit_size + y_ofs)
			pt2 = (t_p * unit_size + x_ofs, (i+1) * unit_size + y_ofs)

			world = cv2.line(world, pt1, pt2, (0, 255, 0), 5)

			if i == len(path) - 2:
				# draw target
				world = cv2.circle(world, pt2, int(unit_size / 3), (255, 0, 255), 10)

		world = np.flip(np.array(world), 0)
		cv2.imshow("path", world)


if __name__ == "__main__":
	# Testing Here!
	default_map = [
	        [0, 0, 0], # this is the starting row
	        [1, 0, 1],
	        [0, 0, 0],
	        [0, 0, 0],
	        [0, 0, 1],
	        [1, 0, 1],
	        [0, 0, 1],
	        [1, 1, 1]
	    ]

	small_map = [
	        [0, 0, 0],
	        [0, 0, 1],
	        [0, 0, 0],
	        [1, 0, 0],]

	big_map = [
	    [0, 0, 0, 0, 0],
	    [1, 0, 0, 0, 0],
	    [0, 0, 1, 1, 1],
	    [1, 0, 0, 1, 1],
	    [0, 1, 1, 0, 0]]

	big_blocked_map = [
	    [1, 1, 1, 1, 1],
	    [1, 1, 1, 1, 1],
	    [1, 1, 1, 1, 1],
	    [1, 1, 1, 1, 1],
	    [0, 1, 0, 0, 0]]

	blocked_map = [
	        [1, 1, 1],
	        [1, 0, 0],
	        [1, 0, 0],
	        [0, 0, 0],
	        [0, 1, 1],
	        [0, 0, 0],
	        [0, 1, 0],
	        [1, 1, 0]
	    ]


	# Test the Class
	goal = []
	# goal = [3,2]	
	p = path_planner(big_map, goal)
	if len(p.goal)==0:
		path = []
	else:
		h = p.gen_heuristics(2)
		# print("Heuristics:")
		# for j in range(len(h)):
		# 	print(h[j])
		t = p.gen_graph()
		# print("Graph:")
		# for i in range(len(p.graph)):
		# 	print(p.graph[i])
		startpos = p.pick_start_pos()
		# print(startpos)
		path = p.path_search(startpos)
	print(path)
	p.draw_path(path)
	cv2.waitKey(0)


