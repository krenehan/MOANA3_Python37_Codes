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
    s = None
    
    for l in ll:
        
        if 'detectors' in l:
            
            # Process line
            t = l.split('=')[1].split(',')
            d = [int(t[i]) for i in range(len(t))]
                
            
        elif 'sources' in l:
            
            # Process line
            t = l.split('=')[1].split(',')
            s = [int(t[i]) for i in range(len(t))]
            
    return s, d