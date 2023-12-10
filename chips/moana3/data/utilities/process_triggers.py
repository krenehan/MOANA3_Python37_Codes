# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@purpose:   Averages captures in captures.npz to create averaged.npz. 

@usage:     Standalone or in target script.

@prereqs:   zip_files()

@author:    Kevin Renehan
"""

import numpy as np
import os
from pandas import read_table
from interpret_test_setup import interpret_test_setup

def process_triggers():
    
    # This directory
    this_dir = os.path.basename(os.getcwd())
    
    # This function
    this_func = "process_triggers"
    
    # Print header
    header = "    " + this_func + " in " + this_dir + ": "
    
    # File name
    filenames = ['stim_timing.tsv', 'stim.npz']

    # Directory info
    filelist = os.listdir()
    
    # Found
    found = not (False in [ (k in filelist) for k in filenames])
    
    # Check to see if triggers file has been generated
    if found:
        print(header + ' '.join(filenames) + " already generated")
        return 1
    
    # Look for events.tsv file, first_capture.txt, and stim_timing.tsv files
    necessary_files = {'events.tsv': 'events.tsv' in filelist, \
                       'first_capture.txt': 'first_capture.txt' in filelist, \
                       'stim_protocol.tsv': 'stim_protocol.tsv' in filelist, \
                       'captures.npz': 'captures.npz' in filelist, \
                       'test_setup.txt': 'test_setup.txt' in filelist, }
    
    # Determine if all necessary files were found for processing triggers
    found = not (False in [ (k in filelist) for k in necessary_files])

    # Exit if we don't have the things we need
    if not found:
        print(header + "Did not find all required triggering files")
        for k in necessary_files:
            if necessary_files[k]:
                print(header + k + " found")
            else:
                print(header + k + " not found")
        return -1
    
    # Load captures and get necessary information
    number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(np.load("captures.npz")['data'])
    
    # Load test setup and get clock frequency, measurements per pattern
    ts = interpret_test_setup()    
    period = float(ts['Period']) * 1e-9
    measurements_per_pattern = float(ts['Measurements per Pattern'])
    
    # Calculate the time of a single frame
    frame_time = period * measurements_per_pattern * patterns_per_frame
        
    # Load events.tsv
    events_tsv = float(read_table("events.tsv")['Onset'][0])
    
    # Load first_capture.txt
    with open('first_capture.txt') as f:
        first_capture = int(f.readline())
        
    # Load stim_protocol.tsv
    stim_protocol_tsv = read_table("stim_protocol.tsv")

    # Datatype conversion
    stim_protocol_tsv['Onset'] = stim_protocol_tsv['Onset'].astype(float)
    stim_protocol_tsv['Duration'] = stim_protocol_tsv['Duration'].astype(float)
    stim_protocol_tsv['Amplitude'] = stim_protocol_tsv['Amplitude'].astype(float)
    
    # Calculate the elapsed time of the first capture that was logged
    elapsed_time_of_first_capture = first_capture * frame_time * number_of_frames
    
    # Find offset (this basically sets t=0 for capture 0 and determines where the trigger is relative to that point)
    offset_time = events_tsv - elapsed_time_of_first_capture
        
    # Now we build the new stim file, adding the offset time to the original stim file
    stim_protocol_tsv['Onset'] = stim_protocol_tsv['Onset'] + offset_time
    
    # Write it out
    stim_protocol_tsv.to_csv(filenames[0], sep='\t', index=False)
    
    # Build a time axis
    elapsed_t = np.arange(0, number_of_captures * number_of_frames) * frame_time
    
    # Find stimuli
    stimuli = []
    for s in stim_protocol_tsv['trial_type']:
        if s not in stimuli:
            stimuli.append(s)
            
    # Build stim dictionary
    stim_dict = {}; 
    for i, s in enumerate(stimuli):
        stim_dict[s] = i
            
    # Create trigger array
    stim_onset = np.zeros((len(stimuli), len(elapsed_t)), dtype=float)
    stim_boxcar = np.zeros_like(stim_onset)
    
    # Find timepoints where triggers are active
    for j, s in enumerate(stimuli):
        
        # Indexes where we find the stimulus occurs
        idxs = np.where(stim_protocol_tsv['trial_type'] == s)[0]
        
        # In each index, we collect the time points
        for i in idxs:
            
            # Onset and duration
            onset = np.round(stim_protocol_tsv['Onset'][i] / frame_time, 0) * frame_time
            offset = np.round( (onset + stim_protocol_tsv['Duration'][i]) / frame_time, 0) * frame_time
            
            # Mask indexes that should be changed
            where_to_change = np.where(elapsed_t == onset)
            
            # Modify onset array
            stim_onset[j][where_to_change] = 1.0
            
            # Where to change for boxcar array
            where_to_change = np.nonzero( (elapsed_t >= onset) & (elapsed_t < offset) )
            
            # Modify boxcar array
            stim_boxcar[j][where_to_change] = 1.0
            
    # Save trigger dictionary
    np.savez_compressed(filenames[1], stim_dict=np.array(stim_dict), stim_onset = stim_onset, stim_boxcar = stim_boxcar)
    
    # Success
    return 0



# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    
    # Select a data directory
    target_dir = easygui.diropenbox(title="Choose directory containing trigger files")
    
    # Check
    if target_dir == None:
        raise Exception("Target directory not provided")
    
    # Move to data directory
    os.chdir(target_dir)
    
    # Run function
    process_triggers()