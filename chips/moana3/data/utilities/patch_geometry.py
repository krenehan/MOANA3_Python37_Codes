# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 16:19:29 2022

@author: Dell-User
"""

#%% Setup code

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.io import savemat

def patch_geometry():
    
    # Specify source rows and source columns
    rows = 4
    cols = 4
    
    # Position arrays
    src_pos_x = np.zeros( (rows * cols,), dtype=float)
    src_pos_y = np.zeros( (rows * cols,), dtype=float)
    det_pos_x = np.zeros( (rows * cols,), dtype=float)
    det_pos_y = np.zeros( (rows * cols,), dtype=float)
    
    # Source and detector pitch
    pitch = 8
    
    # Offset
    det_offset_x = 0.2975
    det_offset_y =  -0.6525
    
    # Array is centered in scene
    scene_extent_x = (-42//2, 42//2)
    scene_extent_y = (-42//2, 42//2)
    
    # Margin
    x_margin = ((scene_extent_x[1] - scene_extent_x[0]) - (pitch * (cols-1))) / 2
    y_margin = ((scene_extent_y[1] - scene_extent_y[0]) - (pitch * (rows-1))) / 2
    
    # Calculate source detector locations
    print("Calculating source/detector coordinates")
    flat_idx = 0
    for r in range(rows):
        
        # y position for row
        y = scene_extent_y[1] - y_margin - r * pitch
        
        for c in range(cols):
            
            # x position for col
            x = scene_extent_x[1] - x_margin - c * pitch
        
            # Source position
            src_pos_x[flat_idx] = x
            src_pos_y[flat_idx] = y
            
            # Detector position
            det_pos_x[flat_idx] = x + det_offset_x
            det_pos_y[flat_idx] = y + det_offset_y
            
            # Increment flat index
            flat_idx += 1 
            
    # Plot for verification
    print("Plotting source/detector positions")
    plt.scatter(src_pos_x, src_pos_y)
    plt.scatter(det_pos_x, det_pos_y)
    plt.xlim(scene_extent_x)
    plt.ylim(scene_extent_y)
    plt.show()
    
    # Save the mat file
    print("Saving .mat file")
    mdict = {'src_pos_x': src_pos_x, 'src_pos_y': src_pos_y, 'det_pos_x': det_pos_x, 'det_pos_y': det_pos_y}
    savemat("src_det_positions.mat", mdict)
    
    # Create README
    print("Creating README")
    st = \
'''######################### KEYS #########################
src_pos_x   - x-coordinates of source positions in mm.
src_pos_y   - y-coordinates of source positions in mm.
det_pos_x   - x-coordinates of detector positions in mm.
det_pos_y   - y-coordinates of detector positions in mm.

Note that all source and detector positions assume origin in the exact center of the phantom.

############################################ Source/Detector Mapping ############################################
 ____________________
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

'''
    
    f = open('src_det_positions_mat_README.txt', 'w')
    f.write(st)
    f.close()
    
    ###### PYTHON ######
    # Save the npz file
            
    print("Saving .npz file")
    np.savez_compressed ( \
                        "src_det_positions", \
                        src_pos_x = src_pos_x, \
                        src_pos_y = src_pos_y, \
                        det_pos_x = det_pos_x, \
                        det_pos_y = det_pos_y )
    
    # Create README
    print("Creating python README")
    st = \
'''######################### KEYS #########################
src_pos_x   - x-coordinates of source positions in mm.
src_pos_y   - y-coordinates of source positions in mm.
det_pos_x   - x-coordinates of detector positions in mm.
det_pos_y   - y-coordinates of detector positions in mm.

Note that all source and detector positions assume origin in the exact center of the phantom.

############################################ Source/Detector Mapping ############################################
 ____________________
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

'''
    
    f = open('src_det_positions_npz_README.txt', 'w')
    f.write(st)
    f.close()
    
    
    ##### TEXT FILE #####
    print("Creating source/detector position text file")
    st = \
'''Note that all source and detector positions assume origin in the exact center of the phantom.

############################################ Source/Detector Mapping ############################################
 ____________________
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

################################################### Positions ###################################################
'''

    for i in range(len(src_pos_x)):
        st = st + "Source {}: ({}, {})\n".format(i, src_pos_x[i], src_pos_y[i])
    for i in range(len(det_pos_x)):
        st = st + "Detector {}: ({}, {})\n".format(i, det_pos_x[i], det_pos_y[i])
        
    f = open('src_det_positions.txt', 'w')
    f.write(st)
    f.close()
    
    
    
