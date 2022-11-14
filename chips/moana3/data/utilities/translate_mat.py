# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 16:55:43 2022

@author: Dell-User
"""

import numpy as np
import os
import h5py
import pickle

def translate_mat():
    
    # Directory info
    filelist = os.listdir()
    
    # Look for the .mat file
    print("Searching for .mat file")
    found = False
    for f in range(len(filelist)):
        
        # Look for .mat
        if '.mat' in filelist[f]:
            print("Found .mat file")
            idx = f
            found = True
            break
        
    if found:

        # Grab dictionaries
        print("Loading .mat file")
        cudadict = h5py.File(filelist[idx])
            
        # Extract data from dictionaries
        bkgTpsf = np.array(cudadict['bkgTpsf'])
        perturbTpsf = np.array(cudadict['perturbTpsf'])
        diffTpsf = np.array(cudadict['diffTpsf'])
        mHeaders = cudadict['mHeaders']
        
        # Interpret mHeaders struct
        mHeadersDict = {}
        for element in list(mHeaders.keys()):
            mHeadersDict[str(element)] = mHeaders[element][0][0]
            
        # Save arrays
        print("Saving numpy arrays")
        np.savez_compressed('bkgTpsf.npz', data=bkgTpsf)
        np.savez_compressed('perturbTpsf.npz', data=perturbTpsf)
        np.savez_compressed('diffTpsf.npz', data=diffTpsf)
        
        # Save dictionary
        print("Saving mHeaders file")
        f = open('mHeaders.pkl', 'wb')
        pickle.dump(mHeadersDict, f)
        f.close()
        
        print("Done translating .mat file")
        
    else:
        
        print(".mat file not found")
    