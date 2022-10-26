# System includes
import sys
import os
import time
import binascii
import datetime
import pickle
import math
import numpy as np

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

        # Bitfile path
        self.bitfile_path = os.path.join(os.path.join(os.path.join(self.platform_dir, "fpga"), "bit_files"), \
            # 'MOANA3_INTERNAL_CLOCKS_50MHz_nopadreverse.bit') # Uncomment line for internal clock
            # 'MOANA3_INTERNAL_CLOCKS_50MHz_noreverse.bit') # Uncomment line for internal clock
            # 'MOANA3_INTERNAL_CLOCKS_50MHz_fullchain.bit') # Uncomment line for internal clock
            'MOANA3_RIGID4BY4_INTERNAL_CLOCKS_6MHz.bit')
            # 'MOANA3_RIGID4BY4_INTERNAL_FRAME_ARBITER_V2.bit')
            # 'MOANA3_EXTERNAL_REFCLK.bit') # Uncomment line for external laser clock



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
paths = TestingPaths(chip_name = "moana3", experimental_dir = "../../../../")

# Include Equipment
#import  Agilent8133A

# Platform and helpers
import test_platform
import infrastructure
import interface
import MultipleDataPlotter
import DataPacket


