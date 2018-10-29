# EC601_Robotic_Guidedog
Repository for EC601 Project: Robotic Guide dog

## Contents

1. Object Detection in RGB color image using neural network
2. ad-hoc decision algorithm to generate directional instruction
3. utilities for processing and storing depth data obtained from Intel RealSense RGB-D camera.
4. Implementation of Djikstra Algorithm for path planning using depth data
5. Voice user interface.

## Get Started

### Reference Repos: 
* tinyYOLO implementation taken from simo23:tinyYOLOv2 at https://github.com/simo23/tinyYOLOv2

### Software Dependencies:
1. General setup:
    
    The main part of this repo is build and test on **Windows** 10 with **Anaconda3**. On other platforms such as MAC and Linix, code should also work without significant modification.
2. For testing decision algorithm:

    * OpenCV (Build and test with version 3.4.3)
    * TensorFlow (Using Version 1.10.0)
    * (Optional: CUDA 9.0 for using GPU acceleration)
3. For using the Intel RealSense code:

    * OpenCV
    * librealsense (Intel RealSense camera driver, build and test with python wrapper called pyrealsense2. Only needed when you want to read from .bag file)
4. For using path planning:
   
   * OpenCV (Only used for drawing planning result) 

## How things work and Examples

0. System Block Diagram
   
   Three main modules in our system:
   
   * Image Processing and Object Detection module
   * Decision Module
   * User Interface Module 

    <img src="images/block_diagram.png" height=200>
1. Object Detection and Decision Algorithm(Baseline)
   
    The Object Detection module(TinyYOLO Neural Network) find the obstacles in scene, and pass obstacle information to decision algorithm. The decision algorithm generate resonable instruction based on finding the maximum free space in scene.

   <img src="images/decision.jpg" height=200>

    ```
    cd [EC601_ROBOTIC_GUIDEDOG]/tinyYOLOv2
    python decisionTestbench.py
    ```

2. Intel RealSense depth data post-processing

    We are trying to use depth data from Intel RealSense RGB-D camera to imporve the capability of obstacle detection.

    <img src="images/hole_filling.jpg" height=200>

    ```
    cd [EC601_ROBOTIC_GUIDEDOG]/realsense
    python rs_depth_worker.py
    ```

3. Path Planning on Depth Data(Develop)
   
   Performing path planning on depth data. You can change the **dep_mat_fn** variable in **wrapper.py** to test on different depth images.

   ```
    cd [EC601_ROBOTIC_GUIDEDOG]
    python wrapper.py
    ```

   <img src="images/path_plan_with_depth.jpg" height=200>
   
   Path planning to avoid a chair in front of you.

   <img src="images/path_plan_with_depth_1.jpg" height=200>


   Path planning to let you walk straight in freespace.

4. Voice-based User Interface
   
   ```
    cd [EC601_ROBOTIC_GUIDEDOG]/voice
    python voice-class.py
    ```
