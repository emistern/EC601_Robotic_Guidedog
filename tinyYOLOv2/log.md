## Decision Engine

Date: 9/30/2018

Hack on top of tinyYOLO, build a simple algorithm to find freespace based on object detection result.

Files: dev.py

Date: 10/2/2018

Refactor previous hack code into: 1. video testbench for decision algorithm; 2. decision engine class

Idea: Decision engine code should be separated from detection code. Encpsulate detection code into testbench.

Files: decisionTestbench.py, decisionEngine.py