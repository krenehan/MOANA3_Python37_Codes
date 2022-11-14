# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 20:21:22 2022

@author: Kevin Renehan
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# os.chdir('C:\\Users\\Dell-User\\Dropbox\\MOANA\\2020 January Tapeout\\MOANA2 Python Codes\\MOANA2_Python37_Codes\\chips\\moana2\\data\\phantom_roi_5mm\\data')

def roi_raw_histograms(bkg_key, roi_key, capture_window=None, data_dir_prefix=''):
# bkg_key = 'background'
# roi_key = 'roi'
# if True:
    
    # Capture window
    if capture_window is None:
        capture_window_defined = False
    else:
        capture_window_defined = True

    # Interrogate data directory
    dir_list = []
    reduced_dir_list = []
    date_string_present = []
    
    # Filter for only directories
    for d in os.listdir():
        
        # If the path is a directory, we include it
        if os.path.isdir(d):
            
            # Add to directory list
            dir_list.append(d)
            
            # Determine if there is a date in the directory name
            sp = d.split('_')[::-1]
            
            # Length must be greater than 2 if there is a date, because date has 2 underscores alone
            date_string_found = False
            if len(sp) > 2:
                sp = sp[1] + '_' + sp[0]
                
                # Check for underscore and hyphens in exact positions
                if (sp[4] == '-') and (sp[7] == '-') and (sp[10] == '_') and (sp[13] == '-') and (sp[16] == '-'):
                    
                    # Remove the datastring
                    print("date string found")
                    date_string_found = True
                    d = d[0:len(d)-20]
                    
            # Add to list
            date_string_present.append(date_string_found)
            
            # Remove the background string and roi string
            d = d.replace(bkg_key, '')
            d = d.replace(roi_key, '')
            
            # Append to reduced_directory_list
            reduced_dir_list.append(d)
    
    # Dictionary for storing directory pairs
    dir_pairs = {}
    dir_pairs_datestrings = {}
    pair_count = 0
    
    # Pair directories
    for d in reduced_dir_list:
        
        # Only process and find roi directories to match with background
        if bkg_key in d:
            continue
        
        # Create index list, which lists indexes of the directories that match d
        index_list = []
        for i in range(len(reduced_dir_list)):
            if d == reduced_dir_list[i]:
                index_list.append(i)
                
        # Organize pairs of full directory names with background coming first
        if bkg_key in dir_list[index_list[0]]:
            dir_pairs[pair_count] = (dir_list[index_list[0]], dir_list[index_list[1]])
            dir_pairs_datestrings[pair_count] = (date_string_present[index_list[0]], date_string_present[index_list[1]])
        else:
            dir_pairs[pair_count] = (dir_list[index_list[1]], dir_list[index_list[0]])
            dir_pairs_datestrings[pair_count] = (date_string_present[index_list[1]], date_string_present[index_list[0]])
                
        # Increment pair counter
        pair_count = pair_count + 1
        
        # Create time axis
        t_ns = np.arange(0,150)*0.065
        
    # Main contrast loop
    for p in range(len(dir_pairs)):
        
        # Lengths for filenames and print statements
        if dir_pairs_datestrings[p][0]:
            bkg_term_len = len(dir_pairs[p][0])-20
        else:
            bkg_term_len = len(dir_pairs[p][0])
        if dir_pairs_datestrings[p][1]:
            roi_term_len = len(dir_pairs[p][1])-20
        else:
            roi_term_len = len(dir_pairs[p][1])
        
        # Load background captures
        bkg_captures = np.load(os.path.join(dir_pairs[p][0], 'captures.npz'))['data']
        
        # Load roi captures
        roi_captures = np.load(os.path.join(dir_pairs[p][1], 'captures.npz'))['data']
        
        # Get information about shape
        number_of_captures, number_of_chips, number_of_frames, number_of_sources, number_of_bins = np.shape(bkg_captures)
        
        # Reduce captures and frames to only capture axis
        bkg_captures = np.transpose(bkg_captures, axes=(0,2,1,3,4))
        bkg_captures = np.reshape(bkg_captures, newshape=(number_of_captures * number_of_frames, number_of_chips, number_of_sources, number_of_bins))
        roi_captures = np.transpose(roi_captures, axes=(0,2,1,3,4))
        roi_captures = np.reshape(roi_captures, newshape=(number_of_captures * number_of_frames, number_of_chips, number_of_sources, number_of_bins))
        
        # Capture modification
        if capture_window_defined:
            # Pull out only captures that we need
            bkg_captures = bkg_captures[capture_window[0]: capture_window[1]]
            roi_captures = roi_captures[capture_window[0]: capture_window[1]]
            number_of_captures = capture_window[1] - capture_window[0]
        else:
            capture_window = [0, number_of_captures]
        
        # Rearrange as source/detectors
        bkg_captures = np.transpose(bkg_captures, axes=(0,2,1,3))
        roi_captures = np.transpose(roi_captures, axes=(0,2,1,3))
        
        # Average over frames
        bkg_captures = np.average(bkg_captures, axis=(0,))
        roi_captures = np.average(roi_captures, axis=(0,))
        
        # Check for existence of figures directory
        path_string = os.path.join('..\\' + data_dir_prefix + 'figures\\histograms_{}to{}'.format(capture_window[0], capture_window[1]), dir_pairs[p][1][0:roi_term_len])
        if not os.path.exists(path_string):
            Path(path_string).mkdir(parents=True)
        
        # Turn interactive plotting off
        plt.ioff()
        
        # Print status
        print("Plotting raw histograms for {} and {}".format(dir_pairs[p][0][0:bkg_term_len], dir_pairs[p][1][0:roi_term_len]))
        
        # Create a plot
        fig = plt.figure()
        for s in range(number_of_sources):
            for d in range(number_of_chips):
                plt.plot(t_ns, bkg_captures[s][d], label='bkg', color='blue')
                plt.plot(t_ns, roi_captures[s][d], label='roi', color='red')
                plt.title("Source {}, Detector {} Histogram".format(s, d))
                plt.xlabel("Time (ns)")
                plt.ylabel("Counts")
                plt.legend()
                plt.savefig(os.path.join(path_string, 's{:02d}_d{:02d}.png'.format(s, d)))
                plt.cla()
        
        

        
