# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:57:42 2022

@author: bmc06
"""

import numpy as np
import matplotlib.pyplot as plt

# Load captures file and average
c = np.load('C:\\Users\\bmc06\\Desktop\\Phantom Recon - Initial Solutions\\test_run\\data\\thickness6mm_size3mm_locationc5_setting3_bias0p4V\\captures.npz')['data']
ca = np.mean(c, axis=(0,2))

# Load averaged file for comparison
a = np.load('C:\\Users\\bmc06\\Desktop\\Phantom Recon - Initial Solutions\\test_run\\data\\thickness6mm_size3mm_locationc5_setting3_bias0p4V\\averaged.npz')['data']
a = np.reshape(a, (16, 16, 150))

# Load reconstruction_data for comparison
rd = np.load('C:\\Users\\bmc06\\Desktop\\Phantom Recon - Initial Solutions\\test_run\\data\\thickness6mm_size3mm_locationc5_setting3_bias0p4V\\reconstruction_data.npz')['data']

# Plot
plt.close('all')
s = 8
for d in range(16):
    plt.figure() 
    plt.plot(ca[s][d], label='ca')
    # plt.plot(a[8][15], label='a')
    plt.plot(rd[d][s], label='rd')
    plt.legend();