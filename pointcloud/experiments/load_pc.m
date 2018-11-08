% load the point cloud file into workspace
raw_ptCloud = pcread('pc0004.ply');

% read locations and colors from raw
locs = raw_ptCloud.Location;
cols = raw_ptCloud.Color;
% switch the x and z axis in locations
locs(:, [2 3]) = locs(:, [3 2]);
locs(:, 3) = -locs(:, 3);
locs(:, 1) = -locs(:, 1);

% create a new point cloud with swapped axis
ptCloud = pointCloud(locs, 'Color', cols);

% show the original point cloud
figure
pcshow(ptCloud)
xlabel('X(m)')
ylabel('Y(m)')
zlabel('Z(m)')
title('Original Point Cloud')
