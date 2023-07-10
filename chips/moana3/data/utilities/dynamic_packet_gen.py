# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 09:26:58 2023

@author: Dell-User
"""

#%% Imports - Don't touch
import os
import numpy as np
import easygui

# Move to platform for imports
this_dir = os.getcwd()
os.chdir('../../platform')
import chip.DelayLine as DelayLine
import DynamicPacket

# Move back to original working directory
os.chdir(this_dir)


#%% Configure top level options - These can be adjusted by user

# Number of chips on the PCB
number_of_chips = 16

# Number of patterns in a frame
patterns_per_frame = 2

# Clock specifications
clock_period_ns = 20.0
duty_cycle = 0.5

# Base delay for configuring chip delay lines
common_delay = 19.0


#%% Initialize classes - Don't touch

# Dynamic Packet
dynamic_packet = DynamicPacket.DynamicPacket(number_of_chips, patterns_per_frame)

# Delay Line
delay_line = DelayLine.DelayLine()

# Specify clock for delay line
delay_line.specify_clock(clock_period_ns, duty_cycle)

# Get the settings from delay line
clk_flip, coarse, fine, finest, actual_delay_ns = delay_line.get_setting(common_delay)


#%% Configure common settings - Don't touch

# These settings are maintained through all patterns
dynamic_packet.fill(field_dict={    'vcsel_enable': '0', \
                                    'nir_vcsel_enable': '0', \
                                    'ir_vcsel_enable': '0', \
                                    'driver_dll_word': np.binary_repr(0, 5), \
                                    'clk_flip': np.binary_repr(clk_flip,1), \
                                    'aqc_dll_coarse_word': np.binary_repr(coarse, 4), \
                                    'aqc_dll_fine_word': np.binary_repr(fine, 3), \
                                    'aqc_dll_finest_word': np.binary_repr(finest, 1), \
                                    })

    
#%% Configure emitter sweep options - These can be adjusted by user

# Sweep emitter?
sweep_emitter = True

# How many wavelengths?
number_of_wavelengths = 2

# Which sources will be included in the sweep? (do this in order!) (np.nan can be placed in locations where you don't want any chip to turn on)
sources_to_sweep = [0]
sources_to_sweep = np.array(sources_to_sweep)

# Which wavelength is swept first? (if using single wavelength, this is the only one in the sweep)
first_wavelength = 'nir'

# VCSEL driver settings for each wavelength (only used if wavelength is used)
nir_vcsel_setting = 4
ir_vcsel_setting = 3


#%% Propagate emitter options to dynamic  - Don't touch

# Check first wavelength string
if (first_wavelength != 'nir') and (first_wavelength != 'ir'):
    raise Exception("First wavelength must be \'nir\' or \'ir\'")
    
if (np.any(sources_to_sweep >= number_of_chips)):
    raise Exception("Source numbers in sources_to_sweep exceed number_of_chips")

# Check
if len(sources_to_sweep) * number_of_wavelengths != patterns_per_frame:
    raise Exception("Sources to sweep times number of wavelengths must equal patterns per frame!")

    
# Sweep emitter for wavelengths
if sweep_emitter:
    
    # Go through each wavelength
    for w in range(number_of_wavelengths):
        
        # First wavelength
        if w == 0:
            nir_vcsel_enable = str(int(first_wavelength == 'nir'))
            ir_vcsel_enable = str(int(first_wavelength == 'ir'))              
        else:
            nir_vcsel_enable = str(int(first_wavelength != 'nir'))
            ir_vcsel_enable = str(int(first_wavelength != 'ir'))
            
        # Figure out the vcsel setting that should be used
        driver_dll_word = nir_vcsel_setting if bool(int(nir_vcsel_enable)) else ir_vcsel_setting
            
        # Base pattern number
        base_pattern_for_this_wavelength = w * len(sources_to_sweep)
            
        # Go through each source
        for i, s in enumerate(sources_to_sweep):
            
            # Pattern number
            p = base_pattern_for_this_wavelength + i
            
            # Fill all chips in the pattern with the correct VCSEL driver setting
            dynamic_packet.fill(pattern_list=[p], field_dict={'driver_dll_word': np.binary_repr(driver_dll_word, 5)})
            
            # Fill corresponding pattern with vcsel enable for the enabled chip
            if not np.isnan(s):
                s = int(s)
                dynamic_packet.fill(pattern_list=[p], chip_list=[s], field_dict={'vcsel_enable': '1', 'nir_vcsel_enable': nir_vcsel_enable, 'ir_vcsel_enable': ir_vcsel_enable})

# Show results
dynamic_packet.show(pattern_list=[0, patterns_per_frame-1])


#%% Configure time gating options - These can be adjusted by user

# Time gating support
time_gating_enabled = False

# Time gate each wavelength differently?
time_gate_per_wavelength = False

# Generic time gating value for any/all wavelengths
time_gating_value = 2.0

# Time gating values for each wavelength (unused if time_gate_per_wavelength is set to False)
nir_time_gating_value = 2.0
ir_time_gating_value = 0.0


#%% Propagate time-gating options to dynamic packet - Don't touch

    
# Add time gating
if time_gating_enabled:
    
    # Go through each pattern
    for p in range(patterns_per_frame):
        
        # Determine which wavelength is associated with this pattern
        wavelength = dynamic_packet.wavelength_for_pattern(p)
        print("wavelength for pattern " + str(p) + " is " + str(wavelength))
        
        # Determine which time gating value should be used for this
        if wavelength == dynamic_packet.nir_index:
            tgv = nir_time_gating_value
        elif wavelength == dynamic_packet.ir_index:
            tgv = ir_time_gating_value
        else:
            tgv = time_gating_value
            
        # Calculate time gating settings
        clk_flip, coarse, fine, finest, actual_delay_ns = delay_line.get_setting(common_delay + tgv)
        
        # Adjust
        clk_flip = np.binary_repr(clk_flip, 1)
        coarse = np.binary_repr(coarse, 4)
        fine = np.binary_repr(fine, 3)
        finest = np.binary_repr(finest, 1)

        # Fill pattern with new time gate value
        dynamic_packet.fill(pattern_list=[p], field_dict={'clk_flip': clk_flip, 'aqc_dll_coarse_word': coarse, 'aqc_dll_fine_word': fine, 'aqc_dll_finest_word': finest})

# Show results
dynamic_packet.show(pattern_list=[0, patterns_per_frame-1])


#%% Custom code - This section is custom and can be rewritten in its entirety depending on what's being done


#%% This section saves the file to the desired location

# Filename
filename = "dynamic_packet.txt"

# Choose directory to save
dir_to_save = easygui.diropenbox(title="Select a location to save the dynamic packet file", default=this_dir)

# Get string to write from dynamic packet
s = dynamic_packet.write()

# Write out
f = open(os.path.join(dir_to_save, filename), "w")
f.write(s)
f.close()