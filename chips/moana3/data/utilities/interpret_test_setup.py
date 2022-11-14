# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Kevin Renehan

Interpret a test setup file.
"""

import os


def interpret_test_setup():

    # Directory info
    filelist = os.listdir()
    
    # Look for previously generated accumulated file
    print("Searching for test setup file")
    found = False
    for f in range(len(filelist)):
        
        # Look for accumulated tag
        if 'test_setup.txt' in filelist[f]:
            print("Found test setup file")
            found = True
    
    # Test setup file must be present
    if not found:
        
        raise Exception("Test setup file not found")
        
    else:
        
        # Load
        print("Opening test setup file")
        f = open("test_setup.txt", "r")
        
        # Interpret lines
        print("Interpreting test setup file")
        ldict = {}
        l = f.readlines()
        for line in l:
            prefix, suffix = line.split(": ", 1)
            suffix = suffix.split('\n')[0]
            ldict[prefix] = suffix
        
        # Close file
        print("Closing test setup file")
        f.close()
            
        # Remove unused parameters
        to_pop = []
        for entry in ldict:
            if ldict[entry] == '':
                to_pop.append(entry)
        for entry in to_pop:
            ldict.pop(entry)
        
        # Return
        print("Done")
        return ldict
            
