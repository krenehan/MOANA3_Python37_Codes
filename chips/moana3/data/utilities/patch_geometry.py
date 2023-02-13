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
# if True:
    
    # Specify source rows and source columns
    rows = 4
    cols = 4
    
    # Position arrays
    nir_src_pos_x = np.zeros( (rows * cols,), dtype=float)
    nir_src_pos_y = np.zeros( (rows * cols,), dtype=float)
    ir_src_pos_x = np.zeros( (rows * cols,), dtype=float)
    ir_src_pos_y = np.zeros( (rows * cols,), dtype=float)
    det_pos_x = np.zeros( (rows * cols,), dtype=float)
    det_pos_y = np.zeros( (rows * cols,), dtype=float)
    
    # Source and detector pitch
    pitch = 8
    
    # Offset
    src_offset_x = 0.2975
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
            
            # Detector position
            det_pos_x[flat_idx] = x
            det_pos_y[flat_idx] = y + det_offset_y
        
            # Source position
            nir_src_pos_x[flat_idx] = x - src_offset_x
            nir_src_pos_y[flat_idx] = y
            
            # Source position
            ir_src_pos_x[flat_idx] = x + src_offset_x
            ir_src_pos_y[flat_idx] = y
            
            # Increment flat index
            flat_idx += 1 
            
    # Plot for verification
    print("Plotting source/detector positions")
    plt.scatter(nir_src_pos_x, nir_src_pos_y, color='red', label="NIR", s=10)
    plt.scatter(ir_src_pos_x, nir_src_pos_y, color='purple', label="IR", s=10)
    plt.scatter(det_pos_x, det_pos_y, color='green', label="Det", s=10)
    plt.xlim(scene_extent_x)
    plt.ylim(scene_extent_y)
    plt.xlabel("x-position (mm)")
    plt.ylabel("y-position (mm)")
    plt.axvline(x = 0, color='blue', linestyle='--')
    plt.axhline(y=0, color='blue', linestyle='--')
    plt.style.use('dark_background')
    plt.legend()
    plt.savefig("src_det_positions.png", transparent=True)
    plt.show()
    
    # Save the mat file
    print("Saving .mat file")
    mdict = {'nir_src_pos_x': nir_src_pos_x, 'nir_src_pos_y': nir_src_pos_y, 'ir_src_pos_x': ir_src_pos_x, 'ir_src_pos_y': ir_src_pos_y, 'det_pos_x': det_pos_x, 'det_pos_y': det_pos_y}
    savemat("src_det_positions.mat", mdict)
    
    # Create README
    print("Creating README")
    st = \
'''######################### KEYS #########################
nir_src_pos_x  - x-coordinates of NIR source positions in mm.
nir_src_pos_y  - y-coordinates of NIR source positions in mm.
ir_src_pos_x   - x-coordinates of IR source positions in mm.
ir_src_pos_y   - y-coordinates of IR source positions in mm.
det_pos_x      - x-coordinates of detector positions in mm.
det_pos_y      - y-coordinates of detector positions in mm.

Note that all source and detector positions assume origin in the exact center of the array.

############################################ Source/Detector Mapping ############################################
 ___________________
|    |    |    |    |
|  4 |  3 |  2 |  1 |
|____|____|____|____|
|    |    |    |    |
|  8 |  7 |  6 |  5 |
|____|____|____|____|
|    |    |    |    |
| 12 | 11 | 10 | 9  |
|____|____|____|____|
|    |    |    |    |
| 16 | 15 | 14 | 13 |
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
                        nir_src_pos_x = nir_src_pos_x, \
                        nir_src_pos_y = nir_src_pos_y, \
                        ir_src_pos_x = ir_src_pos_x, \
                        ir_src_pos_y = ir_src_pos_y, \
                        det_pos_x = det_pos_x, \
                        det_pos_y = det_pos_y )
    
    # Create README
    print("Creating python README")
    st = \
'''######################### KEYS #########################
nir_src_pos_x  - x-coordinates of NIR source positions in mm.
nir_src_pos_y  - y-coordinates of NIR source positions in mm.
ir_src_pos_x   - x-coordinates of IR source positions in mm.
ir_src_pos_y   - y-coordinates of IR source positions in mm.
det_pos_x      - x-coordinates of detector positions in mm.
det_pos_y      - y-coordinates of detector positions in mm.

Note that all source and detector positions assume origin in the exact center of the array.

############################################ Source/Detector Mapping ############################################
 ___________________
|    |    |    |    |
|  3 |  2 |  1 |  0 |
|____|____|____|____|
|    |    |    |    |
|  7 |  6 |  5 |  4 |
|____|____|____|____|
|    |    |    |    |
| 11 | 10 | 9  | 8  |
|____|____|____|____|
|    |    |    |    |
| 15 | 14 | 13 | 12 |
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
 ___________________
|    |    |    |    |
|  3 |  2 |  1 |  0 |
|____|____|____|____|
|    |    |    |    |
|  7 |  6 |  5 |  4 |
|____|____|____|____|
|    |    |    |    |
| 11 | 10 | 9  | 8  |
|____|____|____|____|
|    |    |    |    |
| 15 | 14 | 13 | 12 |
|____|____|____|____|

################################################### Positions ###################################################
'''

    for i in range(len(nir_src_pos_x)):
        st = st + "NIR Source {}: ({}, {})\n".format(i, nir_src_pos_x[i], nir_src_pos_y[i])
    for i in range(len(ir_src_pos_x)):
        st = st + "IR Source {}: ({}, {})\n".format(i, ir_src_pos_x[i], ir_src_pos_y[i])
    for i in range(len(det_pos_x)):
        st = st + "Detector {}: ({}, {})\n".format(i, det_pos_x[i], det_pos_y[i])
        
    f = open('src_det_positions.txt', 'w')
    f.write(st)
    f.close()
    
    
    
