#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 20:56:49 2023

@author: Mohammad Asif Zaman

Adaptive thresholding for 16 bit images
"""

import numpy as np
import matplotlib.pylab as py
import cv2
import time


st_t = time.time()






py.close('all')

path_main = 'Data/'
folder = ['M1']
path_full = path_main + folder[0] + '/E.tif'        # full path

img = cv2.imread(path_full, cv2.IMREAD_UNCHANGED)     
imb = cv2.medianBlur(img, 5) 
bmx = np.max(imb)
bmn = np.min(img)

py.subplot(3,1,1)
py.imshow(img)
py.clim(bmn,bmx)
py.title('orginal 16 bit')

py.subplot(3,1,2)
py.imshow(imb)
py.clim(bmn,bmx)
py.title('blurred image')





imgM = np.array(imb)
Nr,Nc = imgM.shape

# pad = 20
# for m in range(Nr):
#     pylow = max(0,m-pad)
#     pyhigh = min(m+pad, Nr-1)
    
#     for n in range(Nc):
#         pxlow = max(0,n-pad)
#         pxhigh = min(n+pad, Nc-1)
        
block_size = 41
const_C = -50
th_avg_fct = 0.1    # percentage more than the block_mean required to be considered an object
pad = int((block_size-1)/2)

zero_M = np.zeros(imgM.shape)
mask = np.zeros(imgM.shape)
mask2 = np.zeros(imgM.shape)


# block_M = np.ones((block_size,block_size))
        
# https://stackoverflow.com/questions/53124061/how-can-i-add-a-small-matrix-into-a-big-one-with-numpy     

# for m in range(Nr):
#     pylow = max(0,m-pad)
#     pyhigh = min(m+pad, Nr-1)
    
    
    
#     for n in range(Nc):
#         pxlow = max(0,n-pad)
#         pxhigh = min(n+pad, Nc-1)
        
#         # zero_M[pylow:pyhigh,pxlow:pxhigh] = 1
#         block_mean = np.mean(imgM[pylow:pyhigh,pxlow:pxhigh])
#         avg[m,n] = block_mean
#         if imgM[m,n] > block_mean - const_C:
#             mask[m,n] = 1
 

# I ended up redescovering cv2.blur() function
# note that block averaging is the same as 2D convolution/filter with an appropriate kernel. While the nested loops are slow, 
# built-in convolution/filter functions are fast. The cv2.blur() funciton is basically a filter with averaging kernel.

blur_avg = cv2.blur(imb,(block_size,block_size))
mask = imgM > (blur_avg - const_C)
mask2 = imgM > (1+th_avg_fct)*blur_avg 

# img_avg = cv2.blur()        
 

# ysize = block_size
# xsize = block_size
# m = Nr-1
# n = 0


# pylow = max(0,m-pad)
# pyhigh = min(m+pad, Nr-1)
   
# pxlow = max(0,n-pad)
# pxhigh = min(n+pad, Nc-1)

# zero_M[pylow:pyhigh,pxlow:pxhigh] = 1

# # if m < pad:
# #     ysize = ysize - (pad-m)-1

# # if n < pad:
# #     xsize = block_size - (pad-n)-1
    


# block_M = np.ones((ysize,xsize))
# zero_M = np.zeros(imgM.shape)
# zero_M[m:m+ysize, n:n+xsize] += block_M   
       
bbmx = np.max(blur_avg)
bbmn = np.min(blur_avg)

        
py.subplot(3,1,3)
py.imshow(blur_avg)

py.figure()
py.subplot(2,1,1)
py.imshow(mask)


py.subplot(2,1,2)
py.imshow(mask2)

# py.clim(bmn,bmx)
# py.title('orginal 16 bit')
        
        
        
el_t = time.time()- st_t
print('\nRun time = %.1f sec \n' % el_t)


