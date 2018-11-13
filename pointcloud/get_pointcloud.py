import numpy as np
import pyrealsense2 as rs

def get_pointcloud_frame(bagfile_dir, filter = False):

    # -------------------------------------------- #
    # Read the bag file and save point cloud to .ply file
    # n_img: number of matrix you want to save
    # interval: number of frames between saved matrix
    # -------------------------------------------- #

    input = bagfile_dir

    try:
        # Declare pointcloud object, for calculating pointclouds and texture mappings
        pc = rs.pointcloud()

        # We want the points object to be persistent so we can display the last cloud when a frame drops
        points = rs.points()
        
        # Create pipeline
        pipeline = rs.pipeline()

        # Create a config object
        config = rs.config()
        
        # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
        rs.config.enable_device_from_file(config, input)
    
        # Configure the pipeline to stream the depth and color stream
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

        # Declare filters
        dec_filter = rs.decimation_filter()   # Decimation - reduces depth frame density
        
        spat_filter = rs.spatial_filter()          # Spatial    - edge-preserving spatial smoothing
        
        temp_filter = rs.temporal_filter()    # Temporal   - reduces temporal noise

        fill_filter = rs.hole_filling_filter()  # Hole Filling filter

        disp_filter = rs.disparity_transform()  # Disparity Transform filter

        # Start streaming from file
        profile = pipeline.start(config)

        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)

        while(True):

            # Get frameset of depth
            frames = pipeline.wait_for_frames()

            # Get depth frame
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if (filter):
                # Perform filtering
                filtered = dec_filter.process(depth_frame)

                filtered = spat_filter.process(filtered)

                filtered = fill_filter.process(filtered)

                depth_frame = temp_filter.process(filtered)

                color_frame = dec_filter.process(color_frame)
            
            # Tell pointcloud object to map to this color frame
            pc.map_to(color_frame)

            # Generate the pointcloud and texture mappings
            points = pc.calculate(depth_frame)
            
            # yield
            points_array = np.asanyarray(points.get_vertices())
            
            yield np.asanyarray(depth_frame.get_data()), points_array
                
    finally:
        pass
    return

if __name__ == "__main__":

    gen = get_pointcloud_frame("../realsense/20181011_223353.bag")

    print (next(gen))