# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User
"""


import os
import easygui
import shutil


# List of relevant files within subdirectory that should be copied
relevant_files = ( \
                    'averaged.npz', \
                    'captures.npz', \
                    'emitter_pattern.npy', \
                    'ir_emitters.npy', \
                    'test_setup.txt', \
                    'yield.txt', \
                )
    
# Get the directory to copy
to_copy_dir = easygui.diropenbox(title="Choose directory to copy from", default=os.path.abspath("C:/Users/Dell-User/Downloads"))

# Get the directory to copy to
copy_to_dir = easygui.diropenbox(title="Choose directory to copy to", default=os.path.abspath("C:/Users/Dell-User/Dropbox/MOANA/2020 January Tapeout/MOANA2 Python Codes/MOANA2_Python37_Codes/chips/moana2/data"))

# Change working directory
os.chdir(to_copy_dir)


###############################################################################
# Check directory for correct structure
###############################################################################
print("Checking directory structure for relevant files")

# Check for a data directory
if 'data' not in os.listdir():
    raise Exception("data directory not found in target directory")
    
# Descend into data directory
data_dir = os.path.join(to_copy_dir, 'data')
os.chdir(data_dir)

# Get a list of the subdirectories
subdirectory_list = os.listdir()

# Copy the subdirectory list
subdirectories_to_copy = subdirectory_list.copy()

# Descend into each subdirectory and perform the operations
for sd in subdirectory_list:
    
    # Directory to descend into
    next_dir = os.path.join(data_dir, sd)
    
    # Ensure that subdirectories are actually directories
    if not os.path.isdir(next_dir):
        print(next_dir + " is not a directory and was skipped")
        subdirectories_to_copy.remove(sd)
        continue
    
    # Descend
    os.chdir(next_dir)
    
    # Subdirectory files
    sd_files = os.listdir()
    
    # Check for relevant files within subdirectory
    for f in relevant_files:
        if f not in sd_files:
            raise Exception("Could not find " + f + " in " + sd)
    
# Status
print("Directory passes structure and file checks")
    
###############################################################################
# Perform operations when all checks are complete
###############################################################################
print("Copying")

# Move to copy_to directory
os.chdir(copy_to_dir)

# Check for data directory and create it if it's not already there
if 'data' not in os.listdir():
    os.mkdir('data')

# Move to data directory
os.chdir(os.path.join(copy_to_dir, 'data'))

# Store new data directory path
new_data_dir = os.getcwd()

for sd in subdirectories_to_copy:
    
    # Create subdirectory if it doesn't exist
    if sd not in os.listdir():
        os.mkdir(sd)
        print("Created " + sd + " in " + new_data_dir)
        
    # Path to latest directory
    new_copy_dir = os.path.join(new_data_dir, sd)
    
    # Copy relevant files
    for f in relevant_files:
        
        # File path
        fp = os.path.join(os.path.join(data_dir, sd), f)
        
        # Copy the file
        shutil.copy2(fp, new_copy_dir)
        print("Copied " + f + " to " + sd)
    
print("Done")