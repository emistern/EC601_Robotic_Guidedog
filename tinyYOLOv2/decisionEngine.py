import cv2
import numpy as np

class decisionEngine(object):
    def __init__(self,
                 input_height = 416,
                 input_width = 416):

        # Setup parameters of the detector

        self.input_height = input_height

        self.input_width = input_width

        # Initialize parameters for linear filter

        self.buf_pos = [0, 0, 0, 0, 0]

        self.buf_len = [0, 0, 0, 0, 0]
        
        self.wei_pos = [1, 1, 1, 1, 1]
        
        self.wei_len = [1, 1, 1, 1, 1]

#----------- Stage 1: finding the maximum empty interval between objects -------------

    def detect_freespace(self, predictions):
        space = []
        for i in range(self.input_width):
            space.append(0)

        for pred in predictions:
            box = pred[0] # left top right bottom
            conf = pred[1]
            label = pred[2]
            if (label != "chair"):
                continue
            left = 0 if (box[0] <= 0) else box[0]
            right = self.input_width - 1 if (box[2] >= self.input_width) else box[2]
            for i in range(left, right):
                space[i] = 1

        # find maximum free space
        len_max = 0
        len_buf = 0
        pos_max = 0
        state = 0
        for i in range(len(space)):
            if (i == 0):
                if (space[i] == 0):
                    state = 1
                    len_buf = 1
            elif (i == len(space) - 1):
                if (space[i] == 0):
                    len_buf += 1
                    if (len_buf > len_max):
                        len_max = len_buf
                        pos_max = i - len_buf
            else:
                if (space[i] == 0 and space[i-1] == 1):
                    state = 1
                    len_buf = 1
                elif (space[i] == 1 and space[i-1] == 0):
                    state = 0
                    if (len_buf > len_max):
                        len_max = len_buf
                        pos_max = i - len_buf
                    len_buf = 0
                else:
                    if (state == 1):
                        len_buf += 1
                    else:
                        pass
        return [pos_max, len_max]

#----------- Stage 2: Pass the freespace detection result throught linear filter ----------

    def filt_freespace(self, freespace):
        position = freespace[0]
        length   = freespace[1]

        self.buf_pos.pop(0)
        self.buf_pos.append(position)

        self.buf_len.pop(0)
        self.buf_len.append(length)

        pos_filt = 0
        for i in range(len(self.buf_pos)):
            pos_filt += self.buf_pos[i] * self.wei_pos[i]
        pos_filt = int(pos_filt / sum(self.wei_pos))

        len_filt = 0
        for i in range(len(self.buf_len)):
            len_filt += self.buf_len[i] * self.wei_len[i]
        len_filt = int(len_filt / sum(self.wei_len))

        return [pos_filt, len_filt]

#----------- DEV: Modules under Development ---------

    #---------- Blob Detection Module ----------

    def detect_blob(self, image):

        # convert color image into grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        cv2.imshow("gray", gray)

        # Initialize parameter for blob detector
        params = cv2.SimpleBlobDetector_Params()
        params.minThreshold = 0;    # the graylevel of images
        params.maxThreshold = 100;
        params.filterByColor = False
        params.blobColor = 50
        params.filterByArea = True
        params.minArea = 2000  # The dot in 20pt font has area of about 30
        params.filterByCircularity = False
        params.minCircularity = 0.7
        params.filterByConvexity = False
        params.minConvexity = 0.8
        params.filterByInertia = False
        params.minInertiaRatio = 0.4

        # Instantiate blob detector with parameters
        detector = cv2.SimpleBlobDetector_create(params)

        # deetct
        keypoints = detector.detect(gray)

        # draw keypoint in image
        im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
        return im_with_keypoints

    
#----------- The Decision Function ----------

    def decide(self, nms_predictions):

        # Stage 1
        freespace = self.detect_freespace(nms_predictions)

        # Stage 2
        filted_freespace = self.filt_freespace(freespace)

        return filted_freespace

#----------- Additional Draw Function

    def draw_freespace(self, image, freespace, color=(254.0, 254.0, 254)):
        left = freespace[0]
        top = 0
        right = left + freespace[1]
        bottom = self.input_height
        image = cv2.rectangle(image, (left, top), (right, bottom), color, 6)
        return image


