# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User
"""

import numpy as np
import os
import easygui
from zip_files import zip_files
from average import average
from average_mat import average_mat
from prepare_for_reconstruction import prepare_for_reconstruction
from prepare_hbo2_for_reconstruction import prepare_hbo2_for_reconstruction
from patch_geometry import patch_geometry

# Options
do_average = False
do_average_mat = False
do_prepare_for_reconstruction = False
do_prepare_hbo2_for_reconstruction = False
do_patch_geometry = True                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

# Capture window for reconstruction
capture_window = None

# Get the utilities directory
util_dir = os.getcwd()

# Get the target directory
target_dir = easygui.diropenbox()

# Change working directory
os.chdir(target_dir)

# Target directory operations
if do_patch_geometry:
    if 'source_detector_positions' not in os.listdir():
        os.mkdir('source_detector_positions')
    os.chdir('source_detector_positions')
    patch_geometry()
    os.chdir(target_dir)
    
# Check for a data directory
if 'data' not in os.listdir():
    raise Exception("data directory not found in target directory")
    
# Descend into data directory
data_dir = os.path.join(target_dir, 'data')
os.chdir(data_dir)

# Get a list of the subdirectories
subdirectory_list = os.listdir()

# Descend into each subdirectory and perform the operations
for sd in subdirectory_list:
    
    # Descend
    os.chdir(os.path.join(data_dir, sd))

    # Must zip
    zip_files()
    
    # Optional operations
    if do_average:
        average()
    if do_average_mat:
        average_mat()
    if do_prepare_for_reconstruction:
        prepare_for_reconstruction(capture_window = capture_window) # None or capture_window
    if do_prepare_hbo2_for_reconstruction:
        prepare_hbo2_for_reconstruction(capture_window = capture_window)
    
print("Done")