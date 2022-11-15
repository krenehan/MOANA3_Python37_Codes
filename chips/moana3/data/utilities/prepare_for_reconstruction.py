# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Kevin Renehan

"""

import numpy as np
import os
from scipy.io import savemat
from interpret_test_setup import interpret_test_setup
from interpret_emitter_pattern import interpret_emitter_pattern
from interpret_yield import interpret_yield


def prepare_for_reconstruction(capture_window = None):
    
    # Check for capture window
    if capture_window == None:
        capture_window_specified = False
    else:
        capture_window_specified = True

    # Directory info
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
    if 'emitter_pattern.npy' not in filelist:
        print("Could not find emitter pattern file")
        found = False
    else:
        print("Found emitter pattern file")
        
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
        
        # Load emitter pattern file
        print("Loading emitter pattern file")
        ep = interpret_emitter_pattern()
        
        # Interpret test setup
        print("Loading test setup file")
        ts = interpret_test_setup()
        
        # Used detectors
        print("Loading yield file")
        working_sources, working_detectors =  interpret_yield()
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
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
        
        # Fill capture_window if not specified
        else:
            capture_window = (0, number_of_captures)
        
        # Average
        print("Averaging captures")
        acc = np.mean(arr, axis=0)

        # Create final array
        final = np.zeros((number_of_chips, number_of_chips, number_of_bins), dtype=float)
        
        # Fill final array
        print("Filling output array")
        for s in range(number_of_chips):
            
            # Check to see if the source is functional
            if not (s in working_sources):
                print("Skipping source " + str(s) + " because it is non-functional")
                continue
            
            # Find the source index
            p = np.where(ep==s)[0]
            
            # Check that we got something
            if len(p) == 0:
                continue
            if len(p) > 1:
                raise Exception("Found " + str(len(p)) + " source entries for emitter " + str(s) + " in emitter pattern")
            
            # Extract the index
            pattern_index = p[0]
            
            # Fill
            for chip in range(number_of_chips):
                if chip in working_detectors:
                    final[s][chip] = acc[chip][0][pattern_index]
                else:
                    print("Skipping detector " + str(chip) + " because it is non-functional")
            print("Filled index " + str(s) + " of final array with data from pattern " + str(pattern_index))

        # Create time axis
        t = np.linspace(0, 149, num=150, dtype=int) * 65
        
        # Calculate integration time
        it = float(ts['Period']) * float(ts['Measurements per Pattern']) * float(ts['Number of Frames']) * number_of_captures


        ##### MATLAB #####
        working_detectors_matlab = [i+1 for i in working_detectors]
        working_sources_matlab = [i+1 for i in working_sources]

        # Create dictionary for save
        ddict = {}
        ddict['conditions'] = ts['Conditions']
        ddict['t'] = t
        ddict['data'] = final
        # ddict['sources'] = ep_shuffled
        ddict['integration_time'] = it
        ddict['capture_window'] = capture_window
        ddict['number_of_detectors'] = number_of_chips
        ddict['number_of_sources'] = patterns_per_frame
        ddict['functional_detectors'] = working_detectors_matlab
        ddict['functional_sources'] = working_sources_matlab
        ddict['number_of_bins'] = number_of_bins
        ddict['roi_w'] = ts['ROI Size']
        ddict['roi_l'] = ts['ROI Size']
        # ddict['roi_h'] = 5
        # ddict['roi_ua'] = float(ts['ROI ua'])
        # ddict['laser_wavelength'] = int(ts['Laser Wavelength'])
        
        # Filename
        if capture_window_specified:
            filestring = 'reconstruction_data_it' + str(round(it*1000)) + "ms"
        else:
            filestring = 'reconstruction_data'
            
        # Save accumulated results
        print("Saving averaged .mat file")
        savemat(filestring + '.mat', ddict)
        
        # Create readme string
        st = \
'''################################################### Keys ###################################################
conditions              - Identifier for the experiment.
t                       - Time axis for histograms (ps). Shape is (number_of_bins).
data                    - Histogram data (raw counts). Shape is (number_of_sources, number_of_detectors, number_of_bins).
integration_time        - Integration time (s) for the histogram data in the experiment.
capture_window          - Selected captures from original data set.
number_of_detectors     - Number of detectors on the 4x4 array.
number_of_sources       - Number of sources on the 4x4 array.
functional_sources      - The sources on the 4x4 array that are functional and were used in the experiment. 
functional_detectors    - The detectors on the 4x4 array that are functional and were used in the experiment.
number_of_bins          - The number of bins in a histogram.
roi_w                   - Width of the ROI (mm).
roi_l                   - Length of the ROI (mm).
roi_h                   - Height of the ROI (mm).
roi_ua                  - Absorption coefficient of the ROI (mm^-1).
laser_wavelength        - Wavelength of the laser diode (nm).

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
In Matlab, to plot the histogram between Source 1 and Detector 9 versus time:
--> source = 1
--> detector = 9
--> plot(t, data(source, detector))

The plot should have nonzero values if source is found in functional_sources. 
If source is not found in functional_sources, this means that the source was not working or not used in the experiment, and the histogram data will be all 0s.
        '''
        
        # Save a readme file
        print("Saving MATLAB readme file")
        f = open("reconstruction_data_mat_README.txt", "w")
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
                            t = t, \
                            data = final, \
                            integration_time = it, \
                            capture_window = capture_window, \
                            number_of_detectors = number_of_chips, \
                            number_of_sources = patterns_per_frame, \
                            functional_sources = working_sources, \
                            functional_detectors = working_detectors, \
                            number_of_bins = number_of_bins, \
                            roi_w = ts['ROI Size'], \
                            roi_l = ts['ROI Size'], \
                            # roi_h = 5, \
                            # roi_ua = float(ts['ROI ua']), \
                            # laser_wavelength = int(ts['Laser Wavelength']) \
                            )
        
        # Create readme string
        st = \
'''################################################### Keys ###################################################
conditions              - Identifier for the experiment.
t                       - Time axis for histograms (ps). Shape is (number_of_bins).
data                    - Histogram data (raw counts). Shape is (number_of_sources, number_of_detectors, number_of_bins).
integration_time        - Integration time (s) for the histogram data in the experiment. 
capture_window          - Selected captures from original data set.
number_of_detectors     - Number of detectors on the 4x4 array.
number_of_sources       - Number of sources on the 4x4 array.
functional_sources      - The sources on the 4x4 array that are functional and were used in the experiment. 
functional_detectors    - The detectors on the 4x4 array that are functional and were used in the experiment.
number_of_bins          - The number of bins in a histogram.
roi_w                   - Width of the ROI (mm).
roi_l                   - Length of the ROI (mm).
roi_h                   - Height of the ROI (mm).
roi_ua                  - Absorption coefficient of the ROI (mm^-1).
laser_wavelength        - Wavelength of the laser diode (nm).

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
To plot the histogram between Source 1 and Detector 9 versus time:
--> source = 1
--> detector = 9
--> plot(t, data[source][detector])

The plot should have nonzero values if source is found in functional_sources. 
If source is not found in functional_sources, this means that the source was not working or not used in the experiment, and the histogram data will be all 0s.
        '''
            
        # Save a readme file
        print("Saving Python readme file")
        f = open("reconstruction_data_npz_README.txt", "w")
        f.write(st)
        f.close()
            
        print("Done")

