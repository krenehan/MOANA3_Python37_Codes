# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 13:56:25 2023

@author: Dell-User
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, lfilter_zi
import os
from pathlib import Path


def PHOEBE():
 #%%   
    def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a
        
    def butter_bandpass_filter_zi(data, lowcut, highcut, fs, order=5):
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        zi = lfilter_zi(b, a)
        y,zo = lfilter(b, a, data, zi=zi*data[0])
        return y
    
    
    # Load data - check for reconstruction files first
    fl = os.listdir()
    
    # If data has already been processed, we just use the reconstruction file
    if 'reconstruction_data.npz' in fl:
        exp_t = np.load("reconstruction_data.npz")['exp_t']
        cw_data = np.load("reconstruction_data.npz")['cw_data']
    else:
        raise Exception("reconstruction_data.npz not found")
        
    
    # Shape
    number_of_sources, number_of_wavelengths, number_of_detectors, number_of_captures = np.shape(cw_data)
    
    # Derived shape of colormap
    number_of_rows = int(np.sqrt(number_of_detectors))
    number_of_cols = int(np.sqrt(number_of_detectors))
    
    # Calculate the fps of the data
    fps = 1/(exp_t[1]-exp_t[0])
    
    # Remove DC component of data
    cw_data_filt = np.empty_like(cw_data)
    
    # Bandpass filter the data
    filter_cutoff = np.array([0.5, min(2.49, fps/2-0.01)])
    for s in range(number_of_sources):
        for w in range(number_of_wavelengths):
            for d in range(number_of_detectors):
                cw_data_filt[s][w][d] = butter_bandpass_filter_zi(cw_data[s][w][d], filter_cutoff[0], filter_cutoff[1], fps, order=3)
    
    # Normalize to standard deviation
    cw_data_norm = np.zeros_like(cw_data_filt)
    for s in range(number_of_sources):
        for w in range(number_of_wavelengths):
            for d in range(number_of_detectors):
                if np.std(cw_data_filt[s][w][d]) > 0:
                    cw_data_norm[s][w][d] = cw_data_filt[s][w][d] / np.std(cw_data_filt[s][w][d])
    
    # Split into two wavelengths
    cw_data_norm_tmp = np.transpose(cw_data_norm, axes=(1, 0, 2, 3))
    nir_data = cw_data_norm_tmp[0]
    ir_data = cw_data_norm_tmp[1]
    
    
    # Compute zero lag cross-correlation between two wavelengths
    sci = np.zeros(np.shape(ir_data)[0:2])
    for s in range(number_of_sources):
        for d in range(number_of_detectors):
            sci[s][d] = np.corrcoef(nir_data[s][d], ir_data[s][d])[0][1]
    
    # Rigid or flex 4x4
    rigid = False
    flex = ~rigid
    face_up = False
    face_down = ~face_up
    rot90_ccw = -1
    
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
        
    # Create results directory
    subdirectory_path = os.path.join(os.getcwd(), "phoebe_plots")
    Path( subdirectory_path ).mkdir( parents=True, exist_ok=True )
        
    # Turn off interactive plotting
    # plt.ioff()
    
    # Create plots
    for s in range(number_of_sources):
        
        # Get data for this plot
        data_for_this_plot = sci[s]
        
        # Check data
        if np.all(np.isnan(data_for_this_plot)):
            continue
        
        # Create figure
        plt.figure()
        
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
            sci_rshp[d] = data_for_this_plot[detector_number]
            
        # Reshape to 4x4
        sci_rshp = np.reshape(sci_rshp, newshape=(number_of_rows, number_of_cols))
        
        # Create colormap - the flip here makes it such that the image matches the printed array
        plt.pcolormesh(np.flip(sci_rshp, axis=0), vmin=-1, vmax=1, cmap='RdYlGn')
        plt.colorbar()
        plt.title("Scalp Coupling Index for IC" + str(s+1))
       
        # Hide x and y axes
        plt.gca().axes.xaxis.set_ticks([])
        plt.gca().axes.yaxis.set_ticks([])
        
        # Add chip names
        for r in range(number_of_rows):
            for c in range(number_of_cols):
                
                # Get the position
                y_pos = (number_of_rows - r) - 0.5
                x_pos = c + 0.5
                
                # Get the chip number
                chip_number = position[r][c]
                
                # Color of text
                color = 'purple' if (chip_number==s) else 'black'
                
                # Add text labels
                plt.text(x_pos, y_pos, 'IC' + str(chip_number+1) + '\n' + str(round(sci_rshp[r][c], 2)), horizontalalignment='center', verticalalignment='center', color=color)

        # Save
        filename = "s" + str(s) + ".png"
        plt.savefig(os.path.join(subdirectory_path, filename), dpi=600)
        
        # Close
        # plt.close()
    
# For standalone runs
# Requires that zip_files has already been run in target directory
if __name__ in '__main__':
    
    import easygui
    import os
    
    # Select a data directory
    target_dir = easygui.diropenbox(title="Choose reconstruction outputs directory")
    
    # Check
    if target_dir == None:
        raise Exception("Target directory not provided")
    
    # Move to data directory
    os.chdir(target_dir)
    
    # Run function
    PHOEBE()
    






