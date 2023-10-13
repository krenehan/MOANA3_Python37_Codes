# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 07:38:59 2023

@author: Dell-User
"""

import pandas as pd
import numpy as np
import os


def translate_variable_psychopy_csv(filepath):
    
    # Load csv file
    csv_file = pd.read_csv(filepath)
    
    
    # Some information
    first_event = 'rest_circle'
    events = ['rest_circle', 'stim_text']
    event_output_names = {'rest_circle': 'rest', 'stim_text': 'stim'}
    
    # Find keys to consider
    keys_to_consider = {}
    for e in events:
        l = []
        for k in csv_file.keys():
            if e in k:
                l.append(k)
            if len(l):
                keys_to_consider[e] = l
           
                
    # Grab the columns
    data_dict = {}
    for k in keys_to_consider:
        
        # Grab the list for this key
        l = keys_to_consider[k]
        
        # Translate to a list of arrays
        data_dict[k] = [np.array(csv_file[l[i]]) for i in range(len(l))]
        
        # Remove nans
        for i in range(len(data_dict[k])):
            data_dict[k][i] = data_dict[k][i][np.where(~np.isnan(data_dict[k][i]))]
        
    
    # Get the start index for the first key
    start_idx = np.where(np.array(['started' in keys_to_consider[first_event][i] for i in range(len(keys_to_consider[first_event]))]))[0][0]
    start_time = data_dict[first_event][start_idx][0]
    
    
    # Offset arrays to start at 0 time
    for k in data_dict:
        for i in range(len(data_dict[k])):
            data_dict[k][i] = data_dict[k][i] - start_time
            
        
    # Get duration and onset
    duration_dict = {}
    onset_dict = {}
    for k in data_dict:
        
        # Find start index and stop index for this key
        start_idx = np.where(np.array(['started' in keys_to_consider[k][i] for i in range(len(keys_to_consider[k]))]))[0][0]
        stop_idx = np.where(np.array(['stopped' in keys_to_consider[k][i] for i in range(len(keys_to_consider[k]))]))[0][0]
        
        # The onset is what we already have in the start vector
        onset_dict[k] = data_dict[k][start_idx]
        
        # Duration is just the difference between stop and start
        duration_dict[k] = data_dict[k][stop_idx] - data_dict[k][start_idx]
        
        
    # Get filename
    base_file_path = os.path.split(filepath)[0]
    filename = os.path.splitext(os.path.split(filepath)[1])[0] + ".tsv"
    
    # Filestring to build
    fs = ['Onset', '\t', 'Duration', '\t', 'Amplitude', '\t', 'trial_type', '\n']
    
    # Vertical stack the vectors
    vs = np.vstack([onset_dict[k] for k in onset_dict])
    
    # Find starting point
    for i in range(len(vs.flat)):
        
        # Find minimum index
        next_idx = np.argmin(vs.flat)
        
        # Unravel the index
        mapped_idx = np.unravel_index(next_idx, np.shape(vs))
        
        # Get the key for this idx
        this_key = list(onset_dict.keys())[mapped_idx[0]]
        
        # Add to filestring
        fs.append(str(round(vs[mapped_idx], 2)))
        fs.append('\t')
        fs.append(str(round(duration_dict[this_key][mapped_idx[1]], 2)))
        fs.append('\t')
        fs.append("1")
        fs.append('\t')
        fs.append(event_output_names[this_key])
        fs.append('\n')
        
        # Set the index in vs to huge value
        vs.flat[next_idx] = 500000
        
    # Join the string and write out
    fs = "".join(fs)
    fh = open(os.path.join(base_file_path, filename), "w")
    fh.write(fs)
    fh.close()

# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    
    # Select a file
    target_file = easygui.fileopenbox(title="Choose psychopy csv file")
    
    # Check
    if target_file == None:
        raise Exception("Target file not provided")
    
    # Run function
    translate_variable_psychopy_csv(target_file)










