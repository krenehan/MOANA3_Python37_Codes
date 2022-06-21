# System includes
import sys
import os

chip_name = "moana3"
experimental_dir = "../../.."

# Create a class that holds testing paths, to avoid polluting global namespace
class TestingPaths:
    # Initialize testing paths 
    def __init__(self, chip_name, experimental_dir):
        
        # platform info
        self.chip_name = chip_name
        self.experimental_dir = experimental_dir
        
        # Other setup
        self.chip_dir = os.path.join(os.path.join(self.experimental_dir, "chips"), self.chip_name)
        self.platform_dir = os.path.join(self.chip_dir, "platform")
        self.experiment_dir = os.path.join(self.chip_dir, "experiments")
        self.equipment_dir = os.path.join(self.experimental_dir, "equipment")
        self.data_dir = os.path.join(self.chip_dir, "data");

        # Bitfile path
        self.bitfile_path = os.path.join(os.path.join(os.path.join(self.platform_dir, "fpga"), "bit_files"), \
            "MOANA2_SCAN_CLOCKS_500kHz.bit")

        # Append directories
        include_dirs = self.get_include_dirs()
        for dir in include_dirs:
            sys.path.append(dir)
 
    @staticmethod
    def get_subdirectories(dir):
        return [os.path.join(dir, name) for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

    def get_include_dirs(self):
        return [self.equipment_dir, self.platform_dir, self.experiment_dir] + \
            TestingPaths.get_subdirectories(self.platform_dir) + \
            TestingPaths.get_subdirectories(self.equipment_dir) + \
            TestingPaths.get_subdirectories(self.experiment_dir)

# Global variable with all the testing paths
paths = TestingPaths(chip_name = chip_name, experimental_dir = experimental_dir)

# Python libraries
import numpy as np
import time
import binascii
import datetime
import pickle

# Include Equipment
#import  Agilent8133A

# Platform and helpers
import test_platform
import infrastructure
import interface





