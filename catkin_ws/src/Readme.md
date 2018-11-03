# ROS nodes wrapping our Robot Guide Dog

We are trying to use Robotic Operating System to wrap all our modules into an integrated system. This folder contain most of the nesessary nodes used by our system. Addition native nodes offered by the ROS community may also be used. Typically these community nodes can get through installing community packages.

## Node List

    0. pkg_name

        Template node for building other nodes.
    1. realsense2_camera

        Realsense camera driver ROS wrapper, aquired from community:
        http://wiki.ros.org/realsense2_camera
    2. rosyolo(archived)

        A ROS node wrapped a tiny-YOLO neural network deployed on Intel Movidius Neural Computing Stick. For running this node, you need to have NCS plugged in you machine, and driver for NCS(NCSDK) installed on your machine.
    3. rtabmap_ros

        A ROS node wrapped realtime appearence-based mapping. 
        after install the standalone version of rtbamap, please remember to export the rtbamap_dir for compiling rtabmap_ros node:

        ```
            export RTABMap_DIR=~/rtabmap/build    # assuming you install the standalone version rtabmap in your root directory.
        ```