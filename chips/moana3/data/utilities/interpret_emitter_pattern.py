# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Kevin Renehan

Interpret a test setup file.
"""

import os
import numpy as np


def interpret_emitter_pattern():

    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for emitter pattern file")
    found = False
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if 'test_setup.txt' in filelist[f]:
            print("Found test setup file")
            found = True
    
    # Test setup file must be present
    if not found:
        
        raise Exception("Emitter pattern file not found")
        
    else:
        
        # Load
        print("Opening emitter pattern file")
        ep = np.load("emitter_pattern.npy")
        
        # Interpret
        print("Interpreting emitter pattern file")
        number_of_patterns, number_of_chips = np.shape(ep)

        # Create array
        arr = np.empty((number_of_patterns,), dtype=int)
        
        # Fill array
        for p in range(number_of_patterns):
            found = False
            for c in range(number_of_chips):
                if ep[p][c]:
                    arr[p] = c
                    found = True
                    break
            if not found:
                arr[p] = -1
        
        # Return
        print("Done")
        return arr
            
