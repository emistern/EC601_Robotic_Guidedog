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
from wrapper_for import ModuleWrapper, wrapper_args
from wrapper_det import ModuleWrapperDet, wrapper_args_det

class RDGgui(QDialog):

    def __init__(self, parent=None):
        super(RDGgui, self).__init__(parent)

        self.mode_dict = {
            "infinite forward": (ModuleWrapper, wrapper_args),
            "object detection": (ModuleWrapperDet, wrapper_args_det)
        }

        modeComboBox = QComboBox()
        modeComboBox.addItems(self.mode_dict.keys())
        modeLabel = QLabel("&Mode:")
        modeLabel.setBuddy(modeComboBox)
        modeComboBox.activated[str].connect(self.changeMode)
        startButton = QPushButton("Start", self)
        startButton.clicked.connect(self.startRun)
        stopButton = QPushButton("Stop", self)
        stopButton.clicked.connect(self.stopRun)
        monitorCheckBox = QCheckBox("Monitor", self)
        monitorCheckBox.stateChanged.connect(self.checkMonitor)
        voiceCheckBox = QCheckBox("Voice", self)
        voiceCheckBox.stateChanged.connect(self.checkVoice)
        bagCheckBox = QCheckBox("Bagfile", self)
        bagCheckBox.stateChanged.connect(self.checkBag)
        
        self.progLabel = QLabel("Choose a function.")

        self.rgbLabel = QLabel(self)
        self.depLabel = QLabel(self)
        self.mapLabel = QLabel(self)
        self.dirLabel = QLabel(self)

        topLayout = QHBoxLayout()
        topLayout.addWidget(modeLabel)
        topLayout.addWidget(modeComboBox)
        topLayout.addWidget(startButton)
        topLayout.addWidget(stopButton)
        topLayout.addWidget(monitorCheckBox)
        topLayout.addWidget(voiceCheckBox)
        topLayout.addWidget(bagCheckBox)

        topLeftLayout = QHBoxLayout()
        topLeftLayout.addWidget(self.rgbLabel)

        topRightLayout = QHBoxLayout()
        topRightLayout.addWidget(self.depLabel)

        botLeftLayout = QHBoxLayout()
        botLeftLayout.addWidget(self.mapLabel)

        botRightLayout = QHBoxLayout()
        botRightLayout.addWidget(self.dirLabel)

        botLayout = QHBoxLayout()
        botLayout.addWidget(self.progLabel)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(topLeftLayout, 1, 0)
        mainLayout.addLayout(topRightLayout, 1, 1)
        mainLayout.addLayout(botLeftLayout, 2, 0)
        mainLayout.addLayout(botRightLayout, 2, 1)
        mainLayout.addLayout(botLayout, 3, 0, 1, 2)

        self.setLayout(mainLayout)

        self.run_flag = False
        self.pause_flag = False
        self.monitor_flag = False
        self.voice_flag = False
        self.bag_flag = False

        self.funcName = None

    def changeMode(self, funcName):
        self.funcName = funcName
        self.progLabel.setText(" use " + funcName)

    def startRun(self):
        self.progLabel.setText("start running!")
        wrapper, arg_func = self.mode_dict[self.funcName]
        args = arg_func()
        args.bagfile = self.bag_flag
        args.generator = True
        args.voice = self.voice_flag
        args.monitor = self.monitor_flag
        gen = wrapper(args)
        self.run_flag = True
        while(True):
            disp_col, disp_dep, disp_map, disp_sgn = next(gen)
            disp_dep = np.asanyarray(disp_dep / np.amax(disp_dep) * 255.0).astype(np.uint8)
            disp_dep = cv2.applyColorMap(disp_dep, cv2.COLORMAP_JET)
            disp_dict = {
                self.rgbLabel: disp_col,
                self.mapLabel: disp_map,
                self.dirLabel: disp_sgn,
                self.depLabel: disp_dep
            }
            for lb, img in disp_dict.items():
                rz_img = cv2.resize(img, (240, 160))
                rgb_img = cv2.cvtColor(rz_img, cv2.COLOR_BGR2RGB)
                self.setImage(lb, rgb_img)

            if not self.run_flag:
                break

    def stopRun(self):
        self.progLabel.setText("stop running!")
        self.run_flag = False

    def setImage(self, label, image):
        height, width, byteValue = image.shape
        byteValue = byteValue * width
		
        qimage = QtGui.QImage(image, width, height, byteValue, QtGui.QImage.Format_RGB888)
        qpix = QtGui.QPixmap(qimage)
        label.setPixmap(qpix)

    def checkMonitor(self, state):
        if state == QtCore.Qt.Checked:
            self.monitor_flag = True
        else:
            self.monitor_flag = False

    def checkVoice(self, state):
        if state == QtCore.Qt.Checked:
            self.voice_flag = True
        else:
            self.voice_flag = False

    def checkBag(self, state):
        if state == QtCore.Qt.Checked:
            self.bag_flag = True
        else:
            self.bag_flag = False

if __name__ == "__main__":
    app = QApplication([])

    gui = RDGgui()
    gui.show()

    sys.exit(app.exec_())