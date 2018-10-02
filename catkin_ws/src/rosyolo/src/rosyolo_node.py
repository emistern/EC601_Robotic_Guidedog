#!/usr/bin/python
from TinyYolo import YoloDetector
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CompressedImage, Image
import cv2
import numpy as np

# Tiny Yolo assumes input images are these dimensions.
NETWORK_IMAGE_WIDTH = 448
NETWORK_IMAGE_HEIGHT = 448

class YoloNode():
    def __init__(self):
        self.node_name = "yolo"
        self.bridge = CvBridge()
        self.framerate = 5
        self.detector = YoloDetector()
        self.status = "init"
        # Subscribers
        self.sub_image = rospy.Subscriber("/usb_cam/image_raw", Image, self.cbImage, queue_size=1)
        # Timers
        rospy.Timer(rospy.Duration.from_sec(1.0/self.framerate), self.mainLoop)
    
    def cbImage(self, image_msg):
        cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
        #cv_image = cv2.imread('/home/yxiao1996/catkin_ws/src/rosyolo/src/512_Monitor.jpg')
        input_image = cv2.resize(cv_image, (NETWORK_IMAGE_WIDTH, NETWORK_IMAGE_HEIGHT), cv2.INTER_LINEAR)
        
        input_image = input_image.astype(np.float32)
        input_image = np.divide(input_image, 255.0)
        self.rbg = input_image
        self.disp_img = input_image
        self.status = "default"

    def preProcessImg(self):
        input_image = self.rbg
        input_image = cv2.resize(input_image, (NETWORK_IMAGE_WIDTH, NETWORK_IMAGE_HEIGHT), cv2.INTER_LINEAR)
        display_image = input_image
        self.disp_img = display_image
        input_image = input_image.astype(np.float32)
        input_image = np.divide(input_image, 255.0)

    def mainLoop(self, _event):
        if self.status == "default":
            #self.preProcessImg()
            objs = self.detector.detect(self.rbg)
            self.detector.displayDetection(self.disp_img, objs)
        
if __name__ == '__main__':
    rospy.init_node('yolo_node',anonymous=False)
    detector = YoloNode()
    rospy.spin()
