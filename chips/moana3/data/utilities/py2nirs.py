# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 14:44:22 2023

Function to generate .nirs file from raw data captures.

@author: bmc06
"""

import numpy as np
import os
from scipy.io import loadmat, savemat

from interpret_test_setup import interpret_test_setup
from interpret_yield import interpret_yield
from interpret_dynamic_packet import interpret_dynamic_packet



def py2nirs(sd_filepath, capture_window = None):
    
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
    
    # Check that SD file was provided
    if sd_filepath is None:
        print("SD file not provided to py2nirs function")
        print("NIRS file not generated")
        return -1
    
    # Attempt to load SD structure from mat file
    mdict = loadmat(sd_filepath, appendmat=False)
    
    # Look for SD
    if 'SD' in mdict:
        sd = mdict['SD']
    else:
        print("SD structure not found in SD file at " + str(sd_filepath))
        print("NIRS file not generated")
        # return -1
        
    # Get map of flattened indices
    flat_index_map = np.transpose(sd[0][0][MEAS_LIST], axes=(1,0))
    
    # Check for capture window
    if capture_window == None:
        capture_window_specified = False
    else:
        capture_window_specified = True

    # Directory info - we should be in the data directory
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for zipped captures file, emitter pattern file, test setup, and yield file")
    found = True
        
    # Look for captures file
    if 'captures.npz' not in filelist:
        print("Could not find zipped captures file")
        found = False
    else:
        print("Found zipped captures file")

        
    # Look for emitter pattern file
    if 'dynamic_packet.txt' not in filelist:
        print("Could not find dynamic packet file")
        found = False
    else:
        print("Found dynamic packet file")
        
    # Look for test setup file
    if 'test_setup.txt' not in filelist:
        print("Could not find test setup file")
        found = False
    else:
        print("Found test setup file")
        
    # Look for yield file
    if 'yield.txt' not in filelist:
        print("Could not find yield file")
        found = False
    else:
        print("Found yield file")
    
    # Check that we found all the files
    if not found:
        
        raise Exception("One or more files not found")
        
    # Load captures
    print("Loading captures file")
    capture_data = np.load('captures.npz')['data']
    
    # Load emitter pattern file
    print("Loading dynamic file")
    ep = interpret_dynamic_packet()
    
    # Interpret test setup
    print("Loading test setup file")
    ts = interpret_test_setup()
    
    # Used detectors
    print("Loading yield file")
    working_nir_sources, working_ir_sources, working_detectors =  interpret_yield()
    
    # Get shape of captures
    number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(capture_data)
    
    # Get relevant parameters from test setup file
    clk_freq = float(ts['Clock Frequency'])
    period = float(ts['Period'])
    meas_per_patt = float(ts['Measurements per Pattern'])
    patt_per_fram = float(ts['Patterns per Frame'])
    
    # Create time parameters
    t_step = meas_per_patt * period*1e-9 * patt_per_fram
    fps = 1 / t_step
    elapsed_t = np.arange(0, number_of_captures * number_of_frames * t_step, t_step)
    t_ps = np.arange(0, number_of_bins*65, 65)
    
    # Transpose to bin:capture:frame:source:detector, zero out bin 0, tranpose back
    capture_data = np.transpose(capture_data, axes=(4, 0, 1, 2, 3))
    capture_data[0].fill(0)
    capture_data = np.transpose(capture_data, axes=(1,2,3,4,0))
        
    # Transpose to capture:frame:source:detector:bin
    capture_data = np.transpose(capture_data, axes=(0, 2, 1, 3, 4))
    capture_data = np.reshape(capture_data, newshape=(number_of_captures * number_of_frames, number_of_chips, patterns_per_frame, number_of_bins))
    
    # Modify number of captures and frames
    number_of_captures = number_of_captures * number_of_frames
    number_of_frames = 1
    
    # Transpose to source:detector:capture:bin
    capture_data = np.transpose(capture_data, axes=(2, 1, 0, 3))
    
    # Set number of wavelengths
    number_of_wavelengths = 2
    
    # Tranposed emitter pattern (wavelength, chip, pattern)
    ep_T = np.transpose(ep, axes=(2,1,0))
    
    # Create final array [source][wavelength][detector][capture][bin]
    final = np.zeros((number_of_chips, number_of_wavelengths, number_of_chips, number_of_captures, number_of_bins), dtype=float)
    
    # Fill final array
    print("Filling output array")
    for s in range(number_of_chips):
        
        # Defaults
        do_nir = False
        do_ir = False
        
        # Find the NIR pattern and IR pattern index for this source location
        nir_idx = np.where(ep_T[0][s] == True)[0]
        ir_idx = np.where(ep_T[1][s] == True)[0]
        
        # Mask based on whether or not a value was found
        if len(nir_idx) > 0:
            do_nir = True
            nir_idx = nir_idx[0]
            # print("Source {} is NIR emitter for pattern {}".format(s, nir_idx))
        else:
            print("Source {} was not used as an NIR emitter".format(s))
            
        # Mask based on whether or not a value was found
        if len(ir_idx) > 0:
            do_ir = True
            ir_idx = ir_idx[0]
            # print("Source {} is IR emitter for pattern {}".format(s, ir_idx))
        else:
            print("Source {} was not used as an IR emitter".format(s))
        
        # Check to see if the source is functional
        if s not in working_nir_sources:
            do_nir = False
            print("Skipping NIR data for source " + str(s) + " because it is non-functional")
           
        # Check to see if the source is functional
        if s not in working_ir_sources:
            do_ir = False
            print("Skipping IR data for source " + str(s) + " because it is non-functional")
        
        # Fill
        for d in range(number_of_chips):
            if d in working_detectors:
                if do_nir:
                    final[s][0][d] = capture_data[nir_idx][d]
                if do_ir:
                    final[s][1][d] = capture_data[ir_idx][d]
            else:
                print("Skipping detector " + str(d) + " because it is non-functional")
        print("Filled index for source {} of final array with NIR data from pattern {} and IR data from pattern {}".format(s, nir_idx, ir_idx))
    
    # Integrate bins, reshape to flatten, transpose
    final = np.sum(final, axis=4)
    
    # Remap into flattened array, tranpose to shape source*detector*wavelength, timepoints
    flattened_arr = np.zeros((number_of_chips * number_of_chips * number_of_wavelengths, number_of_captures), dtype=final.dtype)
    
    # Fill flattened array
    for s in range(number_of_chips):
        for w in range(number_of_wavelengths):
            for d in range(number_of_chips):
                
                # Get the index
                idx = (flat_index_map[0]-1 == s) & (flat_index_map[1]-1 == d) & (flat_index_map[3]-1 == w)
                if len(idx.nonzero()) > 1:
                    raise Exception("More than one entry for source {}, detector {}, wavelength {} in measurement channel list")
                else:
                    idx = idx.nonzero()[0][0]
                    
                # Fill
                # print("Filled index {} of flattened array with data from source {}, detector {}, wavelength {}".format(idx, s, d, w))
                flattened_arr[idx] = final[s][w][d]
                
    # Transpose to shape number_of_captures x sources*detectors*wavelengths
    flattened_arr = np.transpose(flattened_arr, axes=(1,0))
    
    # Create empty s_array (number of triggers assumed to be 3)
    s_arr = np.zeros((number_of_captures, 3))
    
    # Aux data
    aux = np.array([], dtype=float)
    
    # Check that all arrays are float arrays (due to bug in Homer3 HDF5 Save function)
    for idx in range(len(sd[0][0])):
        
        # Check if the index is numeric
        if np.issubdtype(sd[0][0][idx].dtype, np.number):
        
            # Check dimensions and convert to float
            if np.squeeze(sd[0][0][idx]).ndim > 0:
                sd[0][0][idx] = sd[0][0][idx].astype(float)
    
    # Create dictionary for save
    ddict = {}
    ddict['d'] = flattened_arr
    ddict['s'] = s_arr
    ddict['SD'] = sd
    ddict['t'] = elapsed_t
    ddict['aux'] = aux
        
    # Save accumulated results
    print("Saving data.nirs file")
    savemat('data_r1.nirs', ddict, appendmat=False, oned_as='column')
    

# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    
    # No capture window
    capture_window = None
    
    # Select a data directory
    target_dir = easygui.diropenbox(title="Choose directory containing captures file")
    
    # Check
    if target_dir == None:
        raise Exception("Target directory not provided")
    
    # Move to data directory
    os.chdir(target_dir)
    
    # Select an SD file
    sd_filepath = easygui.fileopenbox(title="Choose an SD file for .nirs file generation")
    
    # Check
    if sd_filepath == None:
        raise Exception("SD file not provided")
    
    # Run function
    py2nirs(sd_filepath, capture_window = capture_window)
    
    
            
            