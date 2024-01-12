#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 18:18:52 2023

@author: Mohammad Asif Zaman


Style note:
    - The labels corresponding to a disabled entry box/meter have bootstyle of secondary. Everytime something
      is enabled/disabled, the corresponding label style is configured accordingly. This style
      should be kept constant in all future modifications.

Things to implement:
    - Drag and drop box for file input
    - Work on the backend to work with adaptive8bit
    - Work on the backend to work with avi files

Version b_0.2:
    - Removed some unnecessary library imports in the front end
    - Quit function: try to make it more accurate
    - Deleted the print_values() function. Also deleted other unused code blocks.
    - Added number validation check to more entry boxes.
    

"""

# =============================================================================
# Import ttkbootstrap 
# =============================================================================

# https://stackoverflow.com/questions/76717279/ttkbootstrap-meter-widget-doc-example-not-working
from PIL import Image
Image.CUBIC = Image.BICUBIC  # this is for the meter widget in ttkbootstrap. Check the stackoverflow link above

import ttkbootstrap as ttb

from ttkbootstrap.dialogs import Messagebox
from tkinter.filedialog import askopenfile 


from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinterdnd2.TkinterDnD import _require


# from ttkbootstrap.scrolled import ScrolledFrame



# =============================================================================


# =============================================================================
# Import backend
# =============================================================================
from ph_bleach_backend_v2_1 import *
# =============================================================================



# =============================================================================    
# Quit program function with confirmation message box
# =============================================================================    
def quit_program():
    # Quit program function with confirmation message box
    
    # create messagebox
    mb_quit = Messagebox.yesno('Do you want to quit PhotoBleach?', 'Quit',parent = output_frame)
    
    if mb_quit == 'Yes':
        
        print('Output frame width = %i' % output_frame.winfo_width())
        print('Output frame height = %i' % output_frame.winfo_height())
        print('Path = %s' %  path) 
        print('\nThank you for using the program. Longer strands!\n')
        root.quit()     # Added this in vb0.2. Sometimes, the terminal gets stuck when quitting the program. This might help.
        root.destroy()
    else:
        pass
# =============================================================================    

# =============================================================================    
# populate the output frame
# =============================================================================    
def fill_output_frame():
    # populate the output frame
    lbl_img.grid(row=1,column =0,  sticky = 'nw', padx= 5, pady= 10)
# =============================================================================    




# =============================================================================    
# Function for when the browse button is clicked. Assigns path, enables run button, populates ifname_list
# =============================================================================    
def open_file():
    # Function for when the browse button is clicked. It assigns the global path variable and populates the global ifname_list list. 
    # Enables run button. Edits the file path label for the output_frame. 
    
    file = askopenfile(mode='r', filetypes=[('TIF', '*.tif')])    # Open file explorer to select file
    
    if file:
        global path
        global ifname_list
        global lbl_path
        
        path = file.name
        
        lbl_path.config(text = 'File = ' + path)   # Label of the file name which will be displayed in the output window.
        
        
        print('Selected file path = %s' %path)
        
        # the file names of the image files saved by the backend code. We will display these images in the output window of the front end
        # note that the file name structure is determined by the backend. 
        ifname_list = [path[0:-3] + 'normalized_rate.png', path[0:-3] + 'rate.png', path[0:-3] + 'after_masking.png',   path[0:-3] + 'test_frame.png']
        
        bt_run.config(state = 'enabled')  # Enables the run button
# =============================================================================    


# =============================================================================    
# Drag and drop function
# =============================================================================    
def drag_drp(e):
    global path   # global variable that contains the path of file 1
    global ifname_list
    global lbl_path
    
    st = str(e.data)   # get drag n drop event data and assign it to a string        
    
    # replace curly brackets (if any). These braces seem to show up on when the file path has space character.
    st = st.replace('{','')
    st = st.replace('}','')
    
    path = st  # feed the cleaned string data in path1 global variable
        
    ent_dnd.delete(0,'end')      # remove old text from the DND box
    ent_dnd.insert(ttb.END, st)  # insert new text in the DND box
   
    
    lbl_path.config(text = 'File = ' + path)   # Label of the file name which will be displayed in the output window.
    
    print('Selected file path = %s' %path)
    
    # the file names of the image files saved by the backend code. We will display these images in the output window of the front end
    # note that the file name structure is determined by the backend. 
    ifname_list = [path[0:-3] + 'normalized_rate.png', path[0:-3] + 'rate.png', path[0:-3] + 'after_masking.png',   path[0:-3] + 'test_frame.png']
    
    bt_run.config(state = 'enabled')  # Enables the run button

# =============================================================================    




# =============================================================================    
# Display info when the info button is pressed
# =============================================================================    
def show_info():
    # Display info when the info button is pressed
    # Displays content of the readme.txt file in a messagebox. The txt file needs more work.
    freadme = open('readme.txt').read()  
    Messagebox.show_info(freadme, 'Information', parent = ctrl_frame) 
# =============================================================================    



# =============================================================================    
# load output images, set the selected output image, and call the fill_output_frame()        
# =============================================================================    
def show_plot():
    # load output images, set the selected output image, and call the fill_output_frame()
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
    for m_fname in ifname_list:                    #ifname_list is a global variable defineed in the open_file() function
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


    # Down sample the image to fit within output_frame() frame     
    img_list[ind] = img_list[ind].subsample(scl,scl)   # maybe think about preserving the original image. Saving the scaled image in a new temp variable doesn't work for some reason
    
    lbl_img.config(image = img_list[ind])   # change the label so that it is associated with the current subsampled image
        
    
    # call funciton to fill all the contents in the output window
    fill_output_frame()
# =============================================================================    
    

# =============================================================================    
#  # Checks the dt, Block size, savgol window and order entry boxes to make sure that the inputs are numbers (int, float)
# =============================================================================  
def validate_number():
    # Checks the dt, Block size, savgol window and order entry boxes to make sure that the inputs are numbers (int, float)
    flag = 0  # zero means no error
    
    try:
        int(ent_sv_window.get())
    except ValueError:
        Messagebox.show_error('Failed to run. SAVGOL window must be an integer', 'Input error', parent = output_frame)
        flag = 1    # set flag = 1 to indicate error
    
    try:
        int(ent_sv_order.get())
    except ValueError:
        Messagebox.show_error('Failed to run. SAVGOL order must be an integer', 'Input error', parent = output_frame)
        flag = 1    # set flag = 1 to indicate error
        
    try:
        int(ent_block_size.get())
    except ValueError:
        Messagebox.show_error('Failed to run. Block size must be an integer', 'Input error', parent = output_frame)
        flag = 1    # set flag = 1 to indicate error
            
    try:
        float(ent_dt.get())
    except ValueError:
        Messagebox.show_error('Failed to run. Time step must be a number', 'Input error', parent = output_frame)
        flag = 1    # set flag = 1 to indicate error
  
        
  
    return flag    
# =============================================================================        

    
# =============================================================================        
# depending on the threshold type, enable/disable some features
# =============================================================================
def limit_input():
    # depending on the threshold type, enable/disable some features
    temp = spn_th_type.get()   # get the threshold type input from spinbox
    
    # if statements for threshold type
    if temp == 'simple':
        mtr_adth.configure(interactive = False,bootstyle= 'secondary')  # disable adaptive threshold meter input
        mtr_th.configure(interactive = True, bootstyle = 'danger')      # turn ON simple threshold meter
        ent_block_size.configure(state = 'disabled')                    # disable block size entry box. This is only valid for adaptive thresholding
        lbl_block_size.configure(bootstyle = 'secondary')               # change color of the block_size label to indicate the corresponding entry box has been disabled
    
    if temp == 'adaptive16bit':
        mtr_th.configure(interactive = False, bootstyle= 'secondary')
        mtr_adth.configure(interactive = True, bootstyle = 'danger')
        ent_block_size.configure(state = 'enabled')        
        lbl_block_size.configure(bootstyle = 'primary')
        
        
    # if statement for smooth data check box    
    if sm_data.get() == False:      
        # if smooth data is not selected, disable the savgol window and order entry boxes
        # note that along with the entry box disabled, the corresponding labels' colors change to secondary to 
        # further highlight the disabled status
        ent_sv_order.configure(state = 'disabled')
        ent_sv_window.configure(state = 'disabled')
        lbl_sv_order.configure(bootstyle = 'secondary')
        lbl_sv_window.configure(bootstyle = 'secondary')
    else:
        # if smooth data is selected, enable the corresponding input buttons
        ent_sv_order.configure(state = 'enabled')
        ent_sv_window.configure(state = 'enabled')
        lbl_sv_order.configure(bootstyle = 'primary')
        lbl_sv_window.configure(bootstyle = 'primary')
# =============================================================================






# =============================================================================
# run backend with parameter values from the widget. Calls show_plot() function
# =============================================================================
def run_backend():
    # run backend with parameter values from the widget. Calls show_plot() function     
    # Dec. 20, 2023: all variables except the path have been connected to the widgets. 
    # Will start with the filedaialog box to for this. Later, will try to move on to drag and drop
    
    # Populate path from the global variable
    # path_dir = '/home/asif/Photobleach_data/'   # directory where the data files are
    # fname = 'M_15s.tif'
    # path = path_dir + fname
    
    
    # Don't run if path is empty. Note that the run button is disabled by default and only enables when open_file() is called and a file is selected.
    # So, the following check is superfluous.
    if path == '':
        Messagebox.show_error('No TIF source file selected', 'File error', parent = output_frame)
        return 0 
    
    
    # Do validatio check. If error found, then skip (don't run)
    if validate_number() == 1:
        return 0
    

    
    # =============================================================================
    # Control parameter
    # =============================================================================

    dt = float(ent_dt.get())  #dt = 15/60                  # time interval between images (unit: minutes)
        
    exprt_data = export_data.get()           #exprt_data = True                  # Export data to csv file True/False
    obj_detect_each_frame = obj_det.get()    # if True, then object is detected in every frame. 
                                      # if False, then object is detected in the first frame only
                                      # and is assumed to be stationary if every other frame. Setting False
                                      # might be useful for noisy and low-light image.
                                      
    th_factor = float(mtr_th.amountusedvar.get())/100                     # th_factor = 0.6                   # For simple thresholding: Fraction of maximum brightness. Pixels having this brightness fraction is assumed to be part of the object
    mean_th_fct = float(mtr_adth.amountusedvar.get())/100                 # mean_th_fct = 0.1                 # For 16 bit adaptive thresholding: percentage more than the block_mean required to be considered an object
    
    blur_order = int(spn_blur_order.get())       # blur_order = 5                    # Order of the median blur
    block_size = int(ent_block_size.get())       # block_size = 41                   # block size for adaptive thresholding
    
    # ! Note that the radial object size is converted to area. The backend works with area.    
    obj_size_th_factor = float(mtr_obth.amountusedvar.get()/100)**2               # obj_size_th_factor = 0.1**2       # for composite mask from fragments, size (area) of object to include = max_size * obj_size_th_factor. The square is to convert length to area 
    th_type = spn_th_type.get()              # th_type = 'adaptive16bit'         # thresholding function
    smooth_data = sm_data.get()              # smooth_data = False                 # Smooth data y/n
    savgol_window = int(ent_sv_window.get()) # savgol_window = 11                # parameters for the smoothing filter
    savgol_order = int(ent_sv_order.get())   # savgol_order = 3                  # parameters for the smoothing filter
    
    # this one doesn't have a corresponding input button. Does not appear to be necessary at this moment. It's mostly useful for debugging the backend.
    test_img_ind = 0                  # test image frame to plot
    dpi_fig = int(spn_dpi.get())      # dpi_fig  = 600                    # dpi of saved figures
    # =============================================================================
    
    
    # # https://note.nkmk.me/en/python-os-basename-dirname-split-splitext/
    # dirname = os.path.dirname(path) + '/'
    # print(dirname)
    
    main_run(path, dt, exprt_data, obj_detect_each_frame, th_factor, mean_th_fct, blur_order, block_size, obj_size_th_factor, th_type,
              smooth_data, savgol_window, savgol_order, test_img_ind, dpi_fig)

    
    # =============================================================================
    # Configure frontend options after backend finishes running
    # =============================================================================
    # Enable display button and image select spin box
    bt_display.configure(state = 'enabled')
    spn_img.configure(state = 'readonly')
    # call function to display output plots
    show_plot()
# =============================================================================



    
    
# =============================================================================
# Main program
# =============================================================================


# =============================================================================
#control variables
# =============================================================================
window_width = 1220
window_height = 940    
posx = window_width/8   # x position of the window
posy = window_height/20  # y position of the window

ctrl_width_fraction = 3/8   # what fraction of the total window is the ctrl_frame
top_frame_height = 100
bottom_frame_height = 50

# =============================================================================



# =============================================================================
# root window
# =============================================================================


root = ttb.Window(themename="sandstone")    # set root windows and theme
# root = ttb.Window(themename="superhero")
_require(root)  # for drag and drop support

root.title('PhotoBleach: Analysis from TIF image stack')    # Set title of the root frame
root.geometry(("%dx%d+%d+%d" % (window_width, window_height, posx, posy)))

# Icon not working in linux builds. Work on this later
# my_icon = ttb.PhotoImage('icon.ico')
# root.iconphoto(my_icon)  


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
# total 4 frames. 
ctrl_frame = ttb.Labelframe(root)
output_frame = ttb.Labelframe(root)
top_frame = ttb.Frame(root)
bottom_frame = ttb.Frame(root)

# place/pack the 4 frames
ctrl_frame.place(x=0,y=0,relheight=1, width = window_width*ctrl_width_fraction)
top_frame.place(x=window_width*ctrl_width_fraction, y=0, height = top_frame_height, relwidth = 1 )
output_frame.place(x=window_width*ctrl_width_fraction,y=top_frame_height, relheight=1, relwidth = 1 )
bottom_frame.pack(side= 'bottom',anchor = 'e')

# =============================================================================


# =============================================================================
# Super global variable
# =============================================================================
path = ''    # Start with an empty string. This will be filled when browse button is clicked. Populated in open_file() function.
# =============================================================================


# =============================================================================
# Define variables for the checkboxes
# =============================================================================
export_data = ttb.BooleanVar(value = True)   # set default to be be true
obj_det = ttb.BooleanVar(value = False)      # set default to be false
sm_data = ttb.BooleanVar(value = False)      # set default to be false
# =============================================================================

# =============================================================================
# Defining top frame entries: logo and version info
# =============================================================================
# Label with version number
lbl_version = ttb.Label(top_frame, text = 'Mohammad Asif Zaman \nVersion b_0.3 \nJan. 2024', bootstyle = 'secondary', font = ('Arial',6))

img_logoM = ttb.PhotoImage(file = 'logoM_80px.png')
lbl_logoM = ttb.Label(top_frame,  image = img_logoM)

bt_quit = ttb.Button(top_frame, text = 'Quit', bootstyle = 'danger', command = quit_program)
# =============================================================================


# =============================================================================
# Defining entries of the control frame
# =============================================================================

# Label+Spinbox pair: Threshold type
lbl_th_type = ttb.Label(ctrl_frame,text = 'Threshold type', bootstyle = 'primary')
spn_th_type  = ttb.Spinbox(ctrl_frame, bootstyle= 'primary',
                           values = ['simple', 'adaptive16bit'], state= 'readonly',
                           wrap = True,
                           command = limit_input,
                           )
spn_th_type.set('adaptive16bit')
# Label+Entry pair: Time step
lbl_dt= ttb.Label(ctrl_frame,text = 'Time step (min)', bootstyle = 'primary')
ent_dt = ttb.Entry(ctrl_frame, bootstyle = 'primary')

ent_dt.insert(0,0.25) # default value set



# Label+Spinbox pair: Blur order
lbl_blur_order= ttb.Label(ctrl_frame,text = 'Blur order', bootstyle = 'primary')
spn_blur_order = ttb.Spinbox(ctrl_frame, bootstyle = 'primary', from_=3, to = 5, increment=2, width = 17, wrap = True)
spn_blur_order.insert(0,5)   # set default value
spn_blur_order.configure(state = 'readonly')  # set as readonly

# Label+Entry pair: Block size
lbl_block_size= ttb.Label(ctrl_frame,text = 'Block size', bootstyle = 'primary')
ent_block_size = ttb.Entry(ctrl_frame, bootstyle = 'primary')

ent_block_size.insert(0,41) # default value set



# Checkboxes
chk_obj_detect_each_frame = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary-round-toggle', text = 'OD in each frame', variable = obj_det)
chk_export_data = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary-round-toggle', text = 'Export data', variable = export_data)
chk_sm_data = ttb.Checkbutton(ctrl_frame, bootstyle = 'primary-round-toggle', text = 'Smooth data', variable = sm_data, command = limit_input)


# Meters
mtr_th = ttb.Meter(ctrl_frame, bootstyle = 'secondary', 
                    subtext = 'Simp. Th',
                    interactive = False,
                    stripethickness=8,
                    meterthickness=6,
                    metersize = 110,
                    amounttotal = 100,
                    amountused = 80,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',)

mtr_adth = ttb.Meter(ctrl_frame, bootstyle = 'danger', 
                    subtext = 'Adpt.Th',
                    interactive = True,
                    stripethickness=8,
                    meterthickness=6,
                    metersize = 110,
                    amounttotal = 100,
                    amountused = 20,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',)

mtr_obth = ttb.Meter(ctrl_frame, bootstyle = 'warning', 
                    subtext = 'Obj. size Th',
                    interactive = True,
                    stripethickness=8,
                    meterthickness=6,
                    metersize = 110,
                    amounttotal = 50,
                    amountused = 10,
                    textright = '%',
                    stepsize=1,
                    textfont='-size 10 -weight bold',)





# Label+Entry pair: Savgol window
lbl_sv_window= ttb.Label(ctrl_frame,text = 'Savgol Window', bootstyle = 'secondary')
ent_sv_window = ttb.Entry(ctrl_frame, bootstyle = 'primary')
ent_sv_window.insert(0,11)
ent_sv_window.configure(state ='disabled')

# Label+Entry pair: Savgol order
lbl_sv_order= ttb.Label(ctrl_frame,text = 'Savgol Order', bootstyle = 'secondary')
ent_sv_order = ttb.Entry(ctrl_frame, bootstyle = 'primary')
ent_sv_order.insert(0,3)
ent_sv_order.configure(state ='disabled')

# Label+Spinbox pair: Fig dpi
lbl_dpi = ttb.Label(ctrl_frame,  text = 'Fig dpi', bootstyle = 'primary')
spn_dpi = ttb.Spinbox(ctrl_frame, bootstyle = 'primary', from_=150, to = 600, increment=150, width = 17)
spn_dpi.insert(0,150)
spn_dpi.configure(state = 'readonly')


# Command buttons in the ctrl frame: run, browse, info. Only the browse button has a separate label
bt_run = ttb.Button(ctrl_frame, text = 'Run', bootstyle = 'success', command = run_backend, state= 'disabled')
bt_info = ttb.Button(top_frame, text = 'Info/Help', bootstyle = 'warning', command = show_info)
bt_browse = ttb.Button(ctrl_frame, text = 'Browse', bootstyle = 'primary', command = open_file)
lbl_browse = ttb.Label(ctrl_frame, text = 'Open file', bootstyle = 'primary')


ent_dnd = ttb.Entry(ctrl_frame, bootstyle = 'primary')
ent_dnd.drop_target_register(DND_FILES)
ent_dnd.dnd_bind('<<Drop>>', drag_drp)
lbl_dnd = ttb.Label(ctrl_frame, text = 'Drag and drop here', bootstyle = 'primary')



# =============================================================================





# =============================================================================
# Defining entries of the bottom frame
# =============================================================================

bt_display = ttb.Button(bottom_frame, text = 'Display/Fit Plots', bootstyle = 'warning', command = show_plot, state = 'disabled')
bt_browse_bottom = ttb.Button(bottom_frame, text = 'Browse', bootstyle = 'primary', command = open_file)

spn_img  = ttb.Spinbox(bottom_frame, bootstyle= 'primary',
                           values = ['Norm. Rate', 'Rate', 'Masking', 'Sample Frame'], 
                           wrap = True,
                           command = show_plot,
                           )

spn_img.insert(0,'Norm Rate')
spn_img.configure(state = 'disabled')

# =============================================================================



# =============================================================================
# Defining entries of the output frame
# =============================================================================

img_place_holder = ttb.PhotoImage(file = 'place_holder.png')
lbl_path = ttb.Label(output_frame, text = '', bootstyle = 'secondary')     # this label will be populated by the path once file is selected
lbl_img = ttb.Label(output_frame,  image = img_place_holder)






# =============================================================================
# Layout (mostly grid)
# =============================================================================

# =============================================================================
# Ctrl_frame fill
# =============================================================================
ctrl_frame.columnconfigure(0, weight = 1)
ctrl_frame.columnconfigure(1, weight = 1)
ctrl_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 17, 18,19,20,21,22,23,24), weight = 1)
ctrl_frame.rowconfigure(25, weight = 1000)   # this will stay an empty row. The large height will pack the other rows tight..


# the count variable makes it easy to reposition widgets in the frame without having to change grid indices of all following entries

count = 0
lbl_browse.grid(row = count, column = 0, stick = 'nw', padx = 10)
lbl_dnd.grid(row = count, column = 1, stick = 'nw', padx = 10)

count = count + 1
ent_dnd.grid(row = count, column = 0, columnspan = 2,  stick = 'nse', padx = 10, ipady = 20, ipadx = 20)
bt_browse.grid(row = count, column = 0, stick = 'nw', padx = 10, ipady = 20, ipadx = 20)
count = count + 1
count = count + 1
ttb.Separator(ctrl_frame, bootstyle='secondary').grid(row=count, column = 0, columnspan=2, pady = 10, sticky = 'nsew')
count = count + 1
               
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
# bt_info.grid(row = count, column = 1, padx = 10, pady = 10)
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


print('Ctrl frame total rows = %i' % count)

# =============================================================================



# =============================================================================
# Output frame fill
# =============================================================================

output_frame.rowconfigure(0, weight = 1)
output_frame.rowconfigure(1, weight = 100)
lbl_path.grid(row = 0, column = 0, stick = 'nw', padx = 10)

# The output frame image is set in the fill_output_frame() function which is called from the show_plot(). The run_backend() calls show_plot().


# =============================================================================
# Bottom frame fill
# =============================================================================
bt_browse_bottom.pack(side = 'left', pady= 10, padx = 10)
bt_display.pack(side = 'left', pady= 10, padx = 10)
spn_img.pack(side = 'left', pady= 10, padx = 10)

# =============================================================================

# =============================================================================
# Top frame fill
lbl_logoM.pack(side = 'left', pady= 2, padx = 10)
lbl_version.pack(side = 'left', pady= 0, padx = 0)
bt_info.pack(side = 'left', pady = 0, padx = 10, ipady = 10)
bt_quit.pack(side = 'left',  pady= 0, padx = 10, ipady = 10, ipadx = 30)
# =============================================================================



root.protocol("WM_DELETE_WINDOW", lambda: (root.quit(), root.destroy()))


root.mainloop()



# x1 = np.round(spn_blur_order.get(),2)