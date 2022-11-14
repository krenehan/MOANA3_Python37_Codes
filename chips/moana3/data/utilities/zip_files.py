# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User
"""

import numpy as np
import os

def zip_files():
    
    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for previously created npz file")
    found = False
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if 'captures.npz' in filelist[f]:
            print("Found previously created npz file")
            found = True
            
    if found:
        
        # Load
        print("Zipping already performed")
        
    else:
        
        print("Zipping files")
        
        # Determine the number of captures
        number_of_captures = 0
        for f in os.listdir():
            #if "capture" in f:
            if ".npy" in f:
                number_of_captures = number_of_captures + 1
                
        # Load the first capture and determine dimensions
        #number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(np.load("capture_1.npy"))
        number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(np.load("1.npy"))
    
        # Create array
        arr = np.empty( (number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins), dtype=int)   
        
        # Accumulate
        for capture in range(number_of_captures):
            if not (capture % 100):
                print("Finished loading " + str(capture) + " captures")
            #arr[capture] = np.load("capture_" + str(capture) + ".npy")
            arr[capture] = np.load(str(capture) + ".npy")
        
        # Zero out the first bin
        print("Zeroing out garbage collection bins")
        for capture in range(number_of_captures):
            if not (capture % 100):
                print("Finished zeroing " + str(capture) + " captures")
            for chip in range(number_of_chips):
                for frame in range(number_of_frames):
                    for pattern in range(patterns_per_frame):
                        arr[capture][chip][frame][pattern][0] = 0.0
            
        # Zip accumulated results
        print("Saving zipped")
        np.savez_compressed('captures.npz', data=arr)