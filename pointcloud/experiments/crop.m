% crop the center part in point cloud

% find the max and min of z-axis in points
max_z = max(locs(:, 3));
min_z = min(locs(:, 3));

max_y = max(locs(:, 2));
min_y = min(locs(:, 2));

max_x = max(locs(:, 1));
min_x = min(locs(:, 1));

% tolerance
t = 0.4;  % 10cm

% roi
roi = [min_x max_x; min_y max_y; (min_z + t) (max_z - t)];

% crop the point cloud
indices = findPointsInROI(ptCloud, roi);
ptCloud_crop = select(ptCloud, indices);