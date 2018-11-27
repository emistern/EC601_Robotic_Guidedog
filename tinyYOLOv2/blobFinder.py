import cv2
import numpy as np
from sklearn.mixture import GaussianMixture as GMM

class blobFinder(object):
    def __init__(self,
                 input_width = 640,
                 input_height= 480
                 ):
        self.input_width  = input_width
        self.input_height = input_height

        #---------- Find Main Color using Gaussian Model ------

    def find_color(self, frame, predictions, padding = 0.5, cutoff = 0.5):

        assert (padding < 1.0 and cutoff < 1.0)

        image_bgr = cv2.resize(frame,(self.input_height, self.input_width), interpolation = cv2.INTER_CUBIC)

        image_bgr = cv2.GaussianBlur(image_bgr, (3,3), 0)

        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        from sklearn.mixture import GaussianMixture as GMM

        colors = []

        for pred in predictions:

            box = pred[0]  # left top right bottom

            # determin boundraies of the predict box
            left = 0 if (box[0] <= 0) else box[0]
            top  = 0 if (box[1] <= 0) else box[1]
            right  = self.input_width - 1 if (box[2] >= self.input_width) else box[2]
            bottom = self.input_height- 1 if (box[3] >= self.input_height)else box[3]

            bottom -= int((bottom - top) * cutoff)

            w = right - left
            h = bottom - top
            left += int(float(w) * padding/2.0)
            top += int(float(h) * padding/2.0)
            right -= int(float(w) * padding/2.0)
            bottom -= int(float(h) * padding/2.0)

            #cropped_img = image[top: bottom, left: right]
            #cv2.imshow("crop", cropped_img)

            # transfer the image from [width, height, 3] to [3, width * height]        
            pixels = []

            for i in range(left, right):

                for j in range(top, bottom):

                    pixels.append(image[j][i])
            
            # fit a gaussian model to find the theme color
            gmm = GMM(n_components=1, covariance_type='full').fit(pixels)

            colors.append(gmm.means_[0])
            #input()

        return colors

    #---------- Generate Color Masks ----------

    def gen_color_mask(self, frame, predictions, colors, window_size = 150.0):

        import numpy as np

        image_bgr = cv2.resize(frame,(self.input_height, self.input_width), interpolation = cv2.INTER_CUBIC)

        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        masks = []

        for i, pred in enumerate(predictions):

            color = colors[i]

            box = pred[0]

            # determin boundraies of the predict box
            left = 0 if (box[0] <= 0) else box[0]
            top  = 0 if (box[1] <= 0) else box[1]
            right  = self.input_width - 1 if (box[2] >= self.input_width) else box[2]
            bottom = self.input_height- 1 if (box[3] >= self.input_height)else box[3]
            
            # crop image
            cropped_image = image[top: bottom, left: right]
            # cv2.imshow("cropped_image", cropped_image)

            # determine the lower bar and the upper bar
            lower = np.array(color) - (window_size / 2.0)
            upper = np.array(color) + (window_size / 2.0)

            # generate mask
            mask = cv2.inRange(cropped_image, lower, upper)
            # cv2.imshow("mask", mask)
            masks.append([mask, [left, top, right, bottom]])

        return masks

    #---------- Draw Color Masks on Image ----------

    def draw_color_mask(self, image, colors, masks):

        for k, raw_mask in enumerate(masks):

            mask = raw_mask[0]
            #print(mask)
            box = raw_mask[1]
            
            color = colors[k]

            # determine the boundries of the object
            left = box[0]
            top  = box[1]
            right= box[2]
            bottom=box[3]
            #print(right-left, bottom-top)
            #print(mask.shape)
            # apply mask on image
            for i in range(left, right):

                for j in range(top, bottom):

                    m = i - left
                    n = j - top
                    #print(mask[m][n])
                    if(mask[n][m] == 255):
                        #print("*")
                        image[j][i][0] = 255#int(color[0])
                        image[j][i][1] = 0#int(color[1])
                        image[j][i][2] = 255#int(color[2])

        return image