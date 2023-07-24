# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 15:42:47 2022

@author: Dell-User
"""

def interpret_yield():
    
    # Load the yield file
    f = open("yield.txt", 'r')
    ll = f.readlines()
    f.close()
    
    # Sources and detectors
    d = None
    nir_s = None
    ir_s = None
    
    # Legacy support
    legacy = False
    
    for l in ll:
        
        if 'detectors' in l:
            
            # Process line
            t = l.split('=')[1].split(',')
            d = [int(t[i]) for i in range(len(t))]
                
            
        elif 'nir_sources' in l:
            
            # Process line
            t = l.split('=')[1].split(',')
            nir_s = [int(t[i]) for i in range(len(t))]
            
            
        elif 'ir_sources' in l:
            
            # Process line
            t = l.split('=')[1].split(',')
            ir_s = [int(t[i]) for i in range(len(t))]
            
        # Legacy support for old yield files
        elif 'sources' in l:
            legacy=True
            
            # Process line
            t = l.split('=')[1].split(',')
            s = [int(t[i]) for i in range(len(t))]
            
    if legacy:
        return s, d
    else:
        return nir_s, ir_s, d