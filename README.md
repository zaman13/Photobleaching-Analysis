# Photobleaching Analysis Through Image Processing

<p float="left">
<a href = "https://github.com/zaman13/Photobleaching-Analysis/tree/main/Code"> <img src="https://img.shields.io/badge/Language-Python-blue" alt="alt text"> </a>
<a href = "https://github.com/zaman13/Photobleaching-Analysis/blob/main/LICENSE"> <img src="https://img.shields.io/badge/License-MIT-green" alt="alt text"></a>
<a href = "https://github.com/zaman13/Photobleaching-Analysis/tree/main/Code"> <img src="https://img.shields.io/badge/Version-2.0-red" alt="alt text"> </a>
</p>


<img align = "right" src="https://github.com/zaman13/Photobleaching-Analysis/blob/main/Sample%20output/K_15s.test_frame.png" alt="alt text" width="460">


The code analyzes photobleaching from a timeseries image TIF image (single image file with multiple frames). Such a TIF file can be generated from a sequence of image files using standard software (i.e., ImageJ). 

The photobleaching code can process a tiff image stack and detect bright objects of arbitrary size and shape. It can calculate the brightness/intensity of those objects in each frame and produce a intensity vs time plot. The code can be used to analyze photobleaching rate. 

# Features of the photobleach analysis code
- Can handle multiple objects in a frame
- Can handle irregularly shaped objects
- Can dynamically adjust the mask every frame to account for object drift
- Average birghtness of all the detected beads in the frames are calculated

## Photobleaching:

The following figure shows the average fluorescence intensity vs time plot. A time series image set containing multiple beads is used as the input data. 

  <img src="https://github.com/zaman13/Photobleaching-Analysis/blob/main/Sample%20output/K_15s.rate.png" alt="alt text" width="600">
   <img src="https://github.com/zaman13/Photobleaching-Analysis/blob/main/Sample%20output/K_15s.normalized_rate.png" alt="alt text" width="600">


## Acknowledgement
This work was developed at the Hesselink research lab, Stanford University. The work was partially supported by the National Institute of Health (NIH) Grant R01GM138716 and 5R21HG009758.
