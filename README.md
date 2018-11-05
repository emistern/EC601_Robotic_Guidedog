# EC601_Robotic_Guidedog
Repository for EC601 Project: Robotic Guide dog

## Abstract

For people who are visually impaired or blind there are only two options currently available to allow them to navigate the world independently:
1. White Cane
2. Guide Dog

The main purpose of both items is to help a user avoid obstacles as they navigate from a starting position to a goal location. The high level path planning, (i.e. knowing what streets to walk down to get to a location) is done by the user, while the lower level path planning, (i.e. avoiding obstacles in the immediate path) is done by the Cane or dog. However, both of these options require the use of the user’s hand leaving them with only one free hand to use while they are navigating through their life. Additionally, the Cane, although only a few hundred dollars [1], protects a user from obstacles solely on the ground while a Guide dog, (costs: $50,000 + $1500/year [2]), can protect a user from obstacles between the ground and the height of the user. A new product that offers a user similar capabilities of a guide dog for a much lower price, and most importantly giving the user use of both hands, is needed to disrupt this environment.

The device will help a user safely and independently navigate the world in a care-free and hands-free environment. It will be powered by a depth camera and a small computer for image processing, path planning, and object detection. The depth camera will serve two purposes:
1. Detect distance to obstacles using depth data
    The depth data will be sliced into layers, (each layer represents the average step a user will take), and then each             layer will be discretized into 0 for free space and 1 for an obstacle. 
2. RGB data for object detection using neural network
    A neural network will be used to detect an object (either a door or a chair) in the RGB data and then the location of           that object will be passed to the path planning algorithm as the goal for the user.

The device will be used in two ways:
1. Infinite Free Forward: if the user wants to walk freely the goal will be set to the farthest free location on the            discretized map in front of them
2. Walk to object: The location of a specified object will be passed to the path planning alogirthm as the goal. If there       are many objects available then the program will return 1 of the objects and if no objects are available the device will        command the user to rotate, which will effectively scan a different part of the room for the object.

The path planning algorithm defaults the goal location to the infinitely farthest free location in front of them unless a   goal from the object detection algorithm passes in a goal location. Currently, the team is testing between the efficiency/performance of two path planning algorithms: 
1. Dijkstra
2. A*

The interaction between the user and the device goes in two directions:
1. User to Robot: the user will tell the device if they want to walk to an object
2. Device to User: the device will communicate to the user what path to take via sound. 
Currently, the team is testing different means of communication between the device and the user.


[1] Kathy Austin. White cane vs. guide dog: Why or why not? @ONLINE, September 2016. 
[2] Colby Morita. How much does a guide dog cost? @ONLINE, September 2017.

### Assumptions
1. The device will be teseted in a small classroom with no windows or objects on the walls. There will only be a door, chairs, and people in the room.
2. The device will not handle mirrors or glass doors.
3. The device will only detect door frames for the purpose of the semester long project


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
5. For voice interface
   * use sox to play audio

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
    For a depth frame image, we separate it into several images of different length ranges (e.g. 0.25 m-0.75 m, 0.75 m-1.25 m). Each slice is compressed vertically into an array. The image below shows the birdview map made of 10 slices.
    
    <img src="images/squeeze_demo.jpeg" height=300>

    ```
    cd [EC601_ROBOTIC_GUIDEDOG]/wall_detection
    python image2birdview.py
    ```
    
3. Path Planning on Depth Data(Develop)
   
   Performing path planning on depth data. You can change the **dep_mat_fn** variable in **wrapper.py** to test on different depth images.

   Before you can run the wrapper, please complie the cython code first with
   ```
   cd [EC601_ROBOTIC_GUIDEDOG]/wall_detection # where you can find the setup.py
   python setup.py build_ext --inplace  # compile the cython code
   ```
   Then you can run it

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
    python voice_class.py
    ```
    The voice interface requires python playsound module. You can install this by pip(3) install playsound.
