# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@purpose:   Averages captures in captures.npz to create averaged.npz. 

@usage:     Standalone or in target script.

@prereqs:   zip_files()

@author:    Kevin Renehan
"""

import numpy as np
import os

def average():
    
    # This directory
    this_dir = os.path.basename(os.getcwd())
    
    # This function
    this_func = "average"
    
    # Print header
    header = "    " + this_func + " in " + this_dir + ": "
    
    # File name
    filename = 'averaged.npz'

    # Directory info
    filelist = os.listdir()
    
    # Check to see if averaged file has been generated
    if filename in filelist:
        print(header + filename + " already generated")
        return 1
    
    # Look for captures.npz
    found = False
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if 'captures.npz' in filelist[f]:
            found = True
            
    if not found:
        
        print(header + "Zipped captures file not found")
        return -1
        
    else:
        
        # Load
        arr = np.load('captures.npz')['data']
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
        # Accumulate
        acc = np.mean(arr, axis=0)
            
        # Save accumulated results
        print(header + "Saving averaged file")
        np.savez_compressed(filename, data=acc)
        
    # Done
    print(header + "Finished")
    return 0






# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    
    # Select a data directory
    target_dir = easygui.diropenbox(title="Choose directory containing captures.npz")
    
    # Check
    if target_dir == None:
        raise Exception("Target directory not provided")
    
    # Move to data directory
    os.chdir(target_dir)
    
    # Run function
    average()