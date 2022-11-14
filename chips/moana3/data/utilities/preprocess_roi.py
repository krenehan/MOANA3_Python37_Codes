# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User
"""

import numpy as np
import os
import easygui
from roi_raw_histograms import roi_raw_histograms
from roi_contrast import roi_contrast
from roi_contrast_to_noise import roi_contrast_to_noise
from roi_difference_matrix import roi_difference_matrix

# Options
do_raw_histogram = False
do_contrast = False
do_contrast_to_noise = True
do_roi_difference_matrix = False

# Background and ROI tags in directory names
data_dir_prefix = 'nir_'
bkg_key = 'bkg'
roi_key = 'roi'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

# Capture window for reconstruction
capture_window = (500,563)

# Get the utilities directory
util_dir = os.getcwd()

# Get the target directory
target_dir = easygui.diropenbox()

# Change working directory
os.chdir(target_dir)
    
# Check for a data directory
if data_dir_prefix + 'data' not in os.listdir():
    raise Exception("data directory not found in target directory")
    
# Descend into data directory
data_dir = os.path.join(target_dir, data_dir_prefix + 'data')
os.chdir(data_dir)

# Optional operations
if do_roi_difference_matrix:
    roi_difference_matrix(bkg_key, roi_key, capture_window=capture_window, data_dir_prefix=data_dir_prefix)
if do_raw_histogram:
    roi_raw_histograms(bkg_key, roi_key, capture_window=capture_window, data_dir_prefix=data_dir_prefix)
if do_contrast:
    roi_contrast(bkg_key, roi_key, capture_window=capture_window, data_dir_prefix=data_dir_prefix)
if do_contrast_to_noise:
    roi_contrast_to_noise(bkg_key, roi_key, capture_window=capture_window, data_dir_prefix=data_dir_prefix)
    
    
print("Done")