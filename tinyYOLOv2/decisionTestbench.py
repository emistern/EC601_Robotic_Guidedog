import tensorflow as tf
import os
import numpy as np
import net
import weights_loader
import cv2
import warnings
import sys
import time
from utils import *
from decisionEngine import *

class decisionTestbench(object):
    """Testbench for decision algorithms on robot guide dog"""
    def __init__(self, 
                 weight_path='./yolov2-tiny-voc.weights', 
                 ckpt_folder_path = './ckpt/',
                 video_source = './videos/test_video.mov',
                 speed = 3):

        # Step 1: Setup TensorFlow environment for object detection

        self.sess = tf.InteractiveSession()

        tf.global_variables_initializer().run()

        saver = tf.train.Saver()

        _ = weights_loader.load(self.sess, weight_path,ckpt_folder_path, saver)

        # parameters for tinyYOLO detector

        self.input_height = 416
        self.input_width = 416

        self.score_threshold = 0.3
        self.iou_threshold = 0.3
        
        # Step 2: Setup video source from file

        self.video_capture = cv2.VideoCapture(video_source)

        # Step 3: Setup decision engine for test

        self.decider = decisionEngine()

        # Additional parameter for speed up the video

        self.speed = speed

    def detect_frame(self):

        # Read frame from video
        for i in range(self.speed):
            _, frame = self.video_capture.read()

        # Image preprocessing
        preprocessed_image = preprocessing(frame,self.input_height,self.input_width)

        # Call inference function to detect objects
        predictions = []
        predictions = inference(self.sess,preprocessed_image)

        # Post-processing for image and detection results
        output_image, nms_predictions = postprocessing(predictions,
                                      frame,
                                      self.score_threshold,
                                      self.iou_threshold,
                                      self.input_height,
                                      self.input_width)

        # Call the decision engine
        freespace = self.decider.decide(nms_predictions)

        filt_image = self.decider.draw_freespace(output_image, freespace, (127.0, 254.0, 254))

        colors = self.decider.find_color(frame, nms_predictions)

        masks = self.decider.gen_color_mask(frame, nms_predictions, colors)
        
        display_img = self.decider.draw_color_mask(output_image, colors, masks)
        # detect blob
        # dispay_img = self.decider.detect_blob(filt_image)

        cv2.imshow('Video', display_img)
        cv2.waitKey(10)
        #input()

    def detect_video(self):

        while True:

            self.detect_frame()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close_camera(self):

        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    t = decisionTestbench()
    #e.detect_image("./person.jpg")
    t.detect_video()
    t.close_camera()