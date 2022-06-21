# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:11:07 2022

@author: Kevin Renehan
"""

from PyQt5 import QtCore
from numpy import save, shape
from time import sleep

class Logger(QtCore.QRunnable):
    """ Logger writes chip data to a directory. """
    
    
    #################################################
    # Constructor
    ################################################# 
    def __init__(self, logger_struct):
        
        # Init QThread
        # super().__init__()
        
        # Init QRunnable
        super(Logger, self).__init__()
        
        # Keep track of logger structure
        self.__logger_struct = logger_struct
        
        # Keep track of capture counter
        self.__capture_counter = self.__logger_struct.capture_counter
        
        
        
    #################################################
    # Run function (called implicitly by thread.start)
    #################################################
    @QtCore.pyqtSlot()
    def run(self):
                    
        # Loop through completed captures
        for capture in range(self.__logger_struct.buffer_lsb_pointer):
            
            # Save to file
            save(self.__logger_struct.experiment_directory + "\\" + str(self.__capture_counter + capture), \
                      self.__logger_struct.buffer[self.__logger_struct.buffer_msb_pointer][capture], \
                      fix_imports=False)
                
            # Exit thread after stop function
            # else:
            #     self.stop()
            #     break
            
            
    #################################################
    # Stop function
    #################################################   
    def stop(self):
        
        # Exit the thread
        self.exit()