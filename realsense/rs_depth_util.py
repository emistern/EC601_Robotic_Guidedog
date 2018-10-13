import cv2
import numpy as np

class depth_worker():

    def __init__(self, save_dir = "./tmp_img/"):

        self.save_dir = save_dir

        return

    def read_depth_matrix(self):

        # -------------------------------------------- #
        # Iterate through all the .npy files in the dir and return raw matrix
        # -------------------------------------------- #

        from os  import listdir

        filenames = listdir(self.save_dir)

        for filename in filenames:

            if (not filename.endswith(".npy")):

                continue  # not a .npy file

            else:

                raw = np.load(self.save_dir + filename)

                yield raw

    def normalize_matrix(self, mat):

        # return the dynamically normalized depth matrix

        return np.asanyarray(mat / np.amax(mat) * 255.0).astype(np.uint8)

    def verify_depth_matrix(self, n_img = 3, show_img = True):

        # -------------------------------------------- #
        # Verify the depth matrix by read into memory and print
        # n_img: number of matrix file you want to check
        # -------------------------------------------- #

        from os import listdir

        filenames = listdir(self.save_dir)

        for filename in filenames:

            if (not filename.endswith(".npy")):

                continue  # not a .npy file

            else:

                raw = np.load(self.save_dir + filename)

                print(raw)

                if (show_img):

                    normalized = self.normalize_matrix(raw)

                    cv2.imshow("Verify", normalized)

                    cv2.waitKey(20)

            input()

    def play_depth_stream(self, bagfile_dir):

        # -------------------------------------------- #
        # Play bag file depth images with filtering
        # -------------------------------------------- #

        import pyrealsense2 as rs

        input = bagfile_dir

        try:
            # Create pipeline
            pipeline = rs.pipeline()

            # Create a config object
            config = rs.config()
            
            # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
            rs.config.enable_device_from_file(config, input)
            
            # Configure the pipeline to stream the depth stream
            config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

            # Start streaming from file
            pipeline.start(config)

            # Declare filters
            dec_filter = rs.decimation_filter()   # Decimation - reduces depth frame density
            
            spat_filter = rs.spatial_filter()          # Spatial    - edge-preserving spatial smoothing
            
            temp_filter = rs.temporal_filter()    # Temporal   - reduces temporal noise

            fill_filter = rs.hole_filling_filter()  # Hole Filling filter

            disp_filter = rs.disparity_transform()  # Disparity Transform filter

            # Streaming loop
            while True:
                # Get frameset of depth
                frames = pipeline.wait_for_frames()

                # Get depth frame
                depth_frame = frames.get_depth_frame()

                # Perform filtering
                filtered = dec_filter.process(depth_frame)

                filtered = spat_filter.process(filtered)
                
                filtered = fill_filter.process(filtered)
                
                filtered = temp_filter.process(filtered)
                
                # Colorize depth frame to jet colormap
                depth_color_frame = rs.colorizer().colorize(depth_frame)
                depth_color_frame_filt = rs.colorizer().colorize(filtered)

                # Convert depth_frame to numpy array to render image in opencv
                depth_color_image = np.asanyarray(depth_color_frame.get_data())
                depth_color_image_filt = np.asanyarray(depth_color_frame_filt.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())

                # Render image in opencv window
                cv2.imshow("Depth Stream", depth_color_image)
                cv2.imshow("Depth Stream Filted", depth_color_image_filt)

                key = cv2.waitKey(1)
                # if pressed escape exit program
                if key == 27:
                    cv2.destroyAllWindows()
                    break
        finally:
            pass

    def save_depth_to_npy(self, bagfile_dir, n_img = 3, interval = 100, filter = True):

        # -------------------------------------------- #
        # Read the bag file and save depth matrix to .npy file
        # n_img: number of matrix you want to save
        # interval: number of frames between saved matrix
        # -------------------------------------------- #

        import pyrealsense2 as rs

        input = bagfile_dir

        try:
            # Create pipeline
            pipeline = rs.pipeline()

            # Create a config object
            config = rs.config()
            
            # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
            rs.config.enable_device_from_file(config, input)
            
            # Configure the pipeline to stream the depth stream
            config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

            # Declare filters
            dec_filter = rs.decimation_filter()   # Decimation - reduces depth frame density
            
            spat_filter = rs.spatial_filter()          # Spatial    - edge-preserving spatial smoothing
            
            temp_filter = rs.temporal_filter()    # Temporal   - reduces temporal noise

            fill_filter = rs.hole_filling_filter()  # Hole Filling filter

            disp_filter = rs.disparity_transform()  # Disparity Transform filter

            # Start streaming from file
            pipeline.start(config)

            count = 0

            for i in range((n_img - 1) * interval + 1):

                if (i % interval != 0):

                    # Get frameset of depth
                    frames = pipeline.wait_for_frames()

                    continue

                else:
            
                    # Get frameset of depth
                    frames = pipeline.wait_for_frames()

                    # Get depth frame
                    depth_frame = frames.get_depth_frame()

                    if (filter):
                        # Perform filtering
                        filtered = dec_filter.process(depth_frame)

                        filtered = spat_filter.process(filtered)

                        filtered = fill_filter.process(filtered)

                        depth_frame = temp_filter.process(filtered)
                    
                    # Convert depth_frame to numpy array to render image in opencv
                    raw = depth_frame.get_data()
                    
                    # generate filename
                    filename = self.save_dir  + "depth" + "%04d"%count + ".npy"

                    # Save raw data into numpy matrix file
                    np.save(filename, raw)

                    count += 1

                    print("save %d th depth matrix from %d th frame to" % (count, i) + filename)
        finally:
            pass
        return

if __name__ == "__main__":
    
    w = depth_worker()

    #w.play_depth_stream("./20181011_223353.bag")
    
    w.save_depth_to_npy("./20181011_223353.bag")

    w.verify_depth_matrix()
