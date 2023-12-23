#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 18:18:52 2023

@author: Mohammad Asif Zaman
"""

# =============================================================================
# Import ttkbootstrap 
# =============================================================================

# https://stackoverflow.com/questions/76717279/ttkbootstrap-meter-widget-doc-example-not-working
from PIL import Image
Image.CUBIC = Image.BICUBIC  # this is for the meter widget in ttkbootstrap. Check the stackoverflow link above

import ttkbootstrap as ttb
import numpy as np
# from ttkbootstrap.constants import *
# from ttkbootstrap.scrolled import ScrolledFrame

# =============================================================================

import numpy as np


# =============================================================================
# Import backend
# =============================================================================
from ph_bleach_backend_v2_1 import *
# =============================================================================


def quit_program():
    print('Thank you for using the program. Longer strands!')
    
    print(output_frame.winfo_width())
    print(output_frame.winfo_height())
    

    
    root.destroy()


def fill_output_frame():
    
    lbl_img.grid(row=0,column =0,  sticky = 'nwse', padx= 5, pady= 10)




def show_plot():
    # global lbl_img
    global img_list
    
    # ===============================================================================================
    # Get spinbox value and set index accordingly
    # ===============================================================================================
    # 'Norm. Rate', 'Rate', 'Masking', 'Sample Frame'
    ind = 0
    if spn_img.get() == 'Norm. Rate':
        ind = 0
    if spn_img.get() == 'Rate':
        ind = 1
    if spn_img.get() == 'Masking':
        ind = 2
    if spn_img.get() == 'Sample Frame':
        ind = 3
      
    
    
    # ===============================================================================================
    # !!!! The image list must be recalculated as the images can change everytime we run the program
    # ===============================================================================================
    img_list = []
    for m_fname in ifname_list:
        img_list.append(ttb.PhotoImage(file = m_fname))
    # ===============================================================================================
        
    
    img = Image.open(ifname_list[ind])   # we need this PIL function to get size of the image later
    lbl_img.grid_forget()   # erase existing image
    
    # output_frame.update()   # ! can't use this. update() causes the spinbox to loop inifinitely
    
    # calculate scale factor (amount by which the image should be scaled down) from outout_frame size and image size
    scl = round((img.size[0]/output_frame.winfo_width()) + 0.5)   # the 0.5 ensures that it'll always round up. Using native round() instead of numpy/math ceil(). We can avoid importing those libraries then.
    scl = max(scl, round((img.size[1]/output_frame.winfo_height()) + 0.5))
              
    print('Current uutput frame width = %i' % output_frame.winfo_width())
    print('Scale factor for image resize = %i' % scl)


         
    img_list[ind] = img_list[ind].subsample(scl,scl)   # maybe think about preserving the original image. Saving the scaled image in a new temp variable doesn't work for some reason
    lbl_img.config(image = img_list[ind])
        
    
    # call funciton to fill all the contents in the output window
    fill_output_frame()
    
    
    
    # lbl_img.grid(row=1,column =0,  sticky = 'nsew', padx= 5, pady= 10)
    # lbl_img.config(text = 'in show plot')
    # lbl_img.config(image = demo_media2)

# debug function. Will be deleted/commented out later
def print_values():
    # x2 = np.round(spn_blur_order.get(),2)
    # x2 = int(spn_blur_order.get())
    print('printing')
    print(export_data.get())
    blur_order = spn_blur_order.get()
    dpi = spn_dpi.get()
  
    # lb_temp = ttb.Label(output_frame, text = ent_block_size.get())
    
    lb_temp = ttb.Label(output_frame, text = 'Threshold type = ' + spn_th_type.get())
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'dt = ' + ent_dt.get())
    lb_temp.pack()
    
    
    lb_temp = ttb.Label(output_frame, text = 'Blur order = ' + str(blur_order))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Block size = ' + ent_block_size.get())
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Export data = ' + str(export_data.get()))
    lb_temp.pack()

    lb_temp = ttb.Label(output_frame, text = 'Obj detect in each frame = ' + str(obj_det.get()))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Smooth data = ' + str(sm_data.get()))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Simple threshold = ' + str(mtr_th.amountusedvar.get()))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Adaptive threshold = ' + str(mtr_adth.amountusedvar.get()))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Object size (radial) threshold = ' + str(mtr_obth.amountusedvar.get()))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Fig. dip = ' + str(dpi))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Savgol window = ' + ent_sv_window.get())
    lb_temp.pack()

    lb_temp = ttb.Label(output_frame, text = 'Savgol order = ' + ent_sv_order.get())
    lb_temp.pack()



# depending on the threshold type, enable/disable some features
def limit_input():
    temp = spn_th_type.get()
    if temp == 'simple':
        mtr_adth.configure(interactive = False,bootstyle= 'secondary')
        mtr_th.configure(interactive = True, bootstyle = 'danger')
        ent_block_size.configure(state = 'disabled')   
        lbl_block_size.configure(bootstyle = 'secondary')
    
    if temp == 'adaptive16bit':
        mtr_th.configure(interactive = False, bootstyle= 'secondary')
        mtr_adth.configure(interactive = True, bootstyle = 'danger')
        ent_block_size.configure(state = 'enabled')        
        lbl_block_size.configure(bootstyle = 'primary')
        
        
        
    if sm_data.get() == False:
        ent_sv_order.configure(state = 'disabled')
        ent_sv_window.configure(state = 'disabled')
        lbl_sv_order.configure(bootstyle = 'secondary')
        lbl_sv_window.configure(bootstyle = 'secondary')
    else:
        ent_sv_order.configure(state = 'enabled')
        ent_sv_window.configure(state = 'enabled')
        lbl_sv_order.configure(bootstyle = 'primary')
        lbl_sv_window.configure(bootstyle = 'primary')

# run backend with parameter values from the widget
def run_backend():
    
    # Dec. 20, 2023: all variables except the path have been connected to the widgets. 
    # Will start with the filedaialog box to for this. Later, will try to move on to drag and drop
    
    path_dir = '/home/asif/Photobleach_data/'   # directory where the data files are
    fname = 'M_15s.tif'
    path = path_dir + fname
    dt = float(ent_dt.get())  #dt = 15/60                  # time interval between images (unit: minutes)
    
    # =============================================================================
    # Control parameter
    # =============================================================================
    exprt_data = export_data.get()           #exprt_data = True                  # Export data to csv file True/False
    obj_detect_each_frame = obj_det.get()    # if True, then object is detected in every frame. 
                                      # if False, then object is detected in the first frame only
                                      # and is assumed to be stationary if every other frame. Setting False
                                      # might be useful for noisy and low-light image.
                                      
    th_factor = float(mtr_th.amountusedvar.get())/100                     # th_factor = 0.6                   # For simple thresholding: Fraction of maximum brightness. Pixels having this brightness fraction is assumed to be part of the object
    mean_th_fct = float(mtr_adth.amountusedvar.get())/100                 # mean_th_fct = 0.1                 # For 16 bit adaptive thresholding: percentage more than the block_mean required to be considered an object
    
    blur_order = int(spn_blur_order.get())       # blur_order = 5                    # Order of the median blur
    block_size = int(ent_block_size.get())       # block_size = 41                   # block size for adaptive thresholding
        
    obj_size_th_factor = float(mtr_obth.amountusedvar.get()/100)**2                  # obj_size_th_factor = 0.1**2       # for composite mask from fragments, size (area) of object to include = max_size * obj_size_th_factor. The square is to convert length to area 
    th_type = spn_th_type.get()              # th_type = 'adaptive16bit'         # thresholding function
    smooth_data = sm_data.get()              # smooth_data = False                 # Smooth data y/n
    savgol_window = int(ent_sv_window.get()) # savgol_window = 11                # parameters for the smoothing filter
    savgol_order = int(ent_sv_order.get())   # savgol_order = 3                  # parameters for the smoothing filter
    
    test_img_ind = 0                  # test image frame to plot
    dpi_fig = int(spn_dpi.get())      # dpi_fig  = 600                    # dpi of saved figures
    # =============================================================================
    
    
    # # https://note.nkmk.me/en/python-os-basename-dirname-split-splitext/
    # dirname = os.path.dirname(path) + '/'
    # print(dirname)
    
    main_run(path, dt, exprt_data, obj_detect_each_frame, th_factor, mean_th_fct, blur_order, block_size, obj_size_th_factor, th_type,
              smooth_data, savgol_window, savgol_order, test_img_ind, dpi_fig)



    
    
# =============================================================================
# Main program
# =============================================================================


# =============================================================================
#control variables
# =============================================================================
window_width = 800
window_height = 600    
posx = window_width/2
posy = window_height/2

ctrl_width_fraction = 3/8 
top_frame_height = 50
bottom_frame_height = 50

# =============================================================================



# =============================================================================
# root window
# =============================================================================


root = ttb.Window(themename="sandstone")

root.title('Photobleaching Analysis from TIF image stack')
root.geometry(("%dx%d+%d+%d" % (window_width, window_height, posx, posy)))

root.update()  # get window dimensiosn
root.minsize(root.winfo_width(), root.winfo_height())   # set minimum size of the program window
# =============================================================================


# =============================================================================
# Set style
# =============================================================================
# my_style = ttb.Style()
# my_style.configure('success.TButton', font = ('Arial',  12))

# =============================================================================


# =============================================================================
# define frames
# =============================================================================
ctrl_frame = ttb.Labelframe(root)
output_frame = ttb.Labelframe(root)
top_frame = ttb.Frame(root)
bottom_frame = ttb.Frame(root)

# ctrl_frame = ScrolledFrame(root, autohide = False)
# output_frame = ScrolledFrame(root, autohide = False)

ctrl_frame.place(x=0,y=0,relheight=1, width = window_width*ctrl_width_fraction)
top_frame.place(x=window_width*ctrl_width_fraction, y=0, height = top_frame_height, relwidth = 1 )
output_frame.place(x=window_width*ctrl_width_fraction,y=top_frame_height, relheight=1, relwidth = 1 )
# bottom_frame.place(x=window_width*ctrl_width_fraction, height = bottom_frame_height, relwidth = 1 )
bottom_frame.pack(side= 'bottom',anchor = 'e')

# =============================================================================





# =============================================================================
# Define variables
# =============================================================================
export_data = ttb.BooleanVar(value = True)
obj_det = ttb.BooleanVar(value = False)
sm_data = ttb.BooleanVar(value = False)
# =============================================================================




# Label+Entry pair
lbl_block_size= ttb.Label(ctrl_frame,text = 'Block size', bootstyle = 'primary')
ent_block_size = ttb.Entry(ctrl_frame, bootstyle = 'primary')

# ent2.delete(0,ttb.END)
ent_block_size.insert(0,41)


# Label+Entry pair
lbl_dt= ttb.Label(ctrl_frame,text = 'Time step (min)', bootstyle = 'primary')
ent_dt = ttb.Entry(ctrl_frame, bootstyle = 'primary')

# ent2.delete(0,ttb.END)
ent_dt.insert(0,0.25)

# 
# lbl_block_size.pack(side='left', pady = 20)
# ent_block_size.pack(side='left', padx = 10)

# lbl_block_size.pack(anchor ='nw',padx = 20)
# ent_block_size.pack(anchor='w', padx = 90)



# Label+Entry pair
lbl_blur_order= ttb.Label(ctrl_frame,text = 'Blur order', bootstyle = 'primary')
spn_blur_order = ttb.Spinbox(ctrl_frame, bootstyle = 'primary', from_=3, to = 5, increment=2, width = 17, wrap = True)
spn_blur_order.insert(0,5)
spn_blur_order.configure(state = 'readonly')

lbl_th_type = ttb.Label(ctrl_frame,text = 'Threshold type', bootstyle = 'primary')
spn_th_type  = ttb.Spinbox(ctrl_frame, bootstyle= 'primary',
                           values = ['simple', 'adaptive16bit'], state= 'readonly',
                           wrap = True,
                           command = limit_input,
                           )
spn_th_type.set('adaptive16bit')

# Label + checkboxes
# lbl_export_data= ttb.Label(ctrl_frame,text = 'Export Data', bootstyle = 'primary')
chk_export_data = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary-round-toggle', text = 'Export data', variable = export_data)



chk_obj_detect_each_frame = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary-round-toggle', text = 'OD in each frame', variable = obj_det)
chk_sm_data = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary-round-toggle', text = 'Smooth data', variable = sm_data, command = limit_input)


mtr_th = ttb.Meter(ctrl_frame, bootstyle = 'secondary', 
                    subtext = 'Simp. Th',
                    interactive = False,
                    stripethickness=10,
                    meterthickness=8,
                    metersize = 120,
                    amounttotal = 100,
                    amountused = 80,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',)

mtr_adth = ttb.Meter(ctrl_frame, bootstyle = 'danger', 
                    subtext = 'Adpt.Th',
                    interactive = True,
                    stripethickness=10,
                    meterthickness=8,
                    metersize = 120,
                    amounttotal = 100,
                    amountused = 20,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',)

mtr_obth = ttb.Meter(ctrl_frame, bootstyle = 'warning', 
                    subtext = 'Obj. size Th',
                    interactive = True,
                    stripethickness=10,
                    meterthickness=8,
                    metersize = 120,
                    amounttotal = 50,
                    amountused = 10,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',)

lbl_dpi = ttb.Label(ctrl_frame,  text = 'Fig dpi', bootstyle = 'primary')
spn_dpi = ttb.Spinbox(ctrl_frame, bootstyle = 'primary', from_=150, to = 600, increment=150, width = 17)
spn_dpi.insert(0,150)
spn_dpi.configure(state = 'readonly')


lbl_sv_window= ttb.Label(ctrl_frame,text = 'Savgol Window', bootstyle = 'secondary')
ent_sv_window = ttb.Entry(ctrl_frame, bootstyle = 'primary')
ent_sv_window.insert(0,11)
ent_sv_window.configure(state ='disabled')

lbl_sv_order= ttb.Label(ctrl_frame,text = 'Savgol Order', bootstyle = 'secondary')
ent_sv_order = ttb.Entry(ctrl_frame, bootstyle = 'primary')
ent_sv_order.insert(0,3)
ent_sv_order.configure(state ='disabled')




bt_run = ttb.Button(ctrl_frame, text = 'Run', bootstyle = 'success', command = run_backend, )

bt1 = ttb.Button(output_frame, text = 'Print', bootstyle = 'info', command = print_values)



bt_quit = ttb.Button(top_frame, text = 'Quit', bootstyle = 'danger', command = quit_program)


bt_display = ttb.Button(bottom_frame, text = 'Display/Fit Plots', bootstyle = 'warning', command = show_plot)
spn_img  = ttb.Spinbox(bottom_frame, bootstyle= 'primary',
                           values = ['Norm. Rate', 'Rate', 'Masking', 'Sample Frame'], 
                           wrap = True,
                           command = show_plot,
                           )

spn_img.insert(0,'Norm Rate')
spn_img.configure(state = 'readonly')

# =============================================================================
# Handle images
# =============================================================================
# these paths will be obtained from file Browse input later
path_dir = '/home/asif/Photobleach_data/'   # directory where the data files are
fname = 'M_15s.tif'
path = path_dir + fname

# =============================================================================
# the file names of the image files saved by the backend code. We will display these images in the output window of the front end

ifname_list = [path[0:-3] + 'normalized_rate.png', path[0:-3] + 'rate.png', path[0:-3] + 'after_masking.png',   path[0:-3] + 'test_frame.png']

# =============================================================================

img_place_holder = ttb.PhotoImage(file = 'place_holder.png')
# img_list = [ttb.PhotoImage(file = ifname1), ttb.PhotoImage(file = ifname2), ttb.PhotoImage(file = ifname3), ttb.PhotoImage(file = ifname4)]

# demo_media = demo_media.subsample(2,2)
lbl_img = ttb.Label(output_frame,  image = img_place_holder)






# =============================================================================
# packing
# =============================================================================


# lbl_block_size.grid(row = 1, column = 1, padx = 10, pady = 10)
# ent_block_size.grid(row = 1, column = 2, padx = 10, pady = 10)


# lbl_blur_order.grid(row = 2, column = 1, padx = 10, pady = 10)
# spn_blur_order.grid(row = 2, column = 2, padx = 10, pady = 10)

# chk_export_data.grid(row = 3, column = 1, padx = 10, pady = 10)
# chk_obj_detect_each_frame.grid(row = 3, column = 2, padx = 10, pady = 10)
# chk_smooth_data.grid(row = 4, column = 1, padx = 10, pady = 10)

# ttb.Separator(ctrl_frame, bootstyle='info').pack(pady = 10, fill = 'x')
# lbl_block_size.pack(anchor='w',padx = 20)
# ent_block_size.pack(anchor='w', padx = 20,pady = 1)
# ttb.Separator(ctrl_frame, bootstyle='info').pack(pady = 5,anchor = 'e')


# lbl_dt.pack(anchor='w',padx = 20)
# ent_dt.pack(anchor='w', padx = 20,pady = 1)
# ttb.Separator(ctrl_frame, bootstyle='info').pack(pady = 5,anchor = 'e')



# lbl_blur_order.pack(anchor='w', padx = 20)
# spn_blur_order.pack(anchor='w', padx = 20,pady = 1)
# ttb.Separator(ctrl_frame, bootstyle='info').pack(pady = 5,anchor = 'e')


# lbl_th_type.pack(anchor='w', padx = 20)
# spn_th_type.pack(anchor='w', padx = 20,pady = 1)
# ttb.Separator(ctrl_frame, bootstyle='info').pack(pady = 5,anchor = 'e')


# ttb.Separator(ctrl_frame, bootstyle='primary').pack(pady = 10, fill = 'x')
                    
# chk_export_data.pack(padx = 20,anchor = 'w')
# chk_obj_detect_each_frame.pack(padx = 20,anchor = 'w')
# chk_sm_data.pack(padx = 20,anchor = 'w')


# ttb.Separator(ctrl_frame, bootstyle='primary').pack(pady = 10, fill = 'x')

# mtr_th.pack(pady = 30, anchor='w', padx = 10)
# ttb.Separator(ctrl_frame, bootstyle='info').pack(pady = 5,anchor = 'e')
# mtr_adth.pack(anchor='w', padx = 10)
# ttb.Separator(ctrl_frame, bootstyle='info').pack(pady = 5,anchor = 'e')
# mtr_obth.pack(anchor='w', padx = 10)


# lbl_sv_window.pack(anchor='w',padx = 20)
# ent_sv_window.pack(anchor='w', padx = 20,pady = 1)
# lbl_sv_order.pack(anchor='w',padx = 20)
# ent_sv_order.pack(anchor='w', padx = 20,pady = 1)


# lbl_dpi.pack(anchor='w', padx = 20)
# spn_dpi.pack(anchor='w', padx = 20,pady = 1)


# bt2.pack(padx = 10, pady = 20)
# bt1.pack(padx = 10, pady = 20)
# bt3.pack(anchor = 's', padx = 10, pady = 20)



# =============================================================================
# Grid layout
# =============================================================================

# =============================================================================
# Ctrl_frame fill
# =============================================================================
ctrl_frame.columnconfigure(0, weight = 1)
ctrl_frame.columnconfigure(1, weight = 1)
ctrl_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight = 1)
ctrl_frame.rowconfigure(17, weight = 1000)   # this will stay an empty row. The large height will pack the other rows tight..



count = 1

lbl_th_type.grid(row=count, column = 0, sticky = 'nw', padx = 10)
lbl_dt.grid(row=count, column = 1, sticky = 'nw', padx = 10)
count = count + 1

spn_th_type.grid(row=count, column = 0, sticky = 'nw', padx = 10)
ent_dt.grid(row=count, column = 1, sticky = 'nw', padx = 10)
count = count + 1

lbl_blur_order.grid(row=count, column = 0, sticky = 'nw', padx = 10)
lbl_block_size.grid(row=count, column = 1, sticky = 'nw', padx = 10)
count = count + 1

spn_blur_order.grid(row=count, column = 0, sticky = 'nw', padx = 10)
ent_block_size.grid(row=count, column = 1, sticky = 'nw', padx = 10)
count = count + 1


chk_obj_detect_each_frame.grid(row = count, column = 0, padx = 10, pady = 10)
chk_export_data.grid(row = count, column = 1, padx = 10, pady = 10)
count = count + 1

ttb.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=2, pady = 10, sticky = 'nsew')
count = count + 1

# middle block with meters
mtr_th.grid(row = count, column = 0, padx = 10, pady = 10)
mtr_adth.grid(row = count, column = 1, padx = 10, pady = 10)
count = count + 1

mtr_obth.grid(row = count, column = 0, padx = 10, pady = 10)
count = count + 1

ttb.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=2, pady = 10, sticky = 'nsew')
count = count + 1




# smooth data block
chk_sm_data.grid(row=count, column = 0, sticky = 'nw', padx = 10)
count = count + 1

lbl_sv_window.grid(row=count, column = 0, sticky = 'nw', padx = 10)
lbl_sv_order.grid(row=count, column = 1, sticky = 'nw', padx = 10)
count = count + 1

ent_sv_window.grid(row=count, column = 0, sticky = 'nw', padx = 10)
ent_sv_order.grid(row=count, column = 1, sticky = 'nw', padx = 10)
count = count + 1

ttb.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=2, pady = 10, sticky = 'nsew')
count = count + 1

# last block

lbl_dpi.grid(row = count, column = 0, sticky = 'nw', padx = 10)
bt_run.grid(row = count, column  = 1, rowspan = 3, sticky = 'nsew',padx = 10)

count = count + 1


spn_dpi.grid(row = count, column = 0, sticky = 'nw', padx = 10)
count = count + 1

ttb.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, pady = 10, sticky = 'nsew')

# =============================================================================



# =============================================================================
# Output frame fill
# =============================================================================

# output_frame.columnconfigure((0,1,2), weight = 1)
# output_frame.rowconfigure((0,1), weight = 1)
# output_frame.rowconfigure(2, weight = 2)
# output_frame.rowconfigure(3, weight = 1)


# lbl_img.grid(row=1,column =0,  sticky = 'nsew', padx= 5, pady= 10)
# fill_output_frame()

# bt_quit.grid(row = 2, column =1, sticky = 'nw', pady= 10)



# =============================================================================
# Bottom frame fill
# =============================================================================
bt_display.pack(side = 'left', pady= 10, padx = 10)
spn_img.pack(side = 'left', pady= 10, padx = 10)

# =============================================================================

# =============================================================================
# Top frame fill
bt_quit.pack(side = 'left', pady= 10, padx = 40)
# =============================================================================



root.protocol("WM_DELETE_WINDOW", lambda: (root.quit(), root.destroy()))


root.mainloop()



# x1 = np.round(spn_blur_order.get(),2)