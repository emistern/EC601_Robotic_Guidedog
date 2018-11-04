# YOLO and Darknet
## Install
Our model is based on YOLOv3. [Here](https://drive.google.com/open?id=1A3kVcJ_3yT9Oc4f2wEViuWYP0RmlvXmL) is the link for ```darknet```. 
### Prerequisites
If you would like to run with CPU (which is easier for demonstrational use), open makefile in root directory of darknet and change ```GPU=1``` and ```CUDNN=1``` to ```GPU=0``` and ```CUDNN=0```. </br></br>
If you would like to run YOLO with GPU (which is generally way faster than CPU in graphical calculations), you need to install CUDA and nvidia driver. Note that your CUDA version must match your nvidia driver. This could be a painful process for those using old GPUs. If you want it to be even faster, install CUDNN as well and set GPU and CUDNN in makefile to 1. </br>
### Compile
Run 
```
$ make -jx
```
at darknet root directory, where x is the number of CPU cores you would like to run with. You can always run 
```
$ make clean
```
to de-make the files. 
