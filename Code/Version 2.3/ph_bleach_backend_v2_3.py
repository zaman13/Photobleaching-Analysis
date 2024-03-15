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

Dec. 18, 2023
    - Implemented new adaptive thresholding algorithm that works on 16 bit Tif images directly (without needing 8 bit down conversion)
    - Made a more efficient mask_fragment function. No longer saving submasks of each detected object (to save memory)
    - Added log file to record run data
    - Bug fixes: moved savefigure outside the for loop. This bug was slowing down the code. 

    - Added exponential curve fitting y = a.exp(-bx) + c
    - Added NaN handling in mean_store array 

Jan 14, 2024
    - Added new parameter t_final to set/limit the final time. This allows time cropping.
    - Added a fail safe steps in case of curve fitting fail. May need more work.
    
March 14, 2024
    - Added calculation of statistics (mean, mode, median, max, min) for the masked region and background region    
    
"""

import numpy as np
import matplotlib.pyplot as py
import cv2
import pandas as pd 

from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
from scipy import stats

from PIL import Image as PIL_Image


from skimage import measure
import time
import datetime
import os




def main_run(path, dt, t_final, exprt_data, obj_detect_each_frame, th_factor, mean_th_fct, blur_order, block_size, obj_size_th_factor, th_type,
         smooth_data, savgol_window, savgol_order, test_img_ind, dpi_fig):        
    st_t = time.time()
    
    
    py.close('all')
    
    path_dir = os.path.dirname(path) + '/'   # Just get the path directory. This information is needed when writing log files
    
    # =============================================================================
    # Parameters of the tiff image
    # =============================================================================
    # path = "Data/Cy5 C/Time Series_2_Red_0-4000_300ms_4.tif"   # load tiff image sequence
    # path = "/home/asif/Photobleach_data/C_20s/C_20s.tif"   # load tiff image sequence
    # path = "/home/asif/Photobleach_data/M_15s.tif"   # load tiff image sequence
    
  
    frame_count = PIL_Image.open(path).n_frames      # find the number of frames of the tif file (the maximum number of frames that can be processed)
    
    
    N_frame_req = int(t_final/dt)    # requested number of frames for processing
    
    N_frames = min(frame_count,N_frame_req)   # set the number of frames for processing 
    
    t = np.arange(0, N_frames*dt,dt)    # define time array
  
    # =============================================================================
    
    
    
    
    

    
    
    
    # =============================================================================
    # initialize empty lists/arrays
    # =============================================================================
    images = []                                  # List to store the loaded image
    mean_store = np.zeros(N_frames)              # empty array to store mean bead intensity values
    
    im_m_mean, im_m_median, im_m_mode, im_m_min, im_m_max = np.zeros((5, N_frames))
    bck_mean, bck_median, bck_mode, bck_min, bck_max = np.zeros((5, N_frames))
    # =============================================================================
    
    
    
    
    
    # =============================================================================
    # Function for logging console output to file
    def print_log( *args):
        file = open(path_dir + 'log.txt','a')
        toprint = ' '.join([str(arg) for arg in args]) 
        print(toprint)
        toprint = toprint + '\n'
        file.write(toprint)
        file.close()
    # =============================================================================
    
    
    # =============================================================================
    def calc_stats(img1):
        
        t_vals, t_counts = np.unique(img1, return_counts=True)   # count and list the number of unique entries. Needed for calculating mode.
        
        i_min = np.min(img1)                        # min of the masked region
        i_max = np.max(img1)                        # max of the masked region
        i_mean = np.mean(img1)                      # mean of the masked region
        i_median = np.median(img1)                  # median of the masked region
        i_mode = t_vals[np.argwhere(t_counts == np.max(t_counts))]  # mode of the masked region
            
        # Make sure i_mode retruns only one value. i.e., i_mode[0]
        return i_mean, i_median, i_mode[0], i_min, i_max
    
    
    # =============================================================================
    
    # Curve fitting function
    def fitting_func(x, a, b, c):
        return a * np.exp(-b * x) + c
    
    # =============================================================================
    # Function to define image mask
    
    # simple mask find function
    
    def simple_threshold(img):
        im_temp = img                             # input image matrix
        im_blur = cv2.medianBlur(im_temp, blur_order)      # Blurring to reduce noise during boundary/mask creation
        mx = np.max(im_blur)
        mn = np.min(im_blur)
        th = mx*th_factor                         # Threshold value for finding bead mask
        im_mask = (im_blur > th)                  # bead mask
        return im_mask
    
    
    def adaptive_threshold_16bit(img, blur_order, block_size, mean_th_fct):
        
        imb = cv2.medianBlur(img, blur_order)  # blur image to get rid of noise and hot pixels
        imgM = np.array(imb)
        # =========================================================================
        # Calculate block average
        # =========================================================================
        # The cv2.blur() funciton is basically a filter with averaging kernel.
        # https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html#gsc.tab=0
        blur_avg = cv2.blur(imb,(block_size,block_size)) 
        # =========================================================================
        # mask = imgM > (blur_avg - const_C)
        
        mask = imgM > ((1+mean_th_fct)*blur_avg) 
        return mask
    
    def object_mask_find(img):
        # block_size = 41
        # blur_order = 5
        # mean_th_fct = 0.2    # percentage more than the block_mean required to be considered an object
        
        if th_type == 'simple':
            print_log('Simple thresholding')
            return simple_threshold(img)
        if th_type == 'adaptive16bit':
            print_log('Adaptive 16bit thresholding')
            return adaptive_threshold_16bit(img, blur_order, block_size, mean_th_fct)
    
    
    
    
    # =============================================================================
    # Function to split/fragment the image mask into individual submasks, each submask 
    # corresponding to one object 
    # =============================================================================
    
    # =============================================================================
    def mask_fragment_eff(img,obj_size_th_factor):
        # Dec. 18, 2023
        # more efficient and simplified form of the mask_fragment() function. Note that storing the submasks for each object is 
        # not needed for the current application. Each object in the frame isn't independently measured. Instead, we measure the
        # average of all the objects. Hence, we don't calculate the submasks, which decreases memory requirement.
        # original mask_fragment() function can be found in version 1.8 (and likely lower)
        
        
        # NoteL The input of the function is the binary image mask. img has to be binary valued matrix.
        # The function checks the sizes (area) of all the detected objects and filters out the small ones
        
        
        #https://stackoverflow.com/questions/49771746/numpy-2d-array-get-indices-of-all-entries-that-are-connected-and-share-the-same
    
        img_labeled = measure.label(img, connectivity=1)
        
        idx = [np.where(img_labeled == label)
               for label in np.unique(img_labeled)
               if label]
      
        N_obj = len(idx)   # number of objects found
        print_log('\nNumber of objects identified, N_obj = %i' %(N_obj))   
        
        if N_obj == 0:
            print_log('Returning orignial mask without refinement (likely a zero mask)')
            return img
        
        # bboxes = [area.bbox for area in measure.regionprops(img_labeled)]
        
        
        uu = np.zeros(np.shape(img)) # numpy image array
     
        
        
        
        
        obj_size_sum = np.zeros(N_obj)     # initialization. The array will store size of each submask.
        
        # calculate all the object sizes
        for m in range(N_obj):             # loop through each object
            uu = uu*0                      # reset uu array for reuse
            uu[idx[m]] = 1                 # populate uu   
            obj_size_sum[m] = np.sum(uu)   # size of the object. Defined by the number of ones.
            
        
        
        # Once we have splitted the mask into submasks for individual objects, we can
        # start checking the size of each object independently. If a detected object
        # is too small, we can neglect it. We start by setting a threshold object size.
        # Then we refine our submask set and only pick the submasks that are larger in size
        # than the threshould value. Once that is done, we recombine the submasks to find
        # a new refined composite mask. 
        
        obj_size_sum_th = np.max(obj_size_sum)*obj_size_th_factor        # threshold value for object size (i.e. threshold size)
        N_obj_refined = sum(obj_size_sum > obj_size_sum_th)              # find the number of objects having length larger than threshold size
    
        print_log('Number of objects refined, N_obj_refined = %i' %(N_obj_refined))
    
        mask_refined = np.zeros(np.shape(img))   # initialize composite mask from refined sub-masks 
        # py.figure()
        
        counter = 0
        for m in range(N_obj):   # loop over all objects
            
            if obj_size_sum[m] > obj_size_sum_th:   # for objects that meet threshold size
                uu = uu*0                      # reset uu array for reuse
                uu[idx[m]] = 1                 # populate uu   
                
                mask_refined = mask_refined + uu # superimpose on the refined mask
                 
                # note that mask refined is still a binary matrix as the sub_masks do not overlap (no element will be larger than one)
            
                # py.subplot(3,int(np.ceil(N_obj_refined/3)),counter+1)
                # py.imshow(sub_masks_refined[:,:,counter])
                # py.axis('off')
                             
                counter = counter + 1
        
        return mask_refined
    
    # =============================================================================
    
    
    # =============================================================================
    # Load image 
    # =============================================================================
    
    ret, images = cv2.imreadmulti(mats=images,
                                  filename=path,
                                  start=0,
                                  count=frame_count,
                                  flags = 2)             # the flags variable is important!
    
    N_plot_row = int(np.sqrt(N_frames))
    # =============================================================================
    
    
    
    
    
    bck = np.mean(images[frame_count-1])       # estimation of background intensity level (assuming the last frame is only background)
    
    
    
    # =============================================================================
    # print_log header
    # =============================================================================
    now = datetime.datetime.now()
    print_log('******************************************************************')
    print_log('******************************************************************')
    print_log(now)
    print_log('******************************************************************')
    print_log('******************************************************************')
    
    
    
    print_log('* Taking last frame as the background')
    print_log('* Total number of frames = %i' % frame_count)
    print_log('* Number of frames to be processed = %i' % N_frames)
    print_log('* Time step = %1.2f minutes' % dt)
    print_log('* Total duration = %1.2f minutes' % (frame_count*dt))
    print_log('* Duration analyzed= %1.2f minutes' % (N_frames*dt))
    
    print_log('Object detect in each frame = %r' %obj_detect_each_frame)
    print_log('Export data = %r' %exprt_data)
    
   
    print_log('Thresholding type = %s' % th_type) 
    print_log('Threshold factor (for simple thresholding)= %1.2f' % th_factor)
    print_log('Blur order = %i' % blur_order)
    print_log('Block size (for adaptive thresholding) = %i' % block_size)
    print_log('Mean threshold factor (for adaptive thresholding) = %1.2f' % mean_th_fct)
   
    print_log('Smooth data = %r' %smooth_data)
    print_log('Savgol window (for smoothing) = %i' %savgol_window)
    print_log('Savgol order = %i' %savgol_order)
    
    
    print_log('Object size thresholding factor (for mask refinement) = %1.6f' % obj_size_th_factor)
    
    print_log('* Setting object intensity threshold to be %i%%  of maximum \n' % (100*th_factor))
    print_log('* Using %i rows to display the frames in the subplots' %N_plot_row)
    print_log('* Colorbar limit in subplot images: min = 0, max = %i' %np.max(images[0]))
    print_log("\n# =============================================================================\n\n")
    # =============================================================================
    
    
    
    
    # =============================================================================
    # Loop over the image frames to find mean-intensity of detected object
    # =============================================================================
    
    
    # find the mask of the first image and then find the corresponding fragments. Putting this outside the for loop should help with speed when obj_detect_each_frame = False
    im_mask = object_mask_find(images[0])                # object mask determined from first frame
    # smasks, smasks_f, mask_r = mask_fragment(im_mask)    # mask fragment and composite reforming
    mask_r = mask_fragment_eff(im_mask,obj_size_th_factor)    # mask refinement
    
    if N_frames >= 1:
        
        for im_ind in range(N_frames):
     
            # Dynamic name
            name = 'Image'+str(im_ind)
     
            # Shape of Image
            print_log(name, 'Shape :', images[im_ind].shape)
    
            im_temp = images[im_ind]                                 # take one image 
            
            
                    
            # in case independent object detection in each frame is needed, then im_mask and fragments are recalculated
            if obj_detect_each_frame == True:
                im_mask = object_mask_find(images[im_ind])           # object mask determined from current
                # smasks, smasks_f, mask_r = mask_fragment(im_mask)    # mask fragment and composite reforming
                mask_r = mask_fragment_eff(im_mask,obj_size_th_factor)    # mask refinement
    
                
            im_mask = mask_r                         # use refined mask
            
            N_pixel = sum(sum(im_mask))              # number of pixels in the mask
            
            im_temp = images[im_ind]*im_mask         # mask the bead and turn everything else to zero
            im_bck = images[im_ind]*(im_mask < 1)    # mask the background and turn everything else to zero
           
            ind_nonzero = np.nonzero(im_temp)        # find indices of all nonzero elements in the masked image
            ind_bck = np.where(im_temp == 0)         # find indices of all zero elements in the masked image. This should be the indices of the background image
            
            
           
            
            t_vals, t_counts = np.unique(im_temp[ind_nonzero], return_counts=True)   # count and list the number of unique entries. Needed for calculating mode.
            
            # im_m_min = np.min(im_temp[ind_nonzero])                        # min of the masked region
            # im_m_max = np.max(im_temp[ind_nonzero])                        # max of the masked region
            # im_m_mean = np.mean(im_temp[ind_nonzero])                      # mean of the masked region
            # im_m_median = np.median(im_temp[ind_nonzero])                  # median of the masked region
            # im_m_mode = t_vals[np.argwhere(t_counts == np.max(t_counts))]  # mode of the masked region
          
            
            im_m_mean[im_ind], im_m_median[im_ind], im_m_mode[im_ind], im_m_min[im_ind], im_m_max[im_ind] = calc_stats(im_temp[ind_nonzero])
            bck_mean[im_ind], bck_median[im_ind], bck_mode[im_ind], bck_min[im_ind], bck_max[im_ind] = calc_stats(im_bck[ind_bck])
            
            # mean is calculated using 2 ways for cross-checking.
            mean_store[im_ind] = sum(sum(np.asfarray(im_temp)))/N_pixel            # find the mean value of the masked region (bead)
            
            
            print_log('Mean = %1.2f'  % mean_store[im_ind])
            print_log('Bck (estimate) = %1.2f'  % bck)
            print_log('Img:: Mean = %1.2f, Median = %1.1f, Mode = %i, Min = %i, Max = %i'  % (im_m_mean[im_ind],im_m_median[im_ind],im_m_mode[im_ind],im_m_min[im_ind],im_m_max[im_ind]))
            print_log('Background:: Mean = %1.2f, Median = %1.1f, Mode = %i, Min = %i, Max = %i'  % (bck_mean[im_ind],bck_median[im_ind],bck_mode[im_ind],bck_min[im_ind],bck_max[im_ind]))
            print_log('\n')
            
            # print_log('Mean = %1.2f'  % np.mean(im_temp[ind_nonzero]))
            
            # print_log('Median = %1.2f'  % np.median(np.asfarray(im_temp)))

            # =============================================================================
            # Displaying the image
            # =============================================================================       
            py.figure(1)
            
            py.subplot(N_plot_row,int(np.ceil(N_frames/N_plot_row)),im_ind + 1)
            py.imshow(im_temp)   # show masked region
            # py.imshow(im_bck)     # show background region
            # py.imshow(im_mask)
            # py.clim([0,np.max(images[0])])
            py.axis('off')
            # py.savefig(path[0:-3] + 'mask.png',dpi = dpi_fig)  # this savefigur in side the loop was slowing down the code immensely
    
            # =============================================================================
    
    else:
        print_log('Not enough frames. N_frames = %i. Cannot process.' %N_frames) 
    
    # Save figure (mask of each frame plotted in a grid in the above for loop.)
    py.savefig(path[0:-3] + 'after_masking.png',dpi = dpi_fig)    
    
    # =============================================================================
    # NaN handling
    # =============================================================================
    mean_store= np.nan_to_num(mean_store, nan = min(mean_store))   # replaces NaN with minimum value of the array.  https://numpy.org/doc/stable/reference/generated/numpy.nan_to_num.html
    # =============================================================================
    
    
    
    # =============================================================================
    # Data smoothing
    # =============================================================================
    sm_data = mean_store
    if smooth_data == True:
        sm_data = savgol_filter(mean_store, savgol_window, savgol_order)           # data smoothing (needs a moderate number of data points. Skipped for short data chains)
    
    sm_data_norm = sm_data/max(sm_data)
    mean_store_norm = mean_store/max(mean_store)
    # =============================================================================
    
    # =============================================================================
    # Curve fitting
    # =============================================================================
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    popt = [0,0,0]  # set a default value in case the interpolation fails
    try:
        popt, pcov = curve_fit(fitting_func, t, mean_store_norm)
        print_log('Exponential fit y = a.exp(-bx) + c with parameters , a = %1.3f, b = %1.3f, c = %1.3f' %(popt[0],popt[1],popt[2]))
        print_log('Decay rate, b = %1.3f a.u/min' %popt[1])
    except:
        print_log('Error. Could not perform curve fitting.')
    # =============================================================================
    
    # =============================================================================
    # Export data
    # =============================================================================
    if exprt_data == True:
        Mdata = np.transpose([t,sm_data, sm_data/np.max(sm_data), im_m_mean, im_m_median, im_m_mode, im_m_min, im_m_max, bck_mean, bck_median, bck_mode, bck_min, bck_max])
        col_names = ['time (min)','intensity', 'normalized intensity', 'im_m_mean', 'im_m_median', 'im_m_mode', 'im_m_min', 'im_m_max', 'bck_mean', 'bck_median', 'bck_mode', 'bck_min', 'bck_max']
        df = pd.DataFrame(Mdata,columns=col_names)
        df.to_csv(path[0:-3] + 'csv', index = False)
    # =============================================================================
    
    
    # =============================================================================
    # Plotting
    # =============================================================================
    py.figure()
    # py.figure(dpi=1200)               # Set this dpi when saving figure. Turn OFF if screen display causes issue
    py.plot(t,mean_store,'.',label='Bead intensity raw data',markersize = 4)
    py.plot(t,sm_data,'r',label='Bead intensity curve')
    py.plot(t, np.ones(len(t))*bck,'k--', label = 'background level')
    
    
    
    py.title('Photobleaching data')
    py.xlabel('time, t (min)')
    py.ylabel('Intensity (a.u.)')
    py.legend()
    py.savefig(path[0:-3] + 'rate.png', dpi = dpi_fig)
    
    
    py.figure()
    py.plot(t,mean_store_norm,'.', label = 'Normalized raw data')
    py.plot(t, fitting_func(t, *popt), 'r', label = 'Exponential function fitting')
    
    st1 = 'y = a.exp(-bx) + c'
    st2 = ',  a = ' + str(round(popt[0],2)) + ', b = ' + str(round(popt[1],2)) + ', c = ' + str(round(popt[2],2))
    
    py.xlabel('time, t (min)')
    py.ylabel('Intensity (a.u.)')
    py.title(st1 + st2)
    py.legend()
    py.savefig(path[0:-3] + 'normalized_rate.png', dpi = dpi_fig)
    
    # =============================================================================
    
    # =============================================================================
    # Plot test image
    # =============================================================================
    
    im = images[test_img_ind]
    im_mask = object_mask_find(im)
    mask_r = mask_fragment_eff(im_mask,obj_size_th_factor)    # mask refinement
    
    # plot raw image
    # py.set_cmap('viridis')
    py.figure()
    py.subplot(2,2,1)
    py.imshow(im)
    py.title('Image')
    py.clim([bck-100,np.max(im*mask_r)])
    py.axis('off')
    
    # plot image mask
    # py.set_cmap('gray')
    py.subplot(2,2,2)
    py.imshow(im_mask)
    py.title('Mask')
    py.axis('off')
    
    # plot refined image mask
    py.subplot(2,2,3)
    py.imshow(mask_r)
    py.title('Refined mask')
    py.axis('off')
    
    # plot image after masking
    py.subplot(2,2,4)
    py.imshow(im*mask_r)
    py.title('Image after masking')
    py.clim([bck-100,np.max(im*mask_r)])
    py.axis('off')
    py.savefig(path[0:-3] + 'test_frame.png', dpi = dpi_fig)
    
    # =============================================================================
    
    
    el_t = time.time()- st_t
    print_log('\nRun time = %.1f sec \n' % el_t)
    
    return 0


