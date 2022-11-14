# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User

Run zip.py before accumulating
"""

import numpy as np
import os
import matplotlib.pyplot as plt

def accumulate(save_figures=True):

    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for zipped captures file")
    found = False
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if 'captures.npz' in filelist[f]:
            print("Found zipped captures file")
            found = True
            
    if not found:
        
        raise Exception("Zipped captures file not found")
        
    else:
        
        # Load
        print("Loading captures file")
        arr = np.load('captures.npz')['data']
        
        # Get shape
        number_of_captures, number_of_chips, number_of_frames, patterns_per_frame, number_of_bins = np.shape(arr)
        
        # Accumulate
        print("Accumulating captures")
        acc = np.sum(arr, axis=0)
            
        # Save accumulated results
        print("Saving accumulated file")
        np.savez_compressed('accumulated.npz', data=acc)
    
    
        # Create plot structure
        if save_figures:
            print("Creating plot")
            plot_axes = [None]*number_of_chips
            plot_figure, axes_structure = plt.subplots(4, 4, sharex=True, sharey=False)
            # plot_figure.suptitle("Accumulated Data")
            plot_figure.set_size_inches(24, 20)
            for chip in range(number_of_chips):
                
                # Fill plot_axes structure
                plot_axes[chip] = axes_structure.flat[chip]
                
                # Subplot title
                plot_axes[chip].set_title('Chip ' + str(chip+1))
                
                # Subplot axis labels
                if (chip==0) or (chip==4) or (chip==8) or (chip==12):
                    plot_axes[chip].set(ylabel='Counts')
                if (chip>=12):
                    plot_axes[chip].set(xlabel="Bin Number")
                
                # Show units only on outer plots
                # plot_axes[chip].label_outer()
                
                # Set x-axis range
                plot_axes[chip].set_xlim((0, 150))
                
                # Plot
                plot_axes[chip].plot(range(150), acc[chip][0][0])
                # plot_axes[chip].semilogy(range(150), acc_mean[chip][0][0])
                
                # # Set y-axis range
                # plot_axes[chip].set_ylim((1, 10000))
                
            print("Saving plot figure")
            plot_figure.savefig("accumulated_figure.png", dpi=400)
        
        print("Done")