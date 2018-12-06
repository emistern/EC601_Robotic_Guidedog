import sys
sys.path.append("./tinyYOLOv2/")
import tensorflow as tf
import os
import numpy as np
import net
import weights_loader
import cv2
import warnings
import time
from utils import *
from blobFinder import *



class obj_det(object):
    """Testbench for decision algorithms on robot guide dog"""
    def __init__(self, 
                 weight_path='./yolov2-tiny-voc.weights', 
                 ckpt_folder_path = './ckpt/',
                 video_source = 0,
                 speed = 2):

        self.OBJECT = 'chair'

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

        #self.video_capture = cv2.VideoCapture(video_source)

        # Step 3: Setup decision engine for test

        #self.decider = decisionEngine()

        self.finder = blobFinder()

        # Additional parameter for speed up the video

        self.speed = speed

    def detect_frame(self,frame,use_bag = False):
        '''
        # Read frame from video
        for i in range(self.speed):
            _, frame = self.video_capture.read()
        print(type(frame))
        '''

        if use_bag:
            Res_x = 1280
            Res_y = 720
        else:
            Res_x = 640
            Res_y = 480
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

        coord = []

        for objects in nms_predictions:
            label = objects[2]
            box = objects[0]
            if(label == self.OBJECT):
                # determin boundraies of the predict box
                left = 0 if (box[0] <= 0) else box[0]
                top  = 0 if (box[1] <= 0) else box[1]
                right  = self.input_width - 1 if (box[2] >= self.input_width) else box[2]
                bottom = self.input_height- 1 if (box[3] >= self.input_height)else box[3]

                left = left*Res_x/416
                right = right*Res_x/416
                top =top*Res_y/416
                bottom =bottom*Res_y/416

                print("Possibility is ",objects[1])

                coord.append([int(left),int(right),int(top),int(bottom)])

        return coord
        '''
        # Call the decision engine
        freespace, decision_boxes, best_box = self.decider.decide(nms_predictions)

        filt_image = self.decider.draw_freespace(output_image, freespace, (127.0, 254.0, 254))

        for box in decision_boxes:
            filt_image = self.decider.draw_freespace(filt_image, box, (255, 0, 0))
        
        filt_image = self.decider.draw_freespace(filt_image, best_box, (0, 255, 0))

        #colors = self.finder.find_color(frame, nms_predictions)

        #masks = self.finder.gen_color_mask(frame, nms_predictions, colors)
        
        #display_img = self.finder.draw_color_mask(output_image, colors, masks)
        
        # dispay_img = self.decider.detect_blob(filt_image)
                cv2.imshow('Video', output_image)
        cv2.waitKey(10)
        #input()
        '''

    def detect_video(self):

        while True:

            print(self.detect_frame())
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close_camera(self):

        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    t = obj_det()
    #e.detect_image("./person.jpg")
    t.detect_video()
    t.close_camera()