# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Kevin Renehan

Interpret a dynamic packet file. Find patterns where sources are active.
"""

import os
import numpy as np


def interpret_dynamic_packet():

    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for dynamic packet file")
    found = False
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if 'dynamic_packet.txt' in filelist[f]:
            print("Found dynamic packet file")
            found = True
    
    # Test setup file must be present
    if not found:
        raise Exception("Dynamic packet file not found")
        
    # Load
    print("Opening dynamic packet file")
    f = open("dynamic_packet.txt", 'r')
    ll = f.readlines() 
    f.close()
    
    # Find number of patterns
    for l in ll[::-1]:
        if "Pattern" in l:
            patterns_per_frame = int(l.split("Pattern ")[1].split(':')[0]) + 1
            break
    
    # Find number of chips
    for l in ll[::-1]:
        if "Chip" in l:
            number_of_chips = int(l.split("Chip ")[1].split(':')[0]) + 1
            break
        
    # Number of wavelengths
    number_of_wavelengths = 2
    
    # Interpret
    print("Interpreting emitter pattern file")
    
    # Find the emitter in each pattern
    vcsel_enable, nir_vcsel_enable, ir_vcsel_enable = False, False, False
    pattern, chip = 0, 0
    emitter_pattern = np.zeros((patterns_per_frame, number_of_chips, number_of_wavelengths), dtype=bool)
    for i, l in enumerate(ll):
        
        # Fill array if conditions are met
        if vcsel_enable and nir_vcsel_enable:
            emitter_pattern[pattern][chip][0] = True
            
        # Fill array if conditions are met
        if vcsel_enable and ir_vcsel_enable:
            emitter_pattern[pattern][chip][1] = True
        
        # Keep track of the pattern number
        if "Pattern" in l:
            pattern = int(l.split("Pattern ")[1].split(':')[0])
            
            # Reset vcsel enable, nir_vcsel_enable, and ir_vcsel_enable
            vcsel_enable, nir_vcsel_enable, ir_vcsel_enable = False, False, False
            continue
        
        # Keep track of the chip number
        if "Chip" in l:
            chip = int(l.split("Chip ")[1].split(':')[0])
            
            # Reset vcsel enable, nir_vcsel_enable, and ir_vcsel_enable
            vcsel_enable, nir_vcsel_enable, ir_vcsel_enable = False, False, False
            continue
        
        # Find nir_vcsel_enable
        if ("nir_vcsel_enable" in l) and ("1" in l):
            nir_vcsel_enable = True
            print("nir_vcsel_enable found in line {} for pattern {} chip {}".format(i, pattern, chip))
            continue
        
        # Find ir_vcsel_enable
        if ("ir_vcsel_enable" in l) and ("1" in l):
            ir_vcsel_enable = True
            print("ir_vcsel_enable found in line {} for pattern {} chip {}".format(i, pattern, chip))
            continue
        
        # Find vcsel_enable
        if ("vcsel_enable" in l) and ("1" in l):
            vcsel_enable = True
            print("vcsel_enable found in line {} for pattern {} chip {}".format(i, pattern, chip))
            continue
    
    # Return
    print("Done")
    return emitter_pattern
            
