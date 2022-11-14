# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User

Run zip.py before accumulating
"""

import numpy as np
import os
import matplotlib.pyplot as plt

def average():

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
        
        # Load
        print("Loading captures file")
        arr = np.load('captures.npz')['data']
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
        # Accumulate
        print("Averaging captures")
        acc = np.mean(arr, axis=0)
            
        # Save accumulated results
        print("Saving averaged file")
        np.savez_compressed('averaged.npz', data=acc)
        
        print("Done")