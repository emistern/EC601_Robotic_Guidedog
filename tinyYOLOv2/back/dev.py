import tensorflow as tf
import os
import numpy as np
import net
import weights_loader
import cv2
import warnings
import sys
import time
from test_webcam import *


class DecisionEngine(object):
    """ Decision Engine of Robot Guide Dog """
    def __init__(self, 
                 weight_path='./yolov2-tiny-voc.weights', 
                 ckpt_folder_path = './ckpt/',
                 video_source = './test_video.mov'):
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()

        saver = tf.train.Saver()
        _ = weights_loader.load(self.sess, weight_path,ckpt_folder_path, saver)

        self.video_capture = cv2.VideoCapture(video_source)

        self.input_height = 416
        self.input_width = 416
        self.score_threshold = 0.3
        self.iou_threshold = 0.3
        self.n_frame = 0

        self.buf_pos = [0, 0, 0, 0, 0]
        self.buf_len = [0, 0, 0, 0, 0]
        self.wei_pos = [1, 1, 1, 1, 1]
        self.wei_len = [1, 1, 1, 1, 1]

    def detect_image(self, path):
        output_image_path = './output.jpg'
        image = cv2.imread(path)

        preprocessed_image = preprocessing(image,self.input_height,self.input_width)

        predictions = []
        predictions = inference(self.sess,preprocessed_image)

        output_image, nms_predictions = postprocessing(predictions,
                                      image,
                                      self.score_threshold,
                                      self.iou_threshold,
                                      self.input_height,
                                      self.input_width)

        # left top right bottom
        freespace = self.detect_freespace(nms_predictions)

        output_image = self.draw_freespace(output_image, freespace)

        cv2.imwrite(output_image_path,output_image)

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

    def draw_freespace(self, image, freespace, color=(254.0, 254.0, 254)):
        left = freespace[0]
        top = 0
        right = left + freespace[1]
        bottom = self.input_height
        image = cv2.rectangle(image, (left, top), (right, bottom), color, 6)
        return image

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

    def detect_frame(self):
        _, frame = self.video_capture.read()
        self.n_frame += 1

        preprocessed_image = preprocessing(frame,self.input_height,self.input_width)

        predictions = []
        predictions = inference(self.sess,preprocessed_image)

        output_image, nms_predictions = postprocessing(predictions,
                                      frame,
                                      self.score_threshold,
                                      self.iou_threshold,
                                      self.input_height,
                                      self.input_width)

        freespace = self.detect_freespace(nms_predictions)

        filt_freespace = self.filt_freespace(freespace)

        nonfilt_image = self.draw_freespace(output_image, freespace)

        filt_image = self.draw_freespace(output_image, filt_freespace, (127.0, 254.0, 254))

        cv2.imshow('Video', nonfilt_image)

    def detect_video(self):
        while True:
            self.detect_frame()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close_camera(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    e = DecisionEngine()
    #e.detect_image("./person.jpg")
    e.detect_video()
    e.close_camera()



