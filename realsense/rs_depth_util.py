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


    def save_depth_to_npy(self, bagfile_dir, n_img = 3, interval = 100000):

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

            # Start streaming from file
            pipeline.start(config)

            count = 0

            for i in range((n_img - 1) * interval + 1):

                if (i % interval != 0):

                    continue

                else:
            
                    # Get frameset of depth
                    frames = pipeline.wait_for_frames()

                    # Get depth frame
                    depth_frame = frames.get_depth_frame()

                    # Colorize depth frame to jet colormap
                    # depth_color_frame = rs.colorizer().colorize(depth_frame)
                    
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

    w.save_depth_to_npy("./20181011_223353.bag")

    w.verify_depth_matrix()
