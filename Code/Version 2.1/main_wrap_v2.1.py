#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 18:05:03 2023

@author: Mohammad Asif Zaman

Wrap for the photobleach backend code
"""


from ph_bleach_backend_v2.1 import *
import os



path_dir = '/home/asif/Photobleach_data/'   # directory where the data files are
fname = 'M_15s.tif'
path = path_dir + fname
dt = 15/60                  # time interval between images (unit: minutes)

# =============================================================================
# Control parameter
# =============================================================================
exprt_data = 'y'                  # Export data to csv file y/n
obj_detect_each_frame = False     # if True, then object is detected in every frame. 
                                  # if False, then object is detected in the first frame only
                                  # and is assumed to be stationary if every other frame. Setting False
                                  # might be useful for noisy and low-light image.
                                  
th_factor = 0.6                   # For simple thresholding: Fraction of maximum brightness. Pixels having this brightness fraction is assumed to be part of the object
mean_th_fct = 0.1                 # For 16 bit adaptive thresholding: percentage more than the block_mean required to be considered an object
# N_plot_row = 5                  # Number of rows in the subplot when plotting the detected object at each frame
blur_order = 5                    # Order of the median blur
block_size = 41                   # block size for adaptive thresholding

obj_size_th_factor = 0.1**2       # for composite mask from fragments, size (area) of object to include = max_size * obj_size_th_factor. The square is to convert length to area 
th_type = 'adaptive16bit'         # thresholding function
smooth_data = False                 # Smooth data y/n
savgol_window = 11                # parameters for the smoothing filter
savgol_order = 3                  # parameters for the smoothing filter

test_img_ind = 0                  # test image frame to plot
dpi_fig  = 600                    # dpi of saved figures
# =============================================================================


# # https://note.nkmk.me/en/python-os-basename-dirname-split-splitext/
# dirname = os.path.dirname(path) + '/'
# print(dirname)

main_run(path, dt, exprt_data, obj_detect_each_frame, th_factor, mean_th_fct, blur_order, block_size, obj_size_th_factor, th_type,
          smooth_data, savgol_window, savgol_order, test_img_ind, dpi_fig)


