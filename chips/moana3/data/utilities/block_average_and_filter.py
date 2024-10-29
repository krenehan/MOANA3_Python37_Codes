# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 21:55:03 2024

@author: Dell-User
"""

import numpy as np
import signal_processing_functions as spf
import os
import sys
from scipy.io import savemat

def block_average_and_filter(hpcutoff=0.02, lpcutoff=0.3, order=5, block_average_time_window=(-10, 20)):

    # This directory
    this_dir = os.path.basename(os.getcwd())
    
    # This function
    this_func = "block_average_and_filter"
    
    # Print header
    header = "    " + this_func + " in " + this_dir + ": "
    
    # Starting
    print(header + "Starting")
    
    # Filename
    filestring = 'processed_reconstruction_data'
    
    # Directory info
    l = os.listdir()
    filelist = []
    for f in l:
        if os.path.isfile(f):
            filelist.append(f)
            
    # Look for previously generated accumulated file
    print(header + "Searching for reconstruction data file")
    found = True
        
    # Look for captures file
    if 'reconstruction_data.npz' not in filelist:
        print(header + "Could not find reconstruction data file")
        found = False
    else:
        print(header + "Found reconstruction data file")
    
    # Check that all necessary files were found
    if not found:
        print(header + "ERROR - One or more necessary files not found")
        # return -1
    
    # Load the file
    npz = np.load('reconstruction_data.npz', allow_pickle=True)
    
    # Check that triggering is present in the archive
    if 'stim_onset' not in list(npz.keys()):
        print(header + "ERROR - Triggering information not included in reconstruction data file")
        # return -1
        
    # Load everything into a new archive that can be modified
    new_npz = {}
    for k in npz.keys():
        new_npz[k] = npz[k]
    # del npz
    
    # Grab mean of data beforehand
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(new_npz['hist_t'], new_npz['hist_data'][0][1][9][20], label='raw' )
    hist_data_mean = np.mean(new_npz['hist_data'], axis=3)
    hist_data_mean = np.array([hist_data_mean for i in range(new_npz['hist_data'].shape[3])])
    hist_data_mean = np.transpose(hist_data_mean, axes=(1,2,3,0,4))
    
    # Set
    new_hist_data = new_npz['hist_data']
    
    # Highpass filter data
    print(header + "Highpass filtering data")
    if hpcutoff != None:
        new_hist_data = spf.butterhp_filtfilt(new_hist_data, hpcutoff, new_npz['capture_rate'], order=order, axis=3)
        plt.plot(new_npz['hist_t'], new_hist_data[0][1][9][20], label='after highpass' )
    
    # Lowpass filter data
    print(header + "Lowpass filtering data")
    if lpcutoff != None:
        new_hist_data = spf.butterlp_filtfilt(new_hist_data, lpcutoff, new_npz['capture_rate'], order=order, axis=3)
        plt.plot(new_npz['hist_t'], new_hist_data[0][1][9][20], label='after lowpass' )
    
    # Add the mean back so histograms look normal following highpass filter (if we used the highpass filter)
    if hpcutoff != None:
        new_hist_data = new_hist_data + hist_data_mean
        plt.plot(new_npz['hist_t'], new_hist_data[0][1][9][20], label='after mean' )
        plt.legend()
    
    # Run the block averaging once per stim onset
    t_prior = abs(block_average_time_window[0])
    t_after = abs(block_average_time_window[1])
    tba = [None for i in range(len(new_npz['stim_onset']))]
    ba = [None for i in range(len(new_npz['stim_onset']))]
    for i in range(len(new_npz['stim_onset'])):
        tba[i], ba[i] = spf.block_average(new_npz['exp_t'], new_npz['stim_onset'][i], new_hist_data, t_prior=t_prior, t_after=t_after, axis=3)
    tba = np.array(tba)
    ba = np.array(ba)
    
    # Prepare the new archive
    del new_npz['hist_data'], new_npz['cw_data'], new_npz['breath_hold_window']
    new_npz['nir_hist_data'] = np.transpose(new_hist_data, axes=(1,0,2,3,4))[0]
    new_npz['ir_hist_data'] = np.transpose(new_hist_data, axes=(1,0,2,3,4))[1]
    new_npz['cw_data'] = np.sum(new_hist_data, axis=4)
    new_npz['lowpass_cutoff'] = float(lpcutoff) if (lpcutoff != None) else 'None'
    new_npz['highpass_cutoff'] = float(hpcutoff) if (hpcutoff != None) else 'None'
    new_npz['filter_order'] = float(order)
    new_npz['filter_response'] = 'butter'
    new_npz['block_average_window'] = np.array(block_average_time_window)
    new_npz['block_average_time_axis'] = tba
    new_npz['block_average_nir_hist_data'] = np.transpose(ba, axes=(2,0,1,3,4,5))[0]
    new_npz['block_average_ir_hist_data'] = np.transpose(ba, axes=(2,0,1,3,4,5))[1]
    
    # For MATLAB files, we need to check that the array is not too large to save
    if new_npz['nir_hist_data'].nbytes > ((2**32)*2-1):
        print(header + "Cannot save .mat file because hist_data variable is too large")
    else:            
        # Save accumulated results
        print(header + "Saving averaged .mat file")
        savemat(filestring + '.mat', new_npz)
    
    # Create readme string
    st = \
'''################################################### Keys ###################################################
conditions                        - Identifier for the experiment.
hist_t                            - Time axis for histograms (ps). Shape is (number_of_bins).
exp_t                             - Time axis for entire experiment (s). Shape is (number_of_captures).
nir_hist_data                     - Filtered histogram data (raw counts) for NIR wavelength. Shape is (number_of_sources, number_of_detectors, number_of_captures, number_of_bins).
ir_hist_data                      - Filtered histogram data (raw counts) for IR wavelength. Shape is (number_of_sources, number_of_detectors, number_of_captures, number_of_bins).
cw_data                           - Filtered and integrated histogram data (CW). Shape is (number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures).
integration_time                  - Integration time (s) per source for the histogram data in the experiment.
capture_rate                      - Captures per second. One capture is defined as all source/detector pairs at both wavelengths.
number_of_captures                - Number of captures taken over the course of the experiment.
capture_window                    - Selected captures from original data set.
breath_hold_window                - Captures during which strap was tightened to simulate venous occlusion. 
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
number_of_stimuli                 - Number of stimuli in experiment (including rest).
stim_onset                        - Psuedo-delta function showing onset timing of stimuli. Shape is (number_of_stimuli, number_of_captures)
stim_boxcar                       - Boxcar functions showing onset and duration of stimuli. Shape is (number_of_stimuli, number_of_captures). 
stim_dict                         - Struct containing index of each stimuli in stim_onset. Number of fields is number_of_stimuli.
lowpass_cutoff                    - Cutoff frequency for the lowpass filter applied to the data.
highpass_cutoff                   - Cutoff frequency for the highpass filter applied to the data.
filter_order                      - Filter order. Will be doubled because this is a forward/backward filter.
filter_response                   - The type of filter used.
block_average_window              - Time before and time after a stimulus to start and end the block average. 
block_average_time_axis           - Time axis for block average. Shape is (number_of_stimuli, number_of_block_average_timepoints)
block_average_nir_hist_data       - Block averaged NIR data. Shape is (number_of_stimuli, number_of_sources, number_of_detectors, number_of_block_average_timepoints, number_of_bins)
block_average_ir_hist_data        - Block averaged IR data. Shape is (number_of_stimuli, number_of_sources, number_of_detectors, number_of_block_average_timepoints, number_of_bins)

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
--> detector_location = 9;
--> capture = 20;
--> plot(hist_t, squeeze(nir_hist_data(source_location, detector_location, capture, :)));

In Matlab, to plot the IR histogram between Source Location 2 and Detector Location 10 for Capture 24:
--> source_location = 2;
--> detector_location = 10;
--> capture = 24;
--> plot(hist_t, squeeze(ir_hist_data(source_location, detector_location, capture, :)));

In Matlab, to plot the NIR CW time trace between Source 1 and Detector 9 over the entire experiment:
--> source_location = 1;
--> wavelength_index = 1;
--> detector_location = 9;
--> plot(exp_t, squeeze(cw_data(source_location, wavelength_index, detector_location, :)));

In Matlab, to plot the IR CW time trace between Source 1 and Detector 9 over the entire experiment:
--> source_location = 1;
--> wavelength_index = 2;
--> detector_location = 9;
--> plot(exp_t, squeeze(cw_data(source_location, wavelength_index, detector_location, :)));

To add the thumb stimulation timing information to the plot above:
--> hold on;
--> stim_to_plot = stim_onset(stim_dict.thumb, :) * max(cw_data(source_location, wavelength_index, detector_location, :));
--> plot(exp_t, stim_to_plot);
--> hold off;

The plots should have nonzero values if source is found in functional_sources. 
If a NIR/IR source is not found in functional_nir_sources/functional_ir_sources, this means that the NIR/IR source was not working or not used in the experiment, and the histogram data will be all 0s.
    '''
    
    # Save a readme file
    print(header + "Saving MATLAB readme file")
    f = open(filestring + "_mat_README.txt", "w")
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
    
    print(header + "Saving .npz file")
    np.savez_compressed ( \
                        filestring, \
                        conditions = new_npz['conditions'], \
                        hist_t = new_npz['hist_t'], \
                        hist_data = new_hist_data, \
                        exp_t = new_npz['exp_t'], \
                        cw_data = new_npz['cw_data'], \
                        integration_time = new_npz['integration_time'], \
                        capture_rate = new_npz['capture_rate'], \
                        number_of_captures = new_npz['number_of_captures'], \
                        capture_window = new_npz['capture_window'], \
                        number_of_detector_locations = new_npz['number_of_detector_locations'], \
                        number_of_source_locations = new_npz['number_of_source_locations'], \
                        nir_source_wavelength = new_npz['nir_source_wavelength'], \
                        ir_source_wavelength = new_npz['ir_source_wavelength'], \
                        nir_source_array_index = new_npz['nir_source_array_index'], \
                        ir_source_array_index = new_npz['ir_source_array_index'], \
                        functional_detectors = new_npz['functional_detectors'], \
                        functional_nir_sources = new_npz['functional_nir_sources'], \
                        functional_ir_sources = new_npz['functional_ir_sources'], \
                        number_of_bins = new_npz['number_of_bins'], \
                        patch_location = new_npz['patch_location'], \
                        test_type = new_npz['test_type'], \
                        number_of_stimuli = new_npz['number_of_stimuli'], \
                        stim_onset = new_npz['stim_onset'], \
                        stim_boxcar = new_npz['stim_boxcar'], \
                        stim_dict = new_npz['stim_dict'], \
                        lowpass_cutoff = new_npz['lowpass_cutoff'], \
                        highpass_cutoff = new_npz['highpass_cutoff'], \
                        filter_order = new_npz['filter_order'], \
                        filter_response = new_npz['filter_response'], \
                        block_average_window = new_npz['block_average_window'], \
                        block_average_time_axis = new_npz['block_average_time_axis'], \
                        block_average_hist_data = ba, \
                        )
        
    # Create readme string
    st = \
'''################################################### Keys ###################################################
conditions                        - Identifier for the experiment.
hist_t                            - Time axis for histograms (ps). Shape is (number_of_bins).
exp_t                             - Time axis for entire experiment (s). Shape is (number_of_captures).
hist_data                         - Filtered histogram data (raw counts). Shape is (number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures, number_of_bins).
cw_data                           - Filtered, integrated histogram data (CW). Shape is (number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures).
integration_time                  - Integration time (s) per source for the histogram data in the experiment.
capture_rate                      - Captures per second. One capture is defined as all source/detector pairs at both wavelengths.
number_of_captures                - Number of captures taken over the course of the experiment.
capture_window                    - Selected captures from original data set.
breath_hold_window                - Captures during which strap was tightened to simulate venous occlusion. 
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
number_of_stimuli                 - Number of stimuli in experiment (including rest).
stim_onset                        - Psuedo-delta function showing onset timing of stimuli. Shape is (number_of_stimuli, number_of_captures)
stim_boxcar                       - Boxcar functions showing onset and duration of stimuli. Shape is (number_of_stimuli, number_of_captures). 
stim_dict                         - Dictionary containing index of each stimuli in stim_onset. Length is number_of_stimuli.
lowpass_cutoff                    - Cutoff frequency for the lowpass filter applied to the data.
highpass_cutoff                   - Cutoff frequency for the highpass filter applied to the data.
filter_order                      - Filter order. Will be doubled because this is a forward/backward filter.
filter_response                   - The type of filter used.
block_average_window              - Time before and time after a stimulus to start and end the block average. 
block_average_time_axis           - Time axis for block average. Shape is (number_of_stimuli, number_of_block_average_timepoints)
block_average_hist_data           - Block averaged histogram data. Shape is (number_of_stimuli, number_of_sources, number_of_wavelengths, number_of_detectors, number_of_block_average_timepoints, number_of_bins)

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
--> wavelength_index = 0
--> detector_location = 9
--> capture = 20
--> plt.plot(hist_t, hist_data[source][wavelength_index][detector][capture])

In Python, to plot the IR CW time trace between Source 1 and Detector 9 over the entire experiment:
--> source_location = 1
--> wavelength_index = 1
--> detector_location = 9
--> plt.plot(exp_t, cw_data[source_location][wavelength_index][detector_location])

To add the thumb stimulation timing information to the plot above:
--> stim_to_plot = stim_boxcar[stim_dict.thumb] * max(cw_data[source_location][wavelength_index][detector_location])
--> plt.plot(exp_t, stim_to_plot)



The plot should have nonzero values if source is found in functional_sources. 
If source is not found in functional_sources, this means that the source was not working or not used in the experiment, and the histogram data will be all 0s.
    '''
        
    # Save a readme file
    print(header + "Saving Python readme file")
    f = open(filestring+"_npz_README.txt", "w")
    f.write(st)
    f.close()
        
    print(header + "Done")
    return 0


# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    
    # Highpass cutoff
    hpcutoff = None
    
    # Lowpass cutoff
    lpcutoff = 0.3
    
    # Filter order (will be doubled by filtfilt)
    order = 5
    
    # Time window for block average
    block_average_time_window = (-2, 20)
    
    # Select a data directory
    target_dir = easygui.diropenbox(title="Choose directory containing reconstruction_data.npz file")
    
    # Check
    if target_dir == None:
        raise Exception("Target directory not provided")
    
    # Move to data directory
    os.chdir(target_dir)
    
    # Run
    block_average_and_filter(hpcutoff=hpcutoff, lpcutoff=lpcutoff, order=order, block_average_time_window=block_average_time_window)
    
    
    
    
    
    
    
    
    
    
    
    
    