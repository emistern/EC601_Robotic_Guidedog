def door_detection_filter(coord, min_dist, num_row, size_row):
	distance = coord[0]*(size_row/num_row)
	if(distance<min_dist):
		return 1
	else:
		return 0
