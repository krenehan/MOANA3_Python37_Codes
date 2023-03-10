# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@purpose:   Zips capture_N.npy files into single captures.npz file.  

@usage:     Standalone or in target script.

@prereqs:   None.

@author:    Kevin Renehan

"""

import numpy as np
import os

def zip_files():
    
    # This directory
    this_dir = os.path.basename(os.getcwd())
    
    # This function
    this_func = "zip_files"
    
    # Print header
    header = "    " + this_func + " in " + this_dir + ": "
    
    # Starting
    print(header + "Starting")
    
    # Filename to generate
    filename = "captures.npz"
    
    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if filename in filelist[f]:
            print(header + "Found previously created npz file")
            return 1
    
    # Determine the number of captures
    number_of_captures = 0
    for f in os.listdir():
        if "capture" in f:
        # if ".npy" in f:
            number_of_captures = number_of_captures + 1
            
    # Load the first capture and determine dimensions
    number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(np.load("capture_0.npy"))
    # number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(np.load("1.npy"))

    # Create array
    arr = np.empty( (number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins), dtype=int)   
    
    # Accumulate
    for capture in range(number_of_captures):
        if not (capture % 10):
            print(header + "Finished loading " + str(capture) + " captures")
        arr[capture] = np.load("capture_" + str(capture) + ".npy")
        # arr[capture] = np.load(str(capture) + ".npy")
    
    # Zero out the first bin
    for capture in range(number_of_captures):
        for chip in range(number_of_chips):
            for frame in range(number_of_frames):
                for pattern in range(patterns_per_frame):
                    arr[capture][chip][frame][pattern][0] = 0.0
        
    # Zip accumulated results
    print(header + "Saving zipped captures")
    np.savez_compressed(filename, data=arr)
    
    # Done
    print(header + "Finished")
    return 0
    
    
    
# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    
    # Capture window
    capture_window = None
    
    # Breath hold window
    breath_hold_window = None
    
    # Select a data directory
    target_dir = easygui.diropenbox(title="Choose directory containing multiple capture_N.npy files")
    
    # Check
    if target_dir == None:
        raise Exception("Target directory not provided")
    
    # Move to data directory
    os.chdir(target_dir)
    
    # Run function
    zip_files()
    
    