#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 18:18:52 2023

@author: Mohammad Asif Zaman
"""

# =============================================================================
# Import ttkbootstrap 
# =============================================================================
import ttkbootstrap as ttb
import numpy as np
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

# =============================================================================

import numpy as np

# =============================================================================
# Import backend
# =============================================================================
from ph_bleach_backend_v1 import *
# =============================================================================


def print_values():
    # x2 = np.round(spn_blur_order.get(),2)
    # x2 = int(spn_blur_order.get())
    print('printing')
    print(export_data.get())
    blur_order = spn_blur_order.get()
  
    # lb_temp = ttb.Label(output_frame, text = ent_block_size.get())
    lb_temp = ttb.Label(output_frame, text = 'Blur order = ' + str(blur_order))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Block size = ' + ent_block_size.get())
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Export data = ' + str(export_data.get()))
    lb_temp.pack()

    lb_temp = ttb.Label(output_frame, text = 'Obj detect in each frame = ' + str(obj_detect_each_frame.get()))
    lb_temp.pack()
    
    lb_temp = ttb.Label(output_frame, text = 'Smooth data = ' + str(smooth_data.get()))
    lb_temp.pack()


#control variables
window_width = 800
window_height = 600    
posx = window_width/2
posy = window_height/2

entry_width = 12   # width of entry boxes
entry_height = 20
pdy = 5 # default pady value

# str(window_width) + 'X' + str(window_height)

# root window
root = ttb.Window(themename="sandstone")
root.title('Photobleaching Analysis from TIF image stack')
root.geometry(("%dx%d+%d+%d" % (window_width, window_height, posx, posy)))


# define frames
# ctrl_frame = ttb.Labelframe(root,text='Control')
# output_frame = ttb.Labelframe(root, text = 'Output')

ctrl_frame = ScrolledFrame(root, autohide = False)
output_frame = ScrolledFrame(root, autohide = False)


ctrl_frame.place(x=0,y=0,relheight=1, width = 500)
output_frame.place(x=340,y=0,relheight=1,relwidth=.6 )


# =============================================================================
# Define variables
# =============================================================================
export_data = ttb.BooleanVar(value = True)
blur_order = ttb.IntVar()
block_size = ttb.IntVar()
obj_detect_each_frame = ttb.BooleanVar(value = False)
smooth_data = ttb.BooleanVar(value = False)
# =============================================================================


# Label+Entry pair
lbl_block_size= ttb.Label(ctrl_frame,text = 'Block size', bootstyle = 'primary')
ent_block_size = ttb.Entry(ctrl_frame, bootstyle = 'primary')

# ent2.delete(0,ttb.END)
ent_block_size.insert(0,41)

# lbl_block_size.pack(side='left', pady = 20)
# ent_block_size.pack(side='left', padx = 10)

lbl_block_size.grid(row = 1, column = 1, padx = 10, pady = 10)
ent_block_size.grid(row = 1, column = 2, padx = 10, pady = 10)


# Label+Entry pair
lbl_blur_order= ttb.Label(ctrl_frame,text = 'Blur order', bootstyle = 'primary')
spn_blur_order = ttb.Spinbox(ctrl_frame, bootstyle = 'primary', from_=3, to = 13, increment=2, width = 17)
spn_blur_order.insert(0,5)
spn_blur_order.configure(state = 'readonly')
# ent2.delete(0,ttb.END)
# ent_blur_order.insert(0,5)

lbl_blur_order.grid(row = 2, column = 1, padx = 10, pady = 10)
spn_blur_order.grid(row = 2, column = 2, padx = 10, pady = 10)



# Label + checkboxes
lbl_export_data= ttb.Label(ctrl_frame,text = 'Export Data', bootstyle = 'primary')
chk_export_data = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary', text = 'Export data', variable = export_data)
chk_export_data.grid(row = 3, column = 1, padx = 10, pady = 10)

chk_obj_detect_each_frame = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary', text = 'Obj det in each frame', variable = obj_detect_each_frame)
# lbl_export_data.grid(row = 3, column = 1, padx = 10, pady = 10)
chk_obj_detect_each_frame.grid(row = 3, column = 2, padx = 10, pady = 10)

chk_smooth_data = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary', text = 'Smooth data', variable = smooth_data)
# lbl_export_data.grid(row = 3, column = 1, padx = 10, pady = 10)
chk_smooth_data.grid(row = 4, column = 1, padx = 10, pady = 10)



bt1 = ttb.Button(output_frame, text = 'Print', bootstyle = 'danger', command = print_values)
bt1.pack(padx = 10, pady = 20)







root.protocol("WM_DELETE_WINDOW", lambda: (root.quit(), root.destroy()))


root.mainloop()

# x1 = np.round(spn_blur_order.get(),2)