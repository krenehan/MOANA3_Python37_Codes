# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:34:32 2023

# Add 3D information from text file into SD file.

@author: Dell-User
"""

from scipy.io import savemat, loadmat
import numpy as np

# SD file path
sd_2D = r'C:\Users\Dell-User\Dropbox\MOANA\Homer3\new_moana3_probe\MOANA3_RIGID_4BY4.SD'

# SD file path to output
sd_3D = r'C:\Users\Dell-User\Dropbox\MOANA\Homer3\new_moana3_probe\MOANA3_RIGIDFLEX_4BY4_3D.SD'

# Text file path
txt_3D = r'C:\Users\Dell-User\Dropbox\MOANA\Homer3\new_moana3_probe\MOANA3_RIGIDFLEX_4BY4_3D.txt'

# SD indexing (the ones that I know)
WAVELENGTH = 0
SRC_POSITION = 1
DET_POSITION = 2
DUMMY_POSITION = 3
NUM_SRC = 13
NUM_DET = 14
MEAS_LIST = 18
SPRINGS = 20
ANCHORS = 21
MEAS_UNIT = 23

# Load the SD file
mdict = loadmat(sd_2D, appendmat=False)

# Look for SD
if 'SD' in mdict:
    sd = mdict['SD']
    
# Get number of sources and detectors
numSrc = int(sd[0][0][SRC_POSITION])
numDet = int(sd[0][0][DET_POSITION])
numDum = len(sd[0][0][DUMMY_POSITION])

# Create arrays
source_positions = np.zeros_like(sd[0][0][SRC_POSITION], dtype=float)
detector_positions = np.zeros_like(sd[0][0][DET_POSITION], dtype=float)
dummy_positions = np.zeros_like(sd[0][0][DUMMY_POSITION], dtype=float)

# Load the text file
f = open(txt_3D, 'r')
ll = f.readlines()
f.close()

# Go through lines
for l in ll:
    
    # For keeping track
    detector = False
    source = False
    dummy = False
    
    # Check for detector, source, or dummy character
    if l[0] == 'd':
        detector = True
    elif l[0] == 's':
        source = True
    elif l[0] == 'm':
        dummy = True
    else:
        continue
    
    # Get index 
    idx = int(l[1:len(l)].split(":")[0]) - 1
    
    # Split string to retrieve coordinates
    coords = np.array(l.split(": ")[1].strip().split(" ")).astype(float)
    
    # Fill 
    if detector:
        detector_positions[idx] = coords
    elif source:
        source_positions[idx] = coords
    elif dummy:
        dummy_positions[idx] = coords
    
# Replace
sd[0][0][SRC_POSITION] = source_positions
sd[0][0][DET_POSITION] = detector_positions
sd[0][0][DUMMY_POSITION] = dummy_positions

# Check that all arrays are float arrays (due to bug in Homer3 HDF5 Save function)
for idx in range(len(sd[0][0])):
    
    # Check if the index is numeric
    if np.issubdtype(sd[0][0][idx].dtype, np.number):
    
        # Check dimensions and convert to float
        if np.squeeze(sd[0][0][idx]).ndim > 0:
            sd[0][0][idx] = sd[0][0][idx].astype(float)
            
# Create dictionary
mdict['SD'] = sd

# Save file
savemat(sd_3D, mdict, appendmat=False, oned_as='column')