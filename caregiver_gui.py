import cv2
import sys
import time
import numpy as np
sys.path.append("./monitor/")
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
        QGridLayout, QGroupBox, QHBoxLayout, QLabel,
        QProgressBar, QPushButton, QRadioButton,
        QVBoxLayout, QWidget)
from PyQt5 import QtGui, QtCore
from monitor.imgutil import decodejpg
import paho.mqtt.client as mqtt

class Caregiver(QDialog):

    def __init__(self, parent=None):
        super(Caregiver, self).__init__(parent)

        startButton = QPushButton("Start", self)
        startButton.clicked.connect(self.startloop)

        self.rgbLabel = QLabel(self)

        topLayout = QHBoxLayout()
        topLayout.addWidget(startButton)
        topLeftLayout = QHBoxLayout()
        topLeftLayout.addWidget(self.rgbLabel)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(topLeftLayout, 1, 0)

        broker_address="broker.hivemq.com"
        self.topic_color = "RoboticGuideDog/image/color"

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect

        self.client.on_message = self.on_frame_decode #self.on_display_frame

        self.client.connect(broker_address)        


    def on_connect(self, client, userdata, flags, rc):
        print("connected with result code " + str(rc))
        client.subscribe(self.topic_color)

    def on_frame_decode(self, client, user, msg):

        frame = decodejpg(msg.payload)

        try:
            self.setImage(self.rgbLabel, frame)
        except Exception as e:
            print (e)

    def setImage(self, label, image):
        height, width, byteValue = image.shape
        byteValue = byteValue * width
		
        qimage = QtGui.QImage(image, width, height, byteValue, QtGui.QImage.Format_RGB888)
        qpix = QtGui.QPixmap(qimage)
        label.setPixmap(qpix)

    def startloop(self):
        
        self.client.loop_forever()


if __name__ == "__main__":
    app = QApplication([])

    gui = Caregiver()
    gui.show()

    sys.exit(app.exec_())