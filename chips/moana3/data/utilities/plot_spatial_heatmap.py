# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 16:39:01 2023

@author: Dell-User
"""

import numpy as np

def plot_spatial_heatmap(data, plt_obj, rigid=True, face_up=False, rot90_ccw=0, source_number=-1, vmin=None, vmax=None):
    
    # Fixed settings
    number_of_detectors = 16
    number_of_rows, number_of_cols = 4, 4
    
    if not((vmin is None) or (vmax is None)):
        limits_set = True
    else:
        limits_set = False
    
    # Check data shape
    if np.shape(data) != (number_of_detectors,):
        raise Exception("Data must be a 16-element array")
        
    # Derived settings
    flex = ~rigid
    face_down = ~face_up
        
    # Position vector
    position = np.arange(16).reshape(4,4)
    
    # Flip the position vector so that IC1 appears in the upper right hand corner by default
    position = np.flip(position, axis=(1,))
    
    # Adjust position vector as needed
    if (rigid and face_up) or (flex and face_down):
        pass
    elif (rigid and face_down) or (flex and face_up):
        # Move IC1 to the upper left hand corner
        position = np.flip(position, axis=(1,))
        
    # Rotate as needed
    position = np.rot90(position, k=rot90_ccw)
    
    # Create plot data structure for reshaping
    sci_rshp = np.zeros((number_of_detectors))
    
    # Fill 
    for d in range(number_of_detectors):
        
        # Detector number that will fill this index in sci_rshp
        detector_number = np.where(position.flat == d)
        
        # Check that we found the detector number
        if np.shape(detector_number)[1] == 1:
            detector_number = detector_number[0][0]
        else:
            print("Found " + str(np.shape(detector_number)[1]) + " instances of detector " + str(d) + " in position vector")
            # return -1
        
        # Fill index in sci_rshp with the data for the correct detector number
        sci_rshp[d] = data[detector_number]
        
    # Reshape to 4x4
    sci_rshp = np.reshape(sci_rshp, newshape=(number_of_rows, number_of_cols))
    
    # Create figure
    plt_obj.figure()
    
    # Create colormap - the flip here makes it such that the image matches the printed array
    if limits_set:
        plt_obj.pcolormesh(np.flip(sci_rshp, axis=0),  cmap='RdYlGn', vmin=vmin, vmax=vmax,)
    else:
        plt_obj.pcolormesh(np.flip(sci_rshp, axis=0),  cmap='RdYlGn')#, vmin=-1, vmax=1,)
    plt_obj.colorbar()
   
    # Hide x and y axes
    plt_obj.gca().axes.xaxis.set_ticks([])
    plt_obj.gca().axes.yaxis.set_ticks([])
    
    # Add chip names
    for r in range(number_of_rows):
        for c in range(number_of_cols):
            
            # Get the position
            y_pos = (number_of_rows - r) - 0.5
            x_pos = c + 0.5
            
            # Get the chip number
            chip_number = position[r][c]
            
            # Color of text
            color = 'purple' if (chip_number==source_number) else 'black'
            
            # Add text labels
            plt_obj.text(x_pos, y_pos, 'IC' + str(chip_number+1) + '\n' + str(round(sci_rshp[r][c], 2)), horizontalalignment='center', verticalalignment='center', color=color)
