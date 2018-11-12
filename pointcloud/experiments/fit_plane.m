% set the maximum point-to-plane distance
maxDistance = 0.02;

% set the normal vector of the plane
floor_ref = [0 0 1];

% set the maximum anglar distance 
maxAngularDistance = 5;

% detect the floor and extract from point cloud
[model1,inlierIndices,outlierIndices] = pcfitplane(ptCloud,...
            maxDistance,floor_ref,maxAngularDistance);
floor_plane = select(ptCloud,inlierIndices);
remainPtCloud = select(ptCloud,outlierIndices);

% show the floor plane
figure
pcshow(floor_plane)
title('Floor Plane')

% show the remian point cloud
figure 
pcshow(remainPtCloud)
title('Remains')

% extract the obstacle points from remain 
obs_3d = remainPtCloud.Location;

% project the 3d obstables into 2d
proj_mat = [1 0;
            0 1;
            0 0];
        
obs_2d = obs_3d * proj_mat;
figure
scatter(obs_2d(:, 1), obs_2d(:, 2), 1, 'filled');
title('Map')