# Birdview Map
## 1. Introduction to files
```slicer.py```</br></br>
Take a depth image (npy format, examples in "samples" folder) as input, reduce its resolution (from 1280\*720 to 128\*72), slice the image every (0.5) meters into N pieces, and return the 3-d numpy array (128\*72\*N) </br></br>
```image2birdview.py```</br></br>
Import from ```slicer.py```, process the returned numpy array based on our realsense camera's [physical specs](https://click.intel.com/intelr-realsensetm-depth-camera-d435.html) (intel realsense model d435). It compresses each slice (128\*72) into a 1-d array (length 128). Eventually the arrays are combined as one (128\*N) birdview map. </br>
## 2. How to use
For demostration use, put ```slicer.py``` and ```image2birdview.py``` together with a npy file, change the path in ```slicer.py``` and run ```image2birdview.py```.</br>
