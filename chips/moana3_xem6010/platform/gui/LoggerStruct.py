# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:21:00 2022

@author: Dell-User
"""



class LoggerStruct():
    """ Data structure for passing information to Reader thread """
        
    # Structure variables
    __experiment_directory = ''
    __buffer = None
    __buffer_msb_pointer = 0
    __buffer_lsb_pointer = 0
    __capture_counter = 0
    # __begin_logging = False
    # __logger_should_stop = False
    # __logger_done = False

    
    # ====================================================
    # Experiment directory property
    # ====================================================
    @property
    def experiment_directory(self):
        return self.__experiment_directory
    
    @experiment_directory.setter
    def experiment_directory(self, new_experiment_directory):
        self.__experiment_directory = new_experiment_directory
        
        
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
    # Buffer MSB pointer property
    # ====================================================
    @property
    def buffer_msb_pointer(self):
        return self.__buffer_msb_pointer
    
    @buffer_msb_pointer.setter
    def buffer_msb_pointer(self, new_buffer_msb_pointer):
        self.__buffer_msb_pointer = new_buffer_msb_pointer
        
        
    # ====================================================
    # Buffer LSB pointer property
    # ====================================================
    @property
    def buffer_lsb_pointer(self):
        return self.__buffer_lsb_pointer
    
    @buffer_lsb_pointer.setter
    def buffer_lsb_pointer(self, new_buffer_lsb_pointer):
        self.__buffer_lsb_pointer = new_buffer_lsb_pointer
        
        
    # ====================================================
    # Capture counter property
    # ====================================================
    @property
    def capture_counter(self):
        return self.__capture_counter
    
    @capture_counter.setter
    def capture_counter(self, new_capture_counter):
        self.__capture_counter = new_capture_counter
        
        
    # # ====================================================
    # # Begin logging property
    # # ====================================================
    # @property
    # def begin_logging(self):
    #     return self.__begin_logging
    
    # @begin_logging.setter
    # def begin_logging(self, new_begin_logging):
    #     self.__begin_logging = new_begin_logging
        
        
    # # ====================================================
    # # Logger should stop property
    # # ====================================================
    # @property
    # def logger_should_stop(self):
    #     return self.__logger_should_stop
    
    # @logger_should_stop.setter
    # def logger_should_stop(self, new_logger_should_stop):
    #     self.__logger_should_stop = new_logger_should_stop
        
        
    # # ====================================================
    # # Logger done property
    # # ====================================================
    # @property
    # def logger_done(self):
    #     return self.__logger_done
    
    # @logger_done.setter
    # def logger_done(self, new_logger_done):
    #     self.__logger_done = new_logger_done
        