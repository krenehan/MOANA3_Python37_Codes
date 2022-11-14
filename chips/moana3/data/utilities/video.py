# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User

Run zip.py before accumulating
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

capture_number = 0

def make_frame(t):
    
    # Each 
    
    # Clear
    ax.clear()
    
    capture_number = capture_number + 1

def video():

    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for zipped captures file")
    found = False
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if 'captures.npz' in filelist[f]:
            print("Found zipped captures file")
            found = True
            
    if not found:
        
        raise Exception("Zipped captures file not found")
        
    else:
        
        # Load capture file
        arr = np.load('captures.npz')['data']
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
        # Capture number variable
        capture_number = 0
        
        plot_axes = [None]*number_of_chips
        plot_figure, axes_structure = plt.subplots(4, 4, sharex=True, sharey=False)
        # plot_figure.suptitle("Accumulated Data")
        plot_figure.set_size_inches(24, 20)
        
        
        