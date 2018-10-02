## Decision Engine

Date: 9/30/2018

Hack on top of tinyYOLO, build a simple algorithm to find freespace based on object detection result.

Files: dev.py

Date: 10/2/2018

Refactor previous hack code into: 1. video testbench for decision algorithm; 2. decision engine class

Idea: Decision engine code should be separated from detection code. Encpsulate detection code into testbench.

Files: decisionTestbench.py, decisionEngine.py

Adding blob detection module from openCV to the decision algorithm

Idea: Using blob detection to help solving the problem of detection failure when objects only partly shown in image

Link: https://docs.opencv.org/3.4.3/d0/d7a/classcv_1_1SimpleBlobDetector.html

Adding home-made blob detection module using color filtering