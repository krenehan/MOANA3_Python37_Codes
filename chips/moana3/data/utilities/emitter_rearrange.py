# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 12:06:20 2022

@author: bmc06
"""
import numpy as np
import os
from interpret_yield import interpret_yield
import shutil

def emitter_rearrange():
    
    # File list   
    f_l_full = os.listdir()
    
    # Remove directories that do not contain emitter string (result directories)
    f_l = []
    for f in f_l_full:
        if 'emitter' in f:
            f_l.append(f)
    
    # Get the first part of the file 
    first_part = [ f_l[i].split('emitter')[0] for i in range(len(f_l)) ]
    
    # Remove the dates at the end of the file 
    second_part_with_dates = [ f_l[i].split('emitter')[1].split('_') for i in range(len(f_l)) ]
    for i in range(len(f_l)):
        del second_part_with_dates[i][0]
        del second_part_with_dates[i][-2:]
    
    # Get the second part of the file 
    second_part = [ '_'.join(second_part_with_dates[i]) for i in range(len(second_part_with_dates)) ]
    
    # Get the emitter 
    # emitter = [ f_l[i].split('emitter')[1].split('_')[0] for i in range(len(f_l)) ]
    
    # Build list of first part and second part
    unique_names_tmp = list(set( [ (first_part[i], second_part[i]) for i in range(len(f_l))] ))
    
    # Check that result directory does not exist in f_l_full
    # If result directory exists, remove relevant string from unique_names list
    unique_names = []
    for i in range(len(unique_names_tmp)):
        s = unique_names_tmp[i][0] + unique_names_tmp[i][1]
        if s not in f_l_full:
            unique_names.append(unique_names_tmp[i])
    
    # Number of operations
    number_of_operations = len(unique_names)
    
    # Begin operations
    for op in range(number_of_operations):
        
        # Get first part and second part
        fp, sp = unique_names[op]
        
        # Get the shape of the captures file
        for f in f_l:
            if (fp in f) and (sp in f):
                number_of_captures, number_of_detectors, number_of_frames, patterns_per_frame, number_of_bins = np.shape(np.load(f + '\\captures.npz')['data'])
                number_of_sources = number_of_detectors
                break
        
        # Create final array
        final = np.zeros((number_of_sources, number_of_detectors, number_of_captures, number_of_frames, number_of_bins), dtype=float)
                
        # Create directory
        experiment_directory = unique_names[op][0] + unique_names[op][1]
        os.mkdir(experiment_directory)
        
       # Fill in the final array 
        print("Filling output array")
        for s in range(number_of_sources):
            
            # Find appropriate directory
            for f in f_l:
                if (fp in f) and (sp in f) and ('emitter' + str(s) + '_' in f):
                    source_directory_name = f
                    break
                
            # Load directory
            arr = np.load(source_directory_name + '\\captures.npz')['data']
            
            # Load data for source file [capture][detector][frame][pattern][bin]
            # arr = np.load(fp + 'emitter' + str(s) + '_' + sp + '\\captures.npz')['data']
            
            # Transpose [source][detector][capture][frame][bin]
            arr_t = np.transpose(arr, axes=(3,1,0,2,4))
            
            # Fill
            final[s] = arr_t[0]
                        
        # Transpose final array back to [capture][detector][frame][pattern][bin]
        final = np.transpose(final, (2,1,3,0,4))

        # Compress data structure
        print("Saving emitter_rearragned file")
        np.savez_compressed(experiment_directory + '\\captures.npz', data=final)      
        
        # Copy yield file
        shutil.copy2(source_directory_name + '\\yield.txt', experiment_directory)
        
        # Copy test setup file
        shutil.copy2(source_directory_name + '\\test_setup.txt', experiment_directory)
        
        # Copy ir_emitters file
        shutil.copy2(source_directory_name + '\\ir_emitters.npy', experiment_directory)
        
        # Create emitter pattern file
        number_of_patterns = number_of_sources
        ep = np.zeros((number_of_patterns, number_of_sources), dtype=bool)
        for p in range(number_of_patterns):
            for s in range(number_of_sources):
                if p == s:
                    ep[p][s] = True
        np.save(experiment_directory + '\\emitter_pattern.npy', ep, fix_imports=False)
        
        # Remove handled directories
        
            
        