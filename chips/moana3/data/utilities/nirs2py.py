# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 14:44:22 2023

@purpose:   Generates captures.npz file from .nirs file.

@usage:     Standalone or in target script.

@prereqs:   n/a

@author:    Kevin Renehan and Jinwon Kim
"""


import numpy as np
import os
from scipy.io import loadmat, savemat
from interpret_test_setup import interpret_test_setup
from interpret_yield import interpret_yield
from interpret_dynamic_packet import interpret_dynamic_packet
from process_triggers import process_triggers


def nirs2py():
    
    # SD indexing (the ones that I know)
    WAVELENGTH = 0
    SRC_POSITION = 1
    DET_POSITION = 2
    DUMMY_POSITION = 3
    NUM_SRC = 13
    NUM_DET = 14
    MEAS_LIST = 18
    SPRINGS = 20
    ANCHORS = 21
    MEAS_UNIT = 23
    
    # File to generate
    npz_file_name = 'data.npz'
    
    # This directory
    this_dir = os.path.basename(os.getcwd())
    
    # This function
    this_func = "py2nirs"
    
    # Print header
    header = "    " + this_func + " in " + this_dir + ": "
    
    # Filelist
    filelist = os.listdir()
    
    # Starting
    print(header + "Starting")
    
    # Check if file has already been generated
    if npz_file_name in filelist:
        print(header + npz_file_name + " already generated")
        return 1
    
    # Look for previously generated accumulated file
    found = False
        
    # Look for captures file
    for f in filelist:
        if '.nirs' in f:
            nirs_filepath = f
            found = True
            
    # Make sure the file was found
    if not found:
        print(header + "ERROR - .nirs file not found")
        return -1
    
    # Attempt to load SD structure from mat file
    mdict = loadmat(nirs_filepath, appendmat=False)
    
    # Vectors
    time = np.squeeze(np.transpose(mdict['t'], axes=(1,0)))
    data = np.transpose(mdict['d'], axes=(1,0))
    stim = np.transpose(mdict['s'], axes=(1,0))
    
    # Get map of flattened indices
    measurement_list = np.transpose(mdict['SD'][0]['MeasList'][0], axes=(1,0)) - 1
    
    # Get some info from the SD file
    number_of_sources = mdict['SD'][0]['nSrcs'][0][0][0]
    max_source = int(max(measurement_list[0]))
    number_of_detectors = mdict['SD'][0]['nDets'][0][0][0]
    max_detector = int(max(measurement_list[1]))
    number_of_wavelengths = len(mdict['SD'][0]['Lambda'][0][0])
    number_of_frames = len(time)
    
    # Create data array
    final = np.zeros(( max_source, number_of_wavelengths, max_detector, number_of_frames), dtype=float)
    final.fill(np.nan)

    # Fill final array
    print(header + "Filling output array")
    for s in range(max_source):
        for d in range(max_detector):
            
            # Check to see if this is actually a source/detector pair
            if len(np.nonzero((measurement_list[0] == s) & (measurement_list[1] == d))[0]) < 1:
                continue
            
            # Find each wavelength
            for w in range(number_of_wavelengths):
                
                # Get index in measurement list
                idx = np.nonzero((measurement_list[0] == s) & (measurement_list[1] == d) & (measurement_list[3] == w))[0]
                
                # Check that an index was found
                if len(idx) < 1:
                    continue
                
                # Fill
                final[s][w][d] = data[idx]
                    

        
    # Save accumulated results
    print(header + "Saving " + npz_file_name + " file")
    np.savez_compressed( npz_file_name, data=data, time=time, stim=stim)
    
    # Done
    print(header + "Done")
    return 0
    

# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    
    # Select a data directory
    target_dir = easygui.diropenbox(title="Choose directory containing captures file")
    
    # Check
    if target_dir == None:
        raise Exception("Target directory not provided")
    
    # Move to data directory
    os.chdir(target_dir)
    
    # Run function
    nirs2py()
    
    
            
            