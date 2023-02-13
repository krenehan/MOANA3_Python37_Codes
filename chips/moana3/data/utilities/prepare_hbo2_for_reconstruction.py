# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Kevin Renehan

"""

import numpy as np
import os
from scipy.io import savemat
from pathlib import Path
from interpret_test_setup import interpret_test_setup
from interpret_dynamic_packet import interpret_dynamic_packet
from interpret_yield import interpret_yield


def prepare_hbo2_for_reconstruction(capture_window = None):

    # Subdirectory name
    subdirectory_name = "reconstruction_outputs\\"
    subdirectory_path = os.path.join(os.getcwd(), subdirectory_name)
    
    # Check for capture window
    if capture_window == None:
        capture_window_specified = False
    else:
        capture_window_specified = True
    
    # Occlusion window
    breath_hold_window = np.array((600, 900), dtype=int)
    if capture_window_specified:
        breath_hold_window = breath_hold_window - capture_window[0]

    # Directory info
    l = os.listdir()
    filelist = []
    for f in l:
        if os.path.isfile(f):
            filelist.append(f)
            
    
    # Look for previously generated accumulated file
    print("Searching for zipped captures file, dynamic packet file, test setup, and yield file")
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
            
    if not found:
        
        raise Exception("One or more files not found")
        
    else:
        
        # Load
        print("Loading captures file")
        arr = np.load('captures.npz')['data']
        
        # Load emitter pattern file (pattern, chip, wavelength) wavelength 0 is 680nm, wavelength 1 is 850nm
        print("Loading dynamic packet file")
        ep = interpret_dynamic_packet()
        
        # Interpret test setup
        print("Loading test setup file")
        ts = interpret_test_setup()
        
        # Used detectors
        print("Loading yield file")
        working_nir_sources, working_ir_sources, working_detectors =  interpret_yield()
        
        # Create results directory
        Path( subdirectory_path ).mkdir( parents=True, exist_ok=True )
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
        # Set number of wavelengths
        number_of_wavelengths = 2
        
        # Combine the capture and frame axes
        arr = np.transpose(arr, axes=(0, 2, 1, 3, 4))
        arr = np.reshape(arr, newshape=(number_of_captures*number_of_frames, 1, number_of_chips, patterns_per_frame, number_of_bins))
        arr = np.transpose(arr, axes=(0, 2, 1, 3, 4))
        
        # Modify number of captures and frames
        number_of_captures = number_of_captures * number_of_frames
        number_of_frames = 1
        
        # If we have a custom capture window, we redefine the number of captures to be included
        if capture_window_specified:
            if capture_window[0] >= capture_window[1]:
                raise Exception("Second index of capture window greater than or equal to first index")
            if capture_window[0] < 0:
                raise Exception("First index of capture window is less than 0")
            if capture_window[0] > len(arr):
                raise Exception("First index of capture window is greater than the number of captures")
            if capture_window[1] < 0:
                raise Exception("Second index of capture window is less than 0")
            if capture_window[1] > len(arr):
                raise Exception("Second index of capture window is greater than the number of captures")
            arr = arr[capture_window[0]:capture_window[1]]
            number_of_captures = capture_window[1] - capture_window[0]
        
        # Fill capture_window if not specified
        else:
            capture_window = (0, number_of_captures)
            
        # Reshape array [pattern][chip][capture][bin]
        arr = np.transpose(np.squeeze(arr), axes=(2,1,0,3))
            
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
                        final[s][0][d] = arr[nir_idx][d]
                    if do_ir:
                        final[s][1][d] = arr[ir_idx][d]
                else:
                    print("Skipping detector " + str(d) + " because it is non-functional")
            print("Filled index for chip {} of final array with NIR data from pattern {} and IR data from pattern {}".format(s, nir_idx, ir_idx))

        # Create time axis
        hist_t = np.linspace(0, 149, num=150, dtype=int) * 65
        
        # Calculate CW data
        cw_data = np.sum(final, axis=(4,))
        
        # Calculate integration time
        it = float(ts['Period']) * 1e-9 * float(ts['Measurements per Pattern'])
        
        # Calculate frame rate
        fps = 1/(float(ts['Period']) * 1e-9 * float(ts['Measurements per Pattern']) * patterns_per_frame)
        
        # Time axis for experiment
        t_step = 1 / fps
        exp_t = np.arange(capture_window[0], capture_window[1] * t_step, t_step)




    ##### MATLAB #####
    working_detectors_matlab = [i+1 for i in working_detectors]
    working_nir_sources_matlab = [i+1 for i in working_nir_sources]
    working_ir_sources_matlab = [i+1 for i in working_ir_sources]

    # Create dictionary for save
    ddict = {}
    ddict['conditions'] = ts['Conditions']
    ddict['hist_t'] = hist_t
    ddict['hist_data'] = final
    ddict['exp_t'] = exp_t
    ddict['cw_data'] = cw_data
    ddict['integration_time'] = it
    ddict['capture_rate'] = fps
    ddict['number_of_captures'] = number_of_captures
    ddict['capture_window'] = (capture_window[0]+1, capture_window[1]+1)
    ddict['breath_hold_window'] = (breath_hold_window[0] + 1, breath_hold_window[1] + 1)
    ddict['number_of_detector_locations'] = number_of_chips
    ddict['number_of_source_locations'] = patterns_per_frame
    ddict['nir_source_wavelength'] = '680nm'
    ddict['ir_source_wavelength'] = '850nm'
    ddict['nir_source_array_index'] = 1
    ddict['ir_source_array_index'] = 2
    ddict['functional_detectors'] = working_detectors_matlab
    ddict['functional_nir_sources'] = working_nir_sources_matlab
    ddict['functional_ir_sources'] = working_ir_sources_matlab
    ddict['number_of_bins'] = number_of_bins
    ddict['patch_location'] = ts['Patch Location']
    ddict['test_type'] = ts['Test Type']
    
    # Filename
    filestring = os.path.join(subdirectory_path, 'reconstruction_data')
        
    # Save accumulated results
    print("Saving averaged .mat file")
    savemat(filestring + '.mat', ddict)
    
    # Create readme string
    st = \
'''################################################### Keys ###################################################
conditions                        - Identifier for the experiment.
hist_t                            - Time axis for histograms (ps). Shape is (number_of_bins).
exp_t                             - Time axis for entire experiment (s). Shape is (number_of_captures).
hist_data                         - Histogram data (raw counts). Shape is (number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures, number_of_bins).
cw_data                           - Integrated histogram data (CW). Shape is (number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures).
integration_time                  - Integration time (s) per source for the histogram data in the experiment.
capture_rate                      - Captures per second. One capture is defined as all source/detector pairs at both wavelengths.
number_of_captures                - Number of captures taken over the course of the experiment.
capture_window                    - Selected captures from original data set.
breath_hold_window                  - Captures during which strap was tightened to simulate venous occlusion. 
number_of_detector_locations      - Number of detectors on the 4x4 array.
number_of_source_locations        - Total number of source locations on the 4x4 array (2 wavelengths present at each location).
nir_source_wavelength             - Wavelength of the NIR sources.
ir_source_wavelength              - Wavelength of the IR sources.
nir_source_array_index            - Index of NIR data in hist_data and cw_data arrays. 
ir_source_array_index             - Index of IR data in hist_data and cw_data arrays. 
functional_detectors              - The detector locations on the 4x4 array that are functional and were used in the experiment.
functional_nir_sources            - The NIR source locations on the 4x4 array that are functional and were used in the experiment. 
functional_ir_sources             - The IR source locations on the 4x4 array that are functional and were used in the experiment. 
number_of_bins                    - The number of bins in a histogram.
patch_location                    - Physical location of the 4x4 array during the experiment.
test_type                         - Type of experiment that was performed.

############################################ Source/Detector Mapping ############################################
  ___________________
|    |    |    |    |
|  1 |  2 |  3 |  4 |
|____|____|____|____|
|    |    |    |    |
|  5 |  6 |  7 |  8 |
|____|____|____|____|
|    |    |    |    |
|  9 | 10 | 11 | 12 |
|____|____|____|____|
|    |    |    |    |
| 13 | 14 | 15 | 16 |
|____|____|____|____|

############################################ Examples ############################################
In Matlab, to plot the NIR histogram between Source Location 1 and Detector Location 9 for Capture 20:
--> source_location = 1
--> wavelength_index = 1
--> detector_location = 9
--> capture = 20
--> plot(hist_t, hist_data(source_location, wavelength_index, detector_location, capture))

In Matlab, to plot the IR CW time trace between Source 1 and Detector 9 over the entire experiment:
--> source_location = 1
--> wavelength_index = 2
--> detector_location = 9
--> plot(exp_t, cw_data(source_location, wavelength_index, detector_location))

The plots should have nonzero values if source is found in functional_sources. 
If a NIR/IR source is not found in functional_nir_sources/functional_ir_sources, this means that the NIR/IR source was not working or not used in the experiment, and the histogram data will be all 0s.
    '''
    
    # Save a readme file
    print("Saving MATLAB readme file")
    f = open(os.path.join(subdirectory_path, "reconstruction_data_mat_README.txt"), "w")
    f.write(st)
    f.close()
    
    # # Plot to verify
    # import matplotlib.pyplot as plt
    # for s in range(len(used_chips)):
    #     fig, ax = plt.subplots(nrows=3, ncols=3)
    #     ax = ax.flat
    #     fig.suptitle("Source " + str(s+1))
    #     for d in range(len(ax)):
    #         ax[d].plot(t, acc_shuffled[s][d])
    
    print("Saving .npz file")
    np.savez_compressed ( \
                        filestring, \
                        conditions = ts['Conditions'], \
                        hist_t = hist_t, \
                        hist_data = final, \
                        exp_t = exp_t, \
                        cw_data = cw_data, \
                        integration_time = it, \
                        capture_rate = fps, \
                        number_of_captures = number_of_captures, \
                        capture_window = (capture_window[0], capture_window[1]), \
                        breath_hold_window = (breath_hold_window[0], breath_hold_window[1]), \
                        number_of_detector_locations = number_of_chips, \
                        number_of_source_locations = patterns_per_frame, \
                        nir_source_wavelength = '680nm', \
                        ir_source_wavelength = '850nm', \
                        nir_source_array_index = 1, \
                        ir_source_array_index = 2, \
                        functional_detectors = working_detectors_matlab, \
                        functional_nir_sources = working_nir_sources_matlab, \
                        functional_ir_sources = working_ir_sources_matlab, \
                        number_of_bins = number_of_bins, \
                        patch_location = ts['Patch Location'], \
                        test_type = ts['Test Type'], \
                        )
    
    # Create readme string
    st = \
'''################################################### Keys ###################################################
conditions                        - Identifier for the experiment.
hist_t                            - Time axis for histograms (ps). Shape is (number_of_bins).
exp_t                             - Time axis for entire experiment (s). Shape is (number_of_captures).
hist_data                         - Histogram data (raw counts). Shape is (number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures, number_of_bins).
cw_data                           - Integrated histogram data (CW). Shape is (number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures).
integration_time                  - Integration time (s) per source for the histogram data in the experiment.
capture_rate                      - Captures per second. One capture is defined as all source/detector pairs at both wavelengths.
number_of_captures                - Number of captures taken over the course of the experiment.
capture_window                    - Selected captures from original data set.
breath_hold_window                  - Captures during which strap was tightened to simulate venous occlusion. 
number_of_detector_locations      - Number of detectors on the 4x4 array.
number_of_source_locations        - Total number of source locations on the 4x4 array (2 wavelengths present at each location).
nir_source_wavelength             - Wavelength of the NIR sources.
ir_source_wavelength              - Wavelength of the IR sources.
nir_source_array_index            - Index of NIR data in hist_data and cw_data arrays. 
ir_source_array_index             - Index of IR data in hist_data and cw_data arrays. 
functional_detectors              - The detector locations on the 4x4 array that are functional and were used in the experiment.
functional_nir_sources            - The NIR source locations on the 4x4 array that are functional and were used in the experiment. 
functional_ir_sources             - The IR source locations on the 4x4 array that are functional and were used in the experiment. 
number_of_bins                    - The number of bins in a histogram.
patch_location                    - Physical location of the 4x4 array during the experiment.
test_type                         - Type of experiment that was performed.

############################################ Source/Detector Mapping ############################################
  ___________________
|    |    |    |    |
|  0 |  1 |  2 |  3 |
|____|____|____|____|
|    |    |    |    |
|  4 |  5 |  6 |  7 |
|____|____|____|____|
|    |    |    |    |
|  8 |  9 | 10 | 11 |
|____|____|____|____|
|    |    |    |    |
| 12 | 13 | 14 | 15 |
|____|____|____|____|

############################################ Examples ############################################
In Python, array indexes start at 0, so source and detector locations are adjusted so that they start at 0. 
To plot the NIR histogram between Source Location 1 and Detector Location 9 for Capture 20:
--> source_location = 1
--> wavelength_index = 1
--> detector_location = 9
--> capture = 20
--> plot(hist_t, hist_data[source][wavelength_index][detector][capture])

In Python, to plot the IR CW time trace between Source 1 and Detector 9 over the entire experiment:
--> source_location = 1
--> wavelength_index = 2
--> detector_location = 9
--> plot(exp_t, cw_data[source_location][wavelength_index][detector_location])

The plot should have nonzero values if source is found in functional_sources. 
If source is not found in functional_sources, this means that the source was not working or not used in the experiment, and the histogram data will be all 0s.
    '''
        
    # Save a readme file
    print("Saving Python readme file")
    f = open(os.path.join(subdirectory_path, "reconstruction_data_npz_README.txt"), "w")
    f.write(st)
    f.close()
    
    # Saving notes
    print("Saving notes")
    f = open(os.path.join(subdirectory_path, "notes.txt"), "w")
    f.write(ts['Notes'])
    f.close()
        
    print("Done")

