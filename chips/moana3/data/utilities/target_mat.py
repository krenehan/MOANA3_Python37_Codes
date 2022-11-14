# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:43:11 2022

@author: Dell-User
"""

import numpy as np
import os
import easygui
from translate_mat import *

# Options
do = True

# Get the utilities directory
util_dir = os.getcwd()

# Get the target directory
target_dir = easygui.diropenbox()

# Change working directory
os.chdir(target_dir)

# Must translate
translate_mat()

# Optional operations
if do:
    pass