# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@purpose:   Batch data analysis. Will perform specified functions on all subdirectories of a top level directory. 
            Top level directory must contain a subdirectory called data, which contains its own subdirectories corresponding to
            individual runs of an experiment. 

@usage:     Standalone.

@prereqs:   None.

@author:    Kevin Renehan

"""

import numpy as np
import os
import easygui
from zip_files import zip_files
from average import average
from prepare_for_reconstruction import prepare_for_reconstruction
from prepare_hbo2_for_reconstruction import prepare_hbo2_for_reconstruction
from prepare_all_captures_for_reconstruction import prepare_all_captures_for_reconstruction
from patch_geometry import patch_geometry
from py2nirs import py2nirs



# Options
do_average = False
do_prepare_for_reconstruction = False
do_prepare_hbo2_for_reconstruction = True
do_prepare_all_captures_for_reconstruction = False
do_patch_geometry = False
do_py2nirs = False

# Capture window and breath hold window for reconstruction
capture_window = None
breath_hold_window = None #(600, 900)

# SD structure for NIRS generation
sd_filepath = r'C:\Users\Dell-User\Dropbox\MOANA\Homer3\new_moana3_probe\MOANA3_RIGIDFLEX_4BY4_SOMATOSENSORY_3D.SD'





# Function to interpret results
def get_result(int_code):
    if int_code == 0:
        return 'success'
    elif int_code == -1:
        return 'error'
    elif int_code == 1:
        return 'already done'

# Dictionary of results
results_dict = {}

# Get the utilities directory
util_dir = os.getcwd()

# Get the target directory
target_dir = easygui.diropenbox()

# Check 
if target_dir == None:
    raise Exception("Target directory not provided")

# Change working directory
os.chdir(target_dir)

# Print status
print("Beginning target of " + target_dir)

# Target directory operations
if do_patch_geometry:
    patch_result_dict = {}
    print("Starting patch geometry")
    if 'source_detector_positions' not in os.listdir():
        os.mkdir('source_detector_positions')
    os.chdir('source_detector_positions')
    patch_result_dict['patch_geometry'] = get_result(patch_geometry())
    results_dict[os.path.basename(target_dir)] = patch_result_dict
    os.chdir(target_dir)
    
# Check for a data directory
if 'data' not in os.listdir():
    raise Exception("data directory not found in target directory")
    
# Descend into data directory
data_dir = os.path.join(target_dir, 'data')
os.chdir(data_dir)

# Get a list of the subdirectories
subdirectory_list = []
l = os.listdir()
for sd in l:
    if os.path.isdir(sd):
        subdirectory_list.append(sd)
    else:
        print(sd + " is not a directory and will not be considered")

# Descend into each subdirectory and perform the operations
print("Starting subdirectory operations")
for sd in subdirectory_list:
    
    # SD results directory
    sd_results_dict = {}
    
    # Descend
    os.chdir(os.path.join(data_dir, sd))

    # Must zip
    zip_file_result = zip_files()
    sd_results_dict['zip_files'] = get_result(zip_file_result)
    
    # Skip if zip did not work
    if zip_file_result >= 0:
    
        # Optional operations
        if do_average:
            print("Running average")
            sd_results_dict['average'] = get_result(average())
        if do_prepare_for_reconstruction:
            print("Running prepare for reconstruction")
            prepare_for_reconstruction(capture_window = capture_window) # None or capture_window
        if do_prepare_hbo2_for_reconstruction:
            print("Running prepare for HbO2 reconstruction")
            sd_results_dict['prepare_hbo2_for_reconstruction'] = get_result(prepare_hbo2_for_reconstruction(capture_window = capture_window))
        if do_prepare_all_captures_for_reconstruction:
            print("Running prepare all captures for reconstruction")
            sd_results_dict['prepare_all_captures_for_reconstruction'] = get_result(prepare_all_captures_for_reconstruction(capture_window = capture_window))
        if do_py2nirs:
            print("Running py2nirs")
            sd_results_dict['py2nirs'] = get_result(py2nirs(sd_filepath, capture_window = capture_window))
            
    # Add to top level results directory
    results_dict[sd] = sd_results_dict
    
# Show overall results
print("")
print("")
print("")
print("")
for sd in results_dict:
    print('--------------------------------------------------------------------')
    print("Results for " + sd)
    for task in results_dict[sd]:
        print("    " + task + ": " + results_dict[sd][task])
    print('--------------------------------------------------------------------')
    print("")
    
    
    
    
    
    
    
    
    
    
