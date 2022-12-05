# ndvi_project
This project calculates NDVI(Normalized Difference Vegetation Index) and GNDVI(Green Normalized Difference Vegetation Index) from multispectral(5bands) images of leaves.
NDVI and GNDVI are indexes that show greeness of the plant which can be interpreted as tree nutrition.
   
Requirements:   
Test Was done on Ubuntu 18.04 OS and python 3.6, but will work on any OS and python3++.   
 Ubuntu 18.04   
 Python 3.6   
 Micasense RedEdge-MX camera

# Installation
1. Clone this repo   
2. Put calibration panel images in /data/calibration_panels   
3. Put images of plant(leaves) in /data/leaves_data   
4. Check line 19, 62, 107 in main.py   

# Instructions
## Set up
1. Amount of pixel values to translate for image registration were decided based on the data we had. 
You will need to find optimal values for your own dataset as well for registration and update the values. 
You can change this by either chaning default value in class definition in process_multi_images.py - AlignImages() or 
by instantiating an object with different values in main.py   
2. Calibration was done following Micasense RedEdge camera calibration instructions, 
if you are using different camera, please follow your own manufacturer's instruction. 
You need to find location of the calibration panel in your panel image and get coordinates of corners of the panel.   
Update this by either changing default values in class definition in calibration.py - Calibrate() or by instantiating an object 
with different values in main.py   
## Run
In terminal, cd to ~/ndvi_project/scripts and run      
python main.py
