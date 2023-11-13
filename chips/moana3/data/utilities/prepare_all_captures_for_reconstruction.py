# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@purpose:   Prepare phantom experiment data for reconstruction.

@usage:     Standalone or in target script.

@prereqs:   zip_files()

@author:    Kevin Renehan

"""

import numpy as np
import os
from scipy.io import savemat
from interpret_test_setup import interpret_test_setup
from interpret_emitter_pattern import interpret_emitter_pattern
from interpret_yield import interpret_yield

this_dir = os.getcwd()
os.chdir("..\\..\\platform")
import DynamicPacket
os.chdir(this_dir)


def prepare_all_captures_for_reconstruction(capture_window = None):
    
    # This directory
    this_dir = os.path.basename(os.getcwd())
    
    # This function
    this_func = "prepare_all_captures_for_reconstruction"
    
    # Print header
    header = "    " + this_func + " in " + this_dir + ": "
    
    # Starting
    print(header + "Starting")
    
    # Check for capture window
    capture_window = None
    if capture_window == None:
        capture_window_specified = False
    else:
        capture_window_specified = True

    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print(header + "Searching for zipped captures file, emitter pattern file, test setup, and yield file")
    found = True
        
    # Look for captures file
    if 'captures.npz' not in filelist:
        print(header + "Could not find zipped captures file")
        found = False
    else:
        print(header + "Found zipped captures file")

        
    # Look for emitter pattern file
    if ('emitter_pattern.npy' not in filelist) and ('dynamic_packet.txt' not in filelist):
        print(header + "Could not find emitter pattern or dynamic packet file")
        found = False
    else:
        if 'dynamic_packet.txt' in filelist:
            print(header + "Found dynamic packet file")
            legacy = False
            
        elif 'emitter_pattern.npy' in filelist:
            print(header + "Found emitter pattern file")
            legacy = True
        
        
    # Look for test setup file
    if 'test_setup.txt' not in filelist:
        print(header + "Could not find test setup file")
        found = False
    else:
        print(header + "Found test setup file")
        
    # Look for yield file
    if 'yield.txt' not in filelist:
        print(header + "Could not find yield file")
        found = False
    else:
        print(header + "Found yield file")
            
    if not found:
        
        print(header + "One or more necessary files not found")
        return -1
        
    else:
        
        # Load
        print(header + "Loading captures file")
        arr = np.load('captures.npz')['data']
        
        # Load emitter pattern file
        if legacy:
            print(header + "Loading emitter pattern file")
            ep = interpret_emitter_pattern()
        else:
            print(header + "Loading emitter pattern file")
        
        # Interpret test setup
        print(header + "Loading test setup file")
        ts = interpret_test_setup()
        
        # Used detectors
        print(header + "Loading yield file")
        if legacy:
            working_nir_sources, working_detectors =  interpret_yield()
            working_ir_sources = working_nir_sources
        else:
            working_nir_sources, working_ir_sources, working_detectors =  interpret_yield()
            
        # Number of wavelengths
        number_of_wavelengths = 2
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
        # Combine the capture and frame axes
        arr = np.transpose(arr, axes=(0, 2, 1, 3, 4))
        arr = np.reshape(arr, newshape=(number_of_captures*number_of_frames, 1, number_of_chips, patterns_per_frame, number_of_bins))
        arr = np.transpose(arr, axes=(0, 2, 1, 3, 4)) # Shape is [capture, detector, frame, source, bin]
        
        # Modify number of captures and frames
        number_of_captures = number_of_captures * number_of_frames
        number_of_frames = 1
        
        # Dynamic packets
        if not legacy:
            dp = DynamicPacket.DynamicPacket(number_of_chips, patterns_per_frame)
            dp.read("dynamic_packet.txt")
        
        # If we have a custom capture window, we redefine the number of captures to be included
        if capture_window_specified:
            if capture_window[0] >= capture_window[1]:
                print(header + "Second index of capture window greater than or equal to first index")
                return -1
            if capture_window[0] < 0:
                print(header + "First index of capture window is less than 0")
                return -1
            if capture_window[0] > len(arr):
                print(header + "First index of capture window is greater than the number of captures")
                return -1
            if capture_window[1] < 0:
                print(header + "Second index of capture window is less than 0")
                return -1
            if capture_window[1] > len(arr):
                print(header + "Second index of capture window is greater than the number of captures".format)
                return -1
            arr = arr[capture_window[0]:capture_window[1]]
            number_of_captures = capture_window[1] - capture_window[0]
        
        # Fill capture_window if not specified
        else:
            capture_window = (0, number_of_captures)
            
        # Transpose to [detector, frame, source, capture, bin]
        arr = np.transpose(arr, axes=(1, 2, 3, 0, 4))

        # Create final array
        final = np.zeros((number_of_chips, number_of_wavelengths, number_of_chips, number_of_captures, number_of_bins), dtype=int)
        
        # Legacy style with only a single wavelength and emitter pattern file finds the source in the emitter pattern structure
        if legacy:
            
            # Fill final array
            print(header + "Filling output array")
            for s in range(number_of_chips):
                
                # Check to see if the source is functional
                if not (s in working_nir_sources):
                    print(header + "Skipping source " + str(s) + " because it is non-functional")
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
                        final[s][0][chip] = arr[chip][0][pattern_index]
                    else:
                        print(header + "Skipping detector " + str(chip) + " because it is non-functional")
                print(header + "Filled index " + str(s) + " of final array with data from pattern " + str(pattern_index))
                
        else:
            
            # Fill final array
            print(header + "Filling output array")
            
            # Go through each pattern
            for p in range(patterns_per_frame):
                
                # Get the source for this pattern
                eip = dp.emitters_for_pattern(p)
                if len(eip) < 1:
                    raise Exception(header + "emitter not found for pattern " + str(p))
                elif len(eip) > 1:
                    raise Exception(header + "multiple emitters found for pattern " + str(p) + ": " + str(eip))
                else:
                    s = eip[0]
                    
                # Get the wavelength for this pattern
                wip = dp.wavelength_for_pattern(p)
                if len(np.shape(wip)) == 0:
                    w = wip
                else:
                    raise Exception(header + "wavelength not found for pattern " + str(p))
                
                # Check to see if the source is functional
                if w == 0:
                    if not (s in working_nir_sources):
                        print(header + "Skipping NIR source " + str(s) + " because it is non-functional")
                        continue
                elif w == 1:
                    if not (s in working_ir_sources):
                        print(header + "Skipping IR source " + str(s) + " because it is non-functional")
                
                # Fill
                for chip in range(number_of_chips):
                    if chip in working_detectors:
                        final[s][w][chip] = arr[chip][0][p]
                    else:
                        print(header + "Skipping detector " + str(chip) + " because it is non-functional")
                print(header + "Filled index " + str(s) + " of final array with data from pattern " + str(p))
                
        
        # Transpose to final shape [capture x source x wavelength x detector x bin]
        final = np.transpose(final, axes=(3,0,1,2,4))
    
        # Create time axis
        t = np.linspace(0, 149, num=150, dtype=int) * 65
        
        # Calculate integration time
        it = float(ts['Period']) * 1e-9 * float(ts['Measurements per Pattern'])


        ##### MATLAB #####
        working_detectors_matlab = [i+1 for i in working_detectors]
        working_nir_sources_matlab = [i+1 for i in working_nir_sources]
        working_ir_sources_matlab = [i+1 for i in working_ir_sources]

        # Create dictionary for save
        ddict = {}
        ddict['conditions'] = ts['Conditions']
        ddict['t'] = t
        ddict['data'] = final
        # ddict['sources'] = ep_shuffled
        ddict['integration_time'] = it
        ddict['capture_window'] = capture_window
        ddict['number_of_captures'] = number_of_captures
        ddict['number_of_detectors'] = number_of_chips
        ddict['number_of_sources'] = patterns_per_frame
        ddict['functional_detectors'] = working_detectors_matlab
        ddict['functional_nir_sources'] = working_nir_sources_matlab
        ddict['functional_ir_sources'] = working_ir_sources_matlab
        ddict['number_of_bins'] = number_of_bins
        ddict['roi_w'] = ts['ROI Size'] if 'ROI Size' in ts.keys() else 0
        ddict['roi_l'] = ts['ROI Size'] if 'ROI Size' in ts.keys() else 0
        ddict['roi_h'] = ts['ROI Size'] if 'ROI Size' in ts.keys() else 0
        ddict['roi_ua'] = float(ts['ROI ua']) if 'ROI ua' in ts.keys() else 0
        ddict['laser_wavelength'] = int(ts['Laser Wavelength']) if 'Laser Wavelength' in ts.keys() else 0
        
        # Filename
        if capture_window_specified:
            filestring = 'reconstruction_data_it' + str(round(it*1000)) + "ms"
        else:
            filestring = 'reconstruction_data_individual_captures'
            
        # Save accumulated results
        print(header + "Saving averaged .mat file")
        savemat(filestring + '.mat', ddict)
        
        # Create readme string
        st = \
'''################################################### Keys ###################################################
conditions               - Identifier for the experiment.
t                        - Time axis for histograms (ps). Shape is (number_of_bins).
data                     - Histogram data (raw counts). Shape is (number_of_captures, number_of_sources, number_of_wavelengths, number_of_detectors, number_of_bins).
integration_time         - Integration time (s) for the histogram data in the experiment.
capture_window           - Selected captures from original data set.
number_of_captures       - Number of individual captures collected. 
number_of_detectors      - Number of detectors on the 4x4 array.
number_of_sources        - Number of sources on the 4x4 array.
number_of_wavelengths    - Number of wavelengths on the 4x4 array.
functional_sources       - The sources on the 4x4 array that are functional and were used in the experiment. 
functional_nir_detectors - The NIR detectors on the 4x4 array that are functional and were used in the experiment.
functional_ir_detectors  - The IR detectors on the 4x4 array that are functional and were used in the experiment.
number_of_bins           - The number of bins in a histogram.
roi_w                    - Width of the ROI (mm).
roi_l                    - Length of the ROI (mm).
roi_h                    - Height of the ROI (mm).

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
--> source_location = 1;
--> wavelength = 1;
--> detector_location = 9;
--> capture = 20;
--> plot(t, squeeze(data(capture, source_location, detector_location, :)));

The plots should have nonzero values if source is found in functional_sources. 
If a source is not found in functional_sources, this means that the source was not working or not used in the experiment, and the histogram data will be all 0s.
Please note that for the wavelength axis, index 1 is NIR and index 2 is IR.
        '''
        
        # Save a readme file
        print(header + "Saving MATLAB readme file")
        f = open("reconstruction_data_individual_captures_mat_README.txt", "w")
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
        
        roi_size = ts['ROI Size'] if 'ROI Size' in ts.keys() else 0
        roi_ua = ts['ROI ua'] if 'ROI ua' in ts.keys() else 0
        laser_wavelength = ts['Laser Wavelength'] if 'Laser Wavelength' in ts.keys() else 0
        
        print(header + "Saving .npz file")
        np.savez_compressed ( \
                            filestring, \
                            conditions = ts['Conditions'], \
                            t = t, \
                            data = final, \
                            integration_time = it, \
                            capture_window = capture_window, \
                            number_of_captures = number_of_captures, \
                            number_of_detectors = number_of_chips, \
                            number_of_sources = patterns_per_frame, \
                            functional_nir_sources = working_nir_sources, \
                            functional_ir_sources = working_ir_sources, \
                            functional_detectors = working_detectors, \
                            number_of_bins = number_of_bins, \
                            roi_w = roi_size, \
                            roi_l = roi_size, \
                            roi_h = roi_size, \
                            roi_ua = float(roi_ua), \
                            laser_wavelength = int(laser_wavelength) \
                            )
        
        # Create readme string
        st = \
'''################################################### Keys ###################################################
conditions               - Identifier for the experiment.
t                        - Time axis for histograms (ps). Shape is (number_of_bins).
data                     - Histogram data (raw counts). Shape is (number_of_captures, number_of_sources, number_of_wavelengths, number_of_detectors, number_of_bins).
integration_time         - Integration time (s) for the histogram data in the experiment. 
capture_window           - Selected captures from original data set.
number_of_captures       - Number of individual captures collected. 
number_of_detectors      - Number of detectors on the 4x4 array.
number_of_sources        - Number of sources on the 4x4 array.
number_of_wavelengths    - Number of wavelengths on the 4x4 array.
functional_nir_detectors - The NIR detectors on the 4x4 array that are functional and were used in the experiment.
functional_ir_detectors  - The IR detectors on the 4x4 array that are functional and were used in the experiment.
functional_detectors     - The detectors on the 4x4 array that are functional and were used in the experiment.
number_of_bins           - The number of bins in a histogram.
roi_w                    - Width of the ROI (mm).
roi_l                    - Length of the ROI (mm).
roi_h                    - Height of the ROI (mm).

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
--> wavelength = 0
--> detector_location = 9
--> capture = 20
--> plot(t, data[capture][source_location][wavelength][detector_location])

The plot should have nonzero values if source is found in functional_sources. 
If source is not found in functional_sources, this means that the source was not working or not used in the experiment, and the histogram data will be all 0s.
Please note that for the wavelength axis, index 0 is NIR and index 1 is IR.
        '''
            
        # Save a readme file
        print(header + "Saving Python readme file")
        f = open("reconstruction_data_individual_captures_npz_README.txt", "w")
        f.write(st)
        f.close()
        
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
    prepare_all_captures_for_reconstruction(capture_window = None)