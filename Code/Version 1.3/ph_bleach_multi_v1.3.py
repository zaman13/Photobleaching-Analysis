# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 21:47:28 2023

@author: Mohammad Asif Zaman

Notes:
    - Background intensity is assumed to be the intensity of the last frame. 
      It is implied that the object is very dim in the last frame so that the frame
      is basically only the background. 

July 13, 2023
    - Added mask_fragment() function to identify objects in a frame individually. The function
      creates submasks for each identified object. 
    - Parameterized the median blur filter order.

July 18, 2023
    - Data export feature added  (using pandas)
    - Count the number of frames of a tiff file automatically rather than pluggin it in manually (PIL library is used for this)
"""

import numpy as np
import matplotlib.pyplot as py
import cv2
import pandas as pd 

from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
from PIL import Image as PIL_Image


from skimage import measure



py.close('all')



# =============================================================================
# Parameters of the tiff image
# =============================================================================
path = "Data/image_2_c1.tif"   # load tiff image sequence
# path = "e1_c2.tif"   # load tiff image sequence
frame_count = PIL_Image.open(path).n_frames      # find the number of frames of the tif file to process

dt = 15/60             # time interval between images


# path = "image_2_c2.tif"   # load tiff image sequence
# frame_count = 120      # define number of frames of the tif file to process
# dt = 55/60             # time interval between images


t = np.arange(0,frame_count*dt,dt)    # define time array
# =============================================================================





# =============================================================================
# Control parameter
# =============================================================================
exprt_data = 'y'                   # Export data to csv file y/n
obj_detect_each_frame = False     # if True, then object is detected in every frame. 
                                  # if False, then object is detected in the first frame only
                                  # and is assumed to be stationary if every other frame. Setting False
                                  # might be useful for noisy and low-light image.
                                  
th_factor = 0.85                  # Fraction of maximum brightness. Pixels having this brightness fraction is assumed to be part of the object

N_plot_row = 5                    # Number of rows in the subplot when plotting the detected object at each frame
blur_order = 5                    # Order of the median blur
obj_size_th_factor = 0.25         # for composite mask from fragments, size of object to include = max_size * obj_size_th_factor 

smooth_data = 'y'                 # Smooth data y/n
savgol_window = 11                # parameters for the smoothing filter
savgol_order = 3                  # parameters for the smoothing filter
# =============================================================================



# =============================================================================
# initialize empty lists/arrays
# =============================================================================
images = []                                  # List to store the loaded image
mean_store = np.zeros(frame_count)           # empty array to store mean bead intensity values
# =============================================================================




# =============================================================================
# Function to define image mask
def object_mask_find(img):
    im_temp = img                             # input image matrix
    im_blur = cv2.medianBlur(im_temp, blur_order)      # Blurring to reduce noise during boundary/mask creation
    mx = np.max(im_blur)
    mn = np.min(im_blur)
    th = mx*th_factor                         # Threshold value for finding bead mask
    im_mask = (im_blur > th)                  # bead mask
    return im_mask

# =============================================================================


# =============================================================================
# Function to split/fragment the image mask into individual submasks, each submask 
# corresponding to one object 
# =============================================================================
def mask_fragment(img):
    # note, function input is the binary image mask. img has to be binary valued matrix.
    
    #https://stackoverflow.com/questions/49771746/numpy-2d-array-get-indices-of-all-entries-that-are-connected-and-share-the-same

    img_labeled = measure.label(img, connectivity=1)
    
    idx = [np.where(img_labeled == label)
           for label in np.unique(img_labeled)
           if label]
  
    N_obj = len(idx)
    print('\nNumber of objects identified, N_obj = %i' %(N_obj))   
    
    # bboxes = [area.bbox for area in measure.regionprops(img_labeled)]
    
    
    uu = np.zeros(np.shape(img))
 
    
    
    
    sub_masks = np.zeros([np.shape(img)[0],np.shape(img)[1],N_obj])
    obj_size_sum = np.zeros(N_obj)
    
    for m in range(N_obj):
        uu = uu*0
        uu[idx[m]] = 1 
        obj_size_sum[m] = np.sum(uu)   # size of the object
        sub_masks[:,:,m] = uu
        
        # py.subplot(3,int(np.ceil(N_obj/3)),m+1)
        # py.imshow(sub_masks[:,:,m])
        # py.axis('off')
    
    # Once we have splitted the mask into submasks for individual objects, we can
    # start checking the size of each object independently. If a detected object
    # is too small, we can neglect it. We start by setting a threshold object size.
    # Then we refine our submask set and only pick the submasks that are larger in size
    # than the threshould value. Once that is done, we recombine the submasks to find
    # a new refined composite mask. 
    obj_size_sum_th = np.max(obj_size_sum)/4

    N_obj_refined = sum(obj_size_sum > obj_size_sum_th)
    print('Number of objects refined, N_obj_refined = %i' %(N_obj_refined))

    sub_masks_refined = np.zeros([np.shape(im_mask)[0],np.shape(im_mask)[1],N_obj_refined])
    mask_refined = np.zeros(np.shape(im_mask))   # composite mask from refined sub-masks (initialization)
    # py.figure()
    counter = 0
    for m in range(N_obj):
        
        if obj_size_sum[m] > obj_size_sum_th:
            sub_masks_refined[:,:,counter] = sub_masks[:,:,m] 
            mask_refined = mask_refined + sub_masks_refined[:,:,counter]
            
        
            # py.subplot(3,int(np.ceil(N_obj_refined/3)),counter+1)
            # py.imshow(sub_masks_refined[:,:,counter])
            # py.axis('off')
            
                        
            counter = counter + 1

    return sub_masks, sub_masks_refined, mask_refined

# =============================================================================




# =============================================================================
# Load image 
# =============================================================================

ret, images = cv2.imreadmulti(mats=images,
                              filename=path,
                              start=0,
                              count=frame_count,
                              flags = 2)             # the flags variable is important!

# =============================================================================





bck = np.mean(images[frame_count-1])       # estimation of background intensity level (assuming the last frame is only background)



# =============================================================================
# Print header
# =============================================================================
print("\n# =============================================================================")
if obj_detect_each_frame == True:
    print('* Detecting object in every frame')
else:
    print('* Detecting object in first frame and assuming it to be stationary')

print('* Taking last frame as the background')
print('* Number of frames = %i' % frame_count)
print('* Time step = %1.2f minutes' % dt)
print('* Total duration = %1.2f minutes' % (frame_count*dt))


print('* Setting object intensity threshold to be %i%%  of maximum \n' % (100*th_factor))
print('* Using %i rows to display the frames in the subplots' %N_plot_row)
print('* Colorbar limit in subplot images: min = 0, max = %i' %np.max(images[0]))
print("\n# =============================================================================\n\n")
# =============================================================================




# =============================================================================
# Loop over the image frames to find mean-intensity of detected object
# =============================================================================


if len(images) >= 1:
    for im_ind in range(len(images)):
 
        # Dynamic name
        name = 'Image'+str(im_ind)
 
        # Shape of Image
        print(name, 'Shape :', images[im_ind].shape)

        im_temp = images[im_ind]         
        if obj_detect_each_frame == True:
            im_mask = object_mask_find(images[im_ind])           # object mask determined from current
            smasks, smasks_f, mask_r = mask_fragment(im_mask)    # mask fragment and composite reforming

        else:
            im_mask = object_mask_find(images[0])          # object mask determined from first frame
            smasks, smasks_f, mask_r = mask_fragment(im_mask)    # mask fragment and composite reforming

            
        im_mask = mask_r                         # use refined mask
        
        N_pixel = sum(sum(im_mask))              # number of pixels in the mask
        
        im_temp = images[im_ind]*im_mask         # mask the bead and turn everything else to zero
        
        
        mean_store[im_ind] = sum(sum(np.asfarray(im_temp)))/N_pixel             # find the mean value of the masked region (bead)

        # =============================================================================
        # Displaying the image
        # =============================================================================       
        py.figure(1)
        py.subplot(N_plot_row,int(np.ceil(frame_count/N_plot_row)),im_ind + 1)
        py.imshow(im_temp)
        # py.imshow(im_mask)
        # py.clim([0,np.max(images[0])])
        py.axis('off')
        
        # =============================================================================

    


sm_data = mean_store
if smooth_data == 'y':
    sm_data = savgol_filter(mean_store, savgol_window, savgol_order)                  # data smoothing (needs a moderate number of data points. Skipped for short data chains)



# Export data

if exprt_data == 'y':
    Mdata = np.transpose([t,sm_data])
    col_names = ['time (min)','intensity']
    df = pd.DataFrame(Mdata,columns=col_names)
    df.to_csv(path[0:-3] + 'csv', index = False)



# =============================================================================
# Plotting
# =============================================================================
py.figure()
# py.figure(dpi=1200)               # Set this dpi when saving figure. Turn OFF if screen display causes issue
py.plot(t,mean_store,'.',label='Bead intensity raw data',markersize = 4)
py.plot(t,sm_data,'r',label='Bead intensity curve')
py.plot(t, np.ones(len(t))*bck,'k--', label = 'background level')



py.title('Bead detection in each frame')
py.xlabel('time, t (min)')
py.ylabel('Intensity (a.u.)')
py.legend()
py.savefig(path[0:-3] + 'png')
# =============================================================================




im = images[4]
im_mask = object_mask_find(im)

smasks, smasks_f, mask_r = mask_fragment(im_mask)

# py.set_cmap('viridis')
py.figure()
py.subplot(1,4,1)
py.imshow(im)
py.title('Image')
py.clim([bck-100,np.max(im*mask_r)])
py.axis('off')


# py.set_cmap('gray')
py.subplot(1,4,2)
py.imshow(im_mask)
py.title('Mask')
py.axis('off')


py.subplot(1,4,3)
py.imshow(mask_r)
py.title('Refined mask')
py.axis('off')


py.subplot(1,4,4)
py.imshow(im*mask_r)
py.title('Image after masking')
py.clim([bck-100,np.max(im*mask_r)])
py.axis('off')


