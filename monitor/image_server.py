import json
import numpy as np
import paho.mqtt.client as mqtt

class ImageServer(object):

    """
    An image publishing server using mqtt protocol
    """

    def __init__(self):

        broker_address="iot.eclipse.org"
        self.topic_color = "RoboticGuideDog/image/color"

        self.client = mqtt.Client()

        self.client.connect(broker_address)

        self.data = None

    def publish(self, image):

        # publish an image using the server
        self.client.publish(self.topic_color, json.dumps(image))

    def on_msg_debug(self, client, user, msg):

        self.data = json.loads(msg.payload)
        print("data: ", np.fromstring(str(msg.payload.decode("utf-8"))))
    
if __name__ == "__main__":

    server = ImageServer()

    server.client.on_message = server.on_msg_debug

    server.client.loop_start()

    server.client.subscribe(server.topic_color)

    server.publish(
                    [[1, 0, 1],
                    [0, 1, 0],
                    [1, 0, 1]]
                    )

    import time

    time.sleep(4)

    server.client.loop_stop()

    data = np.array(server.data) + np.array([[1, 0, 1],
                    [0, 1, 0],
                    [1, 0, 1]])

    print(data)