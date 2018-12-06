import cv2
import PIL
import json
import numpy as np
from imgutil import decodejpg
import paho.mqtt.client as mqtt

class ImageClient(object):

    def __init__(self, ):

        broker_address="broker.hivemq.com"
        self.topic_color = "RoboticGuideDog/image/color"

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect

        self.client.on_message = self.on_frame_decode #self.on_display_frame

        self.client.connect(broker_address)        
        #self.client.subscribe(self.topic_color)

        self.client.loop_forever()

    def on_display_frame(self, client, user, msg):

        data = json.loads(msg.payload)

        frame = np.array(data, dtype = np.uint8)

        try:
            cv2.imshow("image", frame)

            cv2.waitKey(10)

            cv2.imwrite("debug.jpg", frame)
        except Exception as e:
            print (e)

    def on_frame_decode(self, client, user, msg):

        frame = decodejpg(msg.payload)

        try:
            cv2.imshow("image", frame)

            cv2.waitKey(10)

            cv2.imwrite("debug.jpg", frame)
        except Exception as e:
            print (e)

    def on_connect(self, client, userdata, flags, rc):
        print("connected with result code " + str(rc))
        client.subscribe(self.topic_color)

if __name__ == "__main__":

    client = ImageClient()