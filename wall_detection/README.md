# Birdview Map
## 1. Introduction to files
```slicer.py```</br></br>
Take a depth image (npy format, examples in "samples" folder) as input, reduce its resolution, slice the image every (0.5) meters into N pieces, and return the 3-d numpy array </br></br>
```image2birdview.py```</br></br>
Import from ```slicer.py```, process the returned numpy array based on our realsense camera's [physical specs](https://click.intel.com/intelr-realsensetm-depth-camera-d435.html) (intel realsense model d435). It compresses each slice into a 1-d array. Eventually the arrays are combined as one birdview map. </br>
## 2. How to use
For demostration use, put ```slicer.py``` and ```image2birdview.py``` together with a npy file, change the path in ```slicer.py``` and run ```image2birdview.py```.</br>
