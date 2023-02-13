# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:37:45 2021

A pseudo-struct that contains variables passed to the Reader thread

@author: Kevin Renehan
"""

from os.path import exists, abspath


class ReaderStruct():
    """ Data structure for passing information to Reader thread """
        
    # Structure variables
    __experiment_directory = ''
    __experiment_directory_set = False
    __logging_enabled = False
    __number_of_captures = 100
    __capture_time = 0
    __debug = False
        
    
    # ====================================================
    # Logging directory property
    # ====================================================
    @property
    def experiment_directory(self):
        return self.__experiment_directory
    
    @experiment_directory.setter
    def experiment_directory(self, new_experiment_directory):
        new_experiment_directory = abspath(str(new_experiment_directory))
        if exists(new_experiment_directory):
            self.__experiment_directory = new_experiment_directory
            self.__experiment_directory_set = True
        else:
            print("Logging directory does not exist")
            self.__experiment_directory_set = False
            
            
    # ====================================================
    # Logging directory set property
    # ====================================================
    @property
    def experiment_directory_set(self):
        return self.__experiment_directory_set
    
    @experiment_directory_set.setter
    def experiment_directory_set(self, new_experiment_directory_set):
        print("Logging directory set cannot be modified externally")
        
        
    # ====================================================
    # Logging enabled property
    # ====================================================
    @property
    def logging_enabled(self):
        return self.__logging_enabled
    
    @logging_enabled.setter
    def logging_enabled(self, new_logging_enabled):
        try:
            new_logging_enabled = bool(new_logging_enabled)
            self.__logging_enabled = new_logging_enabled
        except (ValueError, TypeError):
            print("Logging Enabled value not valid")
            
            
    # ====================================================
    # Number of captures property
    # ====================================================
    @property
    def number_of_captures(self):
        return self.__number_of_captures
    
    @number_of_captures.setter
    def number_of_captures(self, new_number_of_captures):
        try:
            new_number_of_captures = int(new_number_of_captures)
            self.__number_of_captures = new_number_of_captures
        except (ValueError, TypeError):
            print("Number of captures value not valid")
            
            
    # ====================================================
    # Capture Time property
    # ====================================================
    @property
    def capture_time(self):
        return self.__capture_time
    
    @capture_time.setter
    def capture_time(self, new_capture_time):
        try:
            new_capture_time = float(new_capture_time)
            self.__capture_time = new_capture_time
        except (ValueError, TypeError):
            print("Capture time value not valid")
        
        
    # ====================================================
    # Debug property
    # ====================================================
    @property
    def debug(self):
        return self.__debug
    
    @debug.setter
    def debug(self, new_debug):
        try:
            new_debug = bool(new_debug)
            self.__debug = new_debug
        except (ValueError, TypeError):
            print("Debug value not valid")
            
            
    # Connect signals
    def connect_signals(self, start, stop):
        
        self.reader_start_signal = start
        self.reader_stop_signal = stop