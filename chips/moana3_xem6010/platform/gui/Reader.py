# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 14:39:24 2021

@author: Dell-User
"""

from PyQt5 import QtCore
#TODO remove randint and sleep
from numpy.random import randint
import numpy as np
from time import perf_counter, sleep, perf_counter_ns
from os.path import join
from gui.Logger import Logger
from gui.LoggerStruct import LoggerStruct
        

class Reader(QtCore.QThread):
    """ Reader polls the read trigger, updates the packet with new data, and writes chip data to a file. """
    
    #################################################
    # Constructor
    ################################################# 
    def __init__(self, dut, packet, reader_struct):
        
        # Init QThread
        super().__init__()
        
        # DUT handle for accessing read methods
        self.__dut = dut
        
        # Packet handle for passing around collected data
        self.__packet = packet
        
        # Reader structure handle for sharing info between main and reader thread
        self.__reader_struct = reader_struct
        
        # Data readout streaming status
        self.__streaming = False
        
        # Watchdog counter for determining if reader cannot keep up with stream
        self.__watchdog = 0
        
        # Capture time
        self.__capture_time_ns = 0
        
        # # Buffer sizes - LSB size determines how many histograms are saved before spawning a logging thread to write them to file
        # self.__buffer_msb_size = 2
        # self.__buffer_lsb_size = 1000
        
        # # Buffer for storing data
        # buffer_shape = (self.__buffer_msb_size, self.__buffer_lsb_size,) + np.shape(packet.data)
        # print(buffer_shape)
        # self.__buffer = np.empty( buffer_shape, dtype=int)
        
        # # Pointers for keeping track of buffer location
        # self.__buffer_msb_pointer = 0
        # self.__buffer_lsb_pointer = 0
        
        # # Initialize logging classes if needed
        # if self.__reader_struct.logging:
            
        #     # Create logger structure
        #     self.__logger_struct = LoggerStruct()
            
        #     # Fill structure
        #     self.__logger_struct.experiment_directory = self.__reader_struct.experiment_directory
        #     self.__logger_struct.buffer = self.__buffer
        #     self.__logger_struct.capture_counter = self.__reader_struct.capture_counter

            

    #################################################
    # Write to a log file
    ################################################# 
    def __write_log_file(self):
        
        # Write to the log file
        np.save(join(self.__reader_struct.experiment_directory, "capture_" + str(self.__reader_struct.capture_counter)), self.__packet.data, fix_imports=False)
        
        
    #################################################
    # Add to buffer
    ################################################# 
    # def __add_to_buffer(self):
        
    #     # Write into buffer
    #     self.__buffer[self.__buffer_msb_pointer][self.__buffer_lsb_pointer] = self.__packet.data
            
    #     # Increment LSB pointer
    #     if self.__buffer_lsb_pointer + 1 < self.__buffer_lsb_size:
    #         self.__buffer_lsb_pointer = self.__buffer_lsb_pointer + 1
    #     else:
            
    #         # Spawn logging thread
    #         self.__start_logger()
            
    #         # Set capture counter value of logger
    #         self.__logger_struct.capture_counter = self.__buffer_lsb_pointer + 1
            
    #         # Reset lsb pointer
    #         self.__buffer_lsb_pointer = 0
            
    #         # Increment MSB pointer when LSB flips over
    #         if self.__buffer_msb_pointer + 1 < self.__buffer_msb_size:
    #             self.__buffer_msb_pointer = self.__buffer_msb_pointer + 1
    #         else:
    #             self.__buffer_msb_pointer = 0
                

    #################################################
    # Start logger
    ################################################# 
    # def __start_logger(self):
        
    #     # Fill logger structure
    #     self.__logger_struct.buffer_msb_pointer = self.__buffer_msb_pointer
    #     self.__logger_struct.buffer_lsb_pointer = self.__buffer_lsb_pointer + 1
    #     self.__logger = Logger(self.__logger_struct)
        
    #     self.__reader_struct.threadpool.start(self.__logger)
    
    #################################################
    # Fake read function for debugging purposes
    #################################################      
    def __fake_read_data(self):
                
        # Call the read function
        self.__packet.data = randint(0, randint(1, high = 4096, size=1)[0], (self.__packet.number_of_chips* self.__packet.actual_number_of_frames * self.__packet.patterns_per_frame * self.__packet.bins_per_histogram))
        # self.time = perf_counter()
        # sleep(0.05)
        
        # Increment the capture counter
        self.__reader_struct.increment_capture_counter()
        
        
    #################################################
    # Begin streaming
    ################################################# 
    def __begin_stream(self):
        
        # Final reset
        print("Initializing stream")
        self.__dut.pulse_signal('cell_reset')
        sleep(0.1)
        
        # Calculate integration_time_ns
        self.__capture_time_ns = self.__packet.capture_time * 1e9
        
        # Clear any existing trigger, begin the stream
        print("Capturing histograms")
        self.__dut.check_read_trigger()
        self.__dut.FrameController.begin_stream()
        

    #################################################
    # End streaming
    ################################################# 
    def __end_stream(self):
        
        # End the stream
        self.__dut.FrameController.end_stream()
        print("Stream finished")
        

    #################################################
    # Read function for collecting data
    #################################################      
    def __read_data_by_stream(self):
            
        # Check for read trigger
        if self.__dut.check_read_trigger():
            
            # Grab current time
            t1 = perf_counter_ns()
            
            # # Acknowledge read trigger
            # self.__dut.acknowledge_read_trigger()
        
            # Wait for streamout process to complete based on capture time
            while perf_counter_ns() - t1 < self.__capture_time_ns:
                pass
            
            # Read the data
            self.__dut.read_master_fifo_data(self.__packet)
            
            # Acknowledge read trigger
            self.__dut.acknowledge_read_trigger()
            
            # Increment capture counter
            self.__reader_struct.increment_capture_counter()
            
            
    #################################################
    # Read function for collecting data using run/stop capture mode
    #################################################      
    def __read_data_by_capture(self):
        
        # Run capture
        self.__dut.FrameController.run_capture()
        # sleep(0.04)
        
        # Read the data into the packet
        self.__dut.read_master_fifo_data(self.__packet)
        
        # Log data
        if self.__reader_struct.logging:
            self.__write_log_file()
    
        # Increment the capture counter
        self.__reader_struct.increment_capture_counter()


    #################################################
    # Function to determine if Reader thread should be stopped
    #################################################    
    def __should_stop(self):
        if self.__reader_struct.reader_should_stop:
            print("Reader thread stopped by main thread")
            return True
        elif self.__reader_struct.capture_counter == self.__reader_struct.number_of_captures:
            print("Reader thread stopped internally")
            return True
        else:
            return False
        
            
    #################################################
    # Run function (called implicitly by thread.start)
    #################################################
    def run(self):
        
        # Begin the stream
        if self.__reader_struct.stream_mode:
            if not self.__reader_struct.debug:
                self.__begin_stream()
        
        # Event loop
        while True:
            
            # Read data and log until stopped
            if not self.__should_stop():
                
                # Read data
                if not self.__reader_struct.debug:
                    if self.__reader_struct.stream_mode:
                        self.__read_data_by_stream()
                    else:
                        self.__read_data_by_capture()
                else:
                    self.__fake_read_data()
                    
                # Add data to buffer if logging
                if self.__reader_struct.logging:
                    self.__write_log_file()
                    # self.__add_to_buffer()
                    
            # Exit thread after stop function
            else:
                self.stop()
                break
            
            
    #################################################
    # Stop function
    #################################################   
    def stop(self):
        
        # End the stream
        if not self.__reader_struct.debug:
            self.__end_stream()
            
        # # Finish logging if needed
        # if self.__buffer_lsb_pointer > 0:
        #     print("Writing remaining logs")
        #     self.__start_logger()
            
        # # Always wait for logger to complete before closing
        # if self.__reader_struct.logging:
        #     self.__reader_struct.threadpool.waitForDone()
        #     # if not self.__logger_struct.logger_done:
        #     #     self.__logger_struct.logger_should_stop = True
        #     #     self.__logger.wait()
        
        # Exit the thread
        self.exit()

