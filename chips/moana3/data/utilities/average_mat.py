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

def map_chip_3by3(chip):
    
    if chip == 2:
        return 1
    elif chip == 3: 
        return 2
    elif chip == 4:
        return 3
    elif chip == 6:
        return 4
    elif chip == 7:
        return 5
    elif chip == 8:
        return 6
    elif chip == 10:
        return 7
    elif chip == 11:
        return 8
    elif chip == 12:
        return 9
    elif chip == 0:
        return -1

def average_mat():

    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for zipped captures file, emitter pattern file, and test setup file")
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
            
    if not found:
        
        raise Exception("One or more files not found")
        
    else:
        
        # Load
        print("Loading captures file")
        arr = np.load('captures.npz')['data']
        
        # Load emitter pattern file
        print("Loading emitter pattern file")
        ep = interpret_emitter_pattern()
        
        # Rearrange ep to be consistent with used_patterns
        ep = np.concatenate( (ep[len(ep)-1:len(ep)], ep[0:len(ep)-1]))
        
        # Interpret test setup
        ts = interpret_test_setup()
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
        # Average
        print("Averaging captures")
        acc = np.mean(arr, axis=0)
        
        #############################################
        ##### CUSTOM SECTION - RESTRUCTURE DATA #####
        #############################################
        
        # Used chips
        used_chips = (2, 3, 4, 6, 7, 8, 10, 11, 12)
        
        # Used sources
        used_patterns = (1, 2, 3, 4, 6)
        
        # Shuffled data array
        acc_shuffled = np.zeros( (len(used_chips), len(used_chips), number_of_bins), dtype=float)
        
        # For keeping track of how many sources were actually used
        functional_sources = []
        
        # Fill shuffled data array
        for s in range(len(used_chips)):
            
            # Source
            source = used_chips[s]
            print("Trying chip " + str(source))
            mapped_source = map_chip_3by3(source)
            print("Mapped source is " + str(mapped_source))
            
            # Check to see if this source was used
            i = np.where(ep == source-1)[0]
            if (len(i) == 0) or source==10:
                continue
            else:
                functional_sources.append(mapped_source)
                source_pattern = i[0]
            
            # Detector
            for d in range(len(used_chips)):
                
                # Actual detector index
                detector = used_chips[d]
                mapped_detector = map_chip_3by3(detector)
                
                # Place data
                print("Packing data from original array at chip {} pattern {} into new array at source {} detector {}".format(detector, source_pattern, mapped_source, mapped_detector))
                acc_shuffled[mapped_source-1][mapped_detector-1] = acc[detector-1][0][source_pattern]
        
        # Redo shape
        patterns_per_frame, number_of_chips, number_of_bins = np.shape(acc_shuffled)
        
        #############################################
        
        #############################################
        ###### CUSTOM SECTION - RESTRUCTURE EP ######
        #############################################
        
        # # Shuffled emitter pattern array
        # ep_shuffled = np.empty( (len(used_patterns), ), dtype=int)
        
        # # List of sources
        # for p in range(patterns_per_frame):
        #     print("Pattern is " + str(used_patterns[p]))
        #     print("Source for pattern is " + str(ep[used_patterns[p]]+1))
        #     print("Maps to chip " + str(map_chip_3by3(ep[used_patterns[p]]+1)))
        #     ep_shuffled[p] = map_chip_3by3(ep[used_patterns[p]]+1)
            
        
        #############################################
        
        # Create time axis
        t = np.linspace(0, 149, num=150, dtype=int) * 65
        
        # Calculate integration time
        it = float(ts['Period'])/2 * float(ts['Measurements per Pattern']) * float(ts['Number of Frames']) * float(ts['Number of Captures'])
        
        # Create dictionary for save
        ddict = {}
        ddict['conditions'] = ts['Conditions']
        ddict['t'] = t
        ddict['data'] = acc_shuffled
        # ddict['sources'] = ep_shuffled
        ddict['integration_time'] = it
        ddict['number_of_detectors'] = number_of_chips
        ddict['number_of_sources'] = patterns_per_frame
        ddict['functional_sources'] = functional_sources
        ddict['number_of_bins'] = number_of_bins
        ddict['roi_w'] = int(ts['ROI Size'])
        ddict['roi_l'] = int(ts['ROI Size'])
        ddict['roi_h'] = 5
        ddict['roi_ua'] = float(ts['ROI ua'])
        ddict['laser_wavelength'] = int(ts['Laser Wavelength'])
            
        # Save accumulated results
        print("Saving averaged .mat file")
        savemat('averaged.mat', ddict)
        
        # Create readme string
        st = \
        '''################################################### Keys ###################################################
conditions          - Identifier for the experiment.
t                   - Time axis for histograms (ps). Shape is (number_of_bins).
data                - Histogram data (raw counts). Shape is (number_of_sources, number_of_detectors, number_of_bins).
integration_time    - Integration time (s) for the histogram data in the experiment. 
number_of_detectors - Number of detectors on the 3x3 array.
number_of_sources   - Number of sources on the 3x3 array.
functional_sources  - The sources on the 3x3 array that are functional and were used in the experiment. 
number_of_bins      - The number of bins in a histogram.
roi_w               - Width of the ROI (mm).
roi_l               - Length of the ROI (mm).
roi_h               - Height of the ROI (mm).
roi_ua              - Absorption coefficient of the ROI (mm^-1).
laser_wavelength    - Wavelength of the laser diode (nm).

############################################ Source/Detector Mapping ############################################
 ____________
|   |   |   |
| 1 | 2 | 3 |
|___|___|___|
|   |   |   |
| 4 | 5 | 6 |
|___|___|___|
|   |   |   |
| 7 | 8 | 9 |
|___|___|___|

############################################ Examples ############################################
To plot the histogram between Source 1 and Detector 9 versus time:
--> source = 1
--> detector = 9
--> plot(t, data[source][detector])

The plot should have nonzero values if source is found in functional_sources. 
If source is not found in functional_sources, this means that the source was not working or not used in the experiment, and the histogram data will be all 0s.
        '''

        
        
        # Save a readme file
        print("Saving readme file")
        f = open("average_mat_README.txt", "w")
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
                            "averaged_mat", \
                            conditions = ts['Conditions'], \
                            t = t, \
                            data = acc_shuffled, \
                            integration_time = it, \
                            number_of_detectors = number_of_chips, \
                            number_of_sources = patterns_per_frame, \
                            functional_sources = functional_sources, \
                            number_of_bins = number_of_bins, \
                            roi_w = int(ts['ROI Size']), \
                            roi_l = int(ts['ROI Size']), \
                            roi_h = 5, \
                            roi_ua = float(ts['ROI ua']), \
                            laser_wavelength = int(ts['Laser Wavelength']) \
                            )
            
        print("Done")

