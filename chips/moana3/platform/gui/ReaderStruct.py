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
    __stream_mode = False
    __experiment_directory = ''
    __experiment_directory_set = False
    __logging = False
    __number_of_captures = 100
    __reader_done = False
    __reader_should_stop = False
    __capture_counter = 0
    __buffer = None
    __debug = False
    __threadpool = None
    
    
    # ====================================================
    # Stream mode property
    # ====================================================
    @property
    def stream_mode(self):
        return self.__stream_mode
    
    @stream_mode.setter
    def stream_mode(self, new_stream_mode):
        self.__stream_mode = bool(new_stream_mode)
        
    
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
    def logging(self):
        return self.__logging
    
    @logging.setter
    def logging(self, new_logging):
        try:
            new_logging = bool(new_logging)
            self.__logging = new_logging
        except (ValueError, TypeError):
            print("Logging value not valid")
            
            
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
    # Reader done property
    # ====================================================
    @property
    def reader_done(self):
        return self.__reader_done
    
    @reader_done.setter
    def reader_done(self, new_reader_done):
        print("Reader done cannot be modified externally")
        
        
    # ====================================================
    # Reader should stop property
    # ====================================================
    @property
    def reader_should_stop(self):
        return self.__reader_should_stop
    
    @reader_should_stop.setter
    def reader_should_stop(self, new_reader_should_stop):
        try:
            new_reader_should_stop = bool(new_reader_should_stop)
            self.__reader_should_stop = new_reader_should_stop
        except (ValueError, TypeError):
            print("Reader should stop value not valid")
            
            
    # ====================================================
    # Capture counter property
    # ====================================================
    @property
    def capture_counter(self):
        return self.__capture_counter
    
    @capture_counter.setter
    def capture_counter(self, new_capture_counter):
        print("Capture cannot be modified externally")
        
        
    # ====================================================
    # Buffer property
    # ====================================================
    @property
    def buffer(self):
        return self.__buffer
    
    @buffer.setter
    def buffer(self, new_buffer):
        self.__buffer = new_buffer
        
        
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
            
            
    # ====================================================
    # Threadpool property
    # ====================================================
    @property
    def threadpool(self):
        return self.__threadpool
    
    
    # ====================================================
    # Threadpool property
    # ====================================================
    @threadpool.setter
    def threadpool(self, new_threadpool):
        self.__threadpool = new_threadpool
     
        
    # ====================================================
    # Increment capture counter function
    # ====================================================
    def increment_capture_counter(self):
        self.__capture_counter += 1 


    # ====================================================
    # Reset capture counter function
    # ====================================================
    def reset_capture_counter(self):
        self.__capture_counter = 0
        
        