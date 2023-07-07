# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:34:32 2023

# Add 3D information from text file into SD file.

@author: Dell-User
"""

import os


###### Parameters ######
number_of_chips = 16
patt_per_frame = 1
output_dir = r'C:\Users\Dell-User\Desktop\tmp'
output_file = r'dynamic_packet_single_source.txt'

# Grab this directory
this_dir = os.getcwd()

# Jump to the platform directory for dynamic packet
os.chdir("../../platform");

# Import dynamic packet
import DynamicPacket

# Go back
os.chdir(this_dir)

raise Exception

# =============================================================================
# Create an emitter pattern
# =============================================================================
dynamic_packet = DynamicPacket.DynamicPacket(number_of_chips, patt_per_frame)

# These settings are maintained through all patterns
dynamic_packet.fill(field_dict={    'nir_vcsel_enable': '1', \
                                    'driver_dll_word': np.binary_repr(vcsel_setting, 5), \
                                    'clk_flip': np.binary_repr(clk_flip,1), \
                                    'aqc_dll_coarse_word': np.binary_repr(coarse, 4), \
                                    'aqc_dll_fine_word': np.binary_repr(fine, 3), \
                                    'aqc_dll_finest_word': np.binary_repr(finest, 1), \
                                    })
    
# Sweep emitter
for p in range(patt_per_frame):
    dynamic_packet.fill(pattern_list=[0], chip_list=[0], field_dict={'vcsel_enable': '1'})

# Show results
p_to_show = 0
dynamic_packet.show(pattern_list=(p_to_show,))