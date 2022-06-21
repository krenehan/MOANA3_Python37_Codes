# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:43:37 2021

The EmitterPatternStruct class encapsulates information passed between the EmitterPatternDialog class and the main GUI. 


@author: Kevin Renehan
"""

from numpy import zeros

class EmitterPatternStruct():
    '''Data structure for storing emitter pattern information'''
    
    # Constructor
    def __init__(self, patterns_per_frame=16):
        
            # Store number of chips and patterns per frame
            self.__patterns_per_frame = patterns_per_frame
            self.__number_of_chips = 16
            
            # Create emitter pattern array
            self.emitter_pattern = zeros( (self.__patterns_per_frame, self.__number_of_chips), dtype=bool)
            
            # Create the IR array
            self.ir_emitters = zeros( (self.__number_of_chips,), dtype=bool)


    ################################
    # Update emitter pattern
    ################################
    def update(self, patterns_per_frame):
        
        # Check to see if the settings have changed
        if self.__patterns_per_frame != patterns_per_frame:
            
            # Store number of chips and patterns per frame
            self.__patterns_per_frame = patterns_per_frame
            
            # Create emitter pattern array
            self.emitter_pattern = zeros( (self.__patterns_per_frame, self.__number_of_chips), dtype=bool)
            
            
    ################################
    # Patterns per frame property
    ################################
    @property
    def patterns_per_frame(self):
        return self.__patterns_per_frame
    
    @patterns_per_frame.setter
    def patterns_per_frame(self, new_patterns_per_frame):
        print("Patterns per frame cannot be set directly")
        
    ################################
    # Number of chips property
    ################################
    @property
    def number_of_chips(self):
        return self.__number_of_chips
    
    @number_of_chips.setter
    def number_of_chips(self, new_number_of_chips):
        print("Number of chips cannot be set directly")
        