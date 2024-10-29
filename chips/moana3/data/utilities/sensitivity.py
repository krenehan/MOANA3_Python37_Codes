# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 11:01:23 2022

@author: bmc06
"""

#%% Load the file 

import numpy as np


def sensitivity(sensitivity_matrix_file, superficial_thickness, sds_list, ua = 0.019):
    
    # Number of layers and moments
    number_of_moments = 3
    number_of_layers = 2
    
    # Result array
    result = np.zeros((len(sds_list), number_of_layers, number_of_moments))
    
    # Get data
    ua_arr = sensitivity_matrix_file['ua']
    z_arr = sensitivity_matrix_file['z']
    sds_arr = sensitivity_matrix_file['sds']
    S = sensitivity_matrix_file['S']
    
    # Sum sensitivities 
    superficial = np.sum(np.transpose(S, axes=(2,0,1,3))[np.where(z_arr<superficial_thickness)], axis=0)
    brain = np.sum(np.transpose(S, axes=(2,0,1,3))[np.where(z_arr>=superficial_thickness)], axis=0)
    
    # Select relevant ua
    superficial = np.transpose(superficial, axes=(1,0,2))[np.where(np.isclose(ua_arr, ua))][0]
    brain = np.transpose(brain, axes=(1,0,2))[np.where(np.isclose(ua_arr, ua))][0]
    
    # For each source/detector separation in the list, interpolate to find the sensitivity
    for sds_idx, sds in enumerate(sds_list):
        
        # Find sensitivities
        superficial_sensitivity = np.array([np.interp(sds, sds_arr, superficial[i]) for i in range(len(superficial))])
        brain_sensitivity = np.array([np.interp(sds, sds_arr, brain[i]) for i in range(len(brain))])
        print(superficial_sensitivity)
        
        # Fill
        result[sds_idx][0] = superficial_sensitivity.copy()
        result[sds_idx][1] = brain_sensitivity.copy()
        
    # Reshape
    result = np.transpose(result, axes=(2,0,1))
    result = np.reshape(result, newshape=(number_of_moments*len(sds_list), number_of_layers))
    
    # Return
    return result
    
    

# Standalone operation
if __name__ in '__main__':
    
    # Sensitivity matrix
    sensitivity_matrix_file = np.load('sensitivity_matrix.npz')
    
    # Thickness of superficial layer in mm
    superficial_thickness = 13
    
    # ua value to use
    ua = 0.019
    
    # List of source detector separations
    sds_list = [8.0, 9.0]
    
    # Call function
    S = sensitivity(sensitivity_matrix_file, superficial_thickness, sds_list, ua=ua)
