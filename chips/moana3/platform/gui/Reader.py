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

import threading
def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))
        

class Reader(QtCore.QObject):
    """ Reader polls the read trigger, updates the packet with new data, and writes chip data to a file. """
    
        
    # Define signal for passing data back to gui thread
    new_data_available = QtCore.pyqtSignal(object)
    
    # Define signal for indicating that reader is done
    finished = QtCore.pyqtSignal(int)
    
    # Define signal for indicating that reader is done logging
    logging_finished = QtCore.pyqtSignal(int)
        
    # Capture counter
    capture_counter = 0
    
    # Counts captures in current collection
    captures_in_current_collection = 0
    
    # Fake counter for data send
    fake_data_counter = 0
    
    # Logging signals
    logging = False # Determines if capture is to be logged
    start_logging_signal_caught = False # Catch for pyqt signal
    stop_logging_signal_caught = False # Catch for pyqt signal
    
    # Timestamp
    start_time = 0
    trigger_time = 0
    
    
    #################################################
    # Constructor
    ################################################# 
    def __init__(self, dut, packet, reader_struct):
        
        # Init QThread
        super().__init__()
        
        # logthread('reader.__init__')
        
        # DUT handle for accessing read methods
        self.dut = dut
        
        # Packet handle for passing around collected data
        self.packet = packet
        
        # Reader structure handle for sharing info between main and reader thread
        self.experiment_directory = reader_struct.experiment_directory
        self.logging_enabled = reader_struct.logging_enabled
        self.number_of_captures = reader_struct.number_of_captures
        self.debug = reader_struct.debug
        self.capture_time = reader_struct.capture_time
        
        # Keep track of reader_struct
        self.reader_struct = reader_struct


    ################################################# 
    # Increment capture counter function
    ################################################# 
    def increment_capture_counter(self):
        self.capture_counter += 1 
        if self.logging:
            self.captures_in_current_collection += 1


    ################################################# 
    # Reset capture counter function
    ################################################# 
    def reset_capture_counter(self):
        self.capture_counter = 0
            

    #################################################
    # Write to a log file
    ################################################# 
    def write_log_file(self):
        
        # Write to the log file
        np.save(join(self.experiment_directory, "capture_" + str(self.capture_counter)), self.packet.data, fix_imports=False)

    
    #################################################
    # Fake read function for debugging purposes
    #################################################      
    def fake_read_data(self):
        
        if self.fake_data_counter > 0:
            
            # Reset
            self.fake_data_counter = 0
                
            # Call the read function
            # self.packet.data = np.zeros(np.shape(self.packet.data))
            self.packet.data = randint(0, randint(1, high = 2**20-1, size=1)[0], np.shape(self.packet.data))
            
            # Indicate that new data is available
            self.new_data_available.emit(self.packet.data)
                
            # Write to log file
            if self.logging:
                self.write_log_file()
                
            # Increment capture counter
            self.increment_capture_counter()
            
        else:
            
            self.fake_data_counter = self.fake_data_counter + 1
            
        
    #################################################
    # Begin streaming
    ################################################# 
    def begin_blitz(self):
        
        # Clear any existing trigger, begin the stream
        print("Capturing histograms")
        self.dut.FrameController.begin_blitz()
    
    
    #################################################
    # Wait for refclk started signal from FPGA
    #################################################   
    def wait_for_refclk_started(self):
        
        # Check for trigger in indicating that refclk has started
        pass
    
    
    #################################################
    # Wait for refclk started signal from FPGA
    #################################################   
    def send_start_trigger(self):
        
        # Report
        print("Sending trigger")
        
        # Send trigger signal to FPGA
        if not self.debug:
            self.dut.ttl_trigger()
            
        # Log the time
        self.trigger_time = perf_counter() - self.start_time
        
        # Write out trigger time file
        if self.logging:
            s = "Onset" + "\t" + "Duration" + "\t" + "Amplitude" + "\t" + "trial_type" + "\n"
            s += str(self.trigger_time) + "\t" + "1" + "\t" + "1" + "\t" + "1" + "\n"
            join(self.experiment_directory, "capture_" + str(self.capture_counter))
            f = open(join(self.experiment_directory, "events.tsv"), "w")
            f.write(s)
            f.close()
        

    #################################################
    # End streaming
    ################################################# 
    def end_blitz(self):
        
        # End the stream
        self.dut.FrameController.end_blitz()
        print("Blitz finished")
        

    #################################################
    # Read function for collecting data
    #################################################      
    def read_data(self):
            
        # Check for read trigger
        if self.dut.check_ram_trigger():
            
            # Read the data
            self.dut.read_master_fifo_data(self.packet)
        
            # Indicate that new data is available
            self.new_data_available.emit(self.packet.data)
                    
            # Write to log file
            if self.logging:
                self.write_log_file()
                
            # Increment capture counter
            self.increment_capture_counter()


    #################################################
    # Function to determine if Reader thread should be stopped
    #################################################    
    def should_stop_logging(self):
        if self.captures_in_current_collection == self.number_of_captures:
            print("Reader stopped internally")
            self.stop_logging()
        else:
            return False


    #################################################
    # Check if logging signals were received
    ################################################# 
    def check_logging_signals(self):
        
        # Start logging if this signal is caught and logging is enabled
        if self.start_logging_signal_caught: 
            
            # Update logging bit
            self.logging = True if self.logging_enabled else False
            print("Logging set to " + str(self.logging))
            
            # Reset catch 
            self.start_logging_signal_caught = False
            
            # Send trigger
            self.send_start_trigger()
            
        
        # Stop logging if this signal is caught
        elif self.stop_logging_signal_caught:
            
            # Update logging bit
            self.logging = False
            print("Logging set to " + str(self.logging))
            
            # Emit logging finished signal
            self.logging_finished.emit(0)
            
            # Reset catch 
            self.stop_logging_signal_caught = False
            
            # Reset captures_in_current_collection
            self.captures_in_current_collection = 0
                
                
    #################################################
    # Function to determine if Reader thread should be stopped
    #################################################
    @QtCore.pyqtSlot()
    def trigger_read(self):
        
        # # Print
        # print("Reader received trigger signal")
        
        # Check for logging signals
        self.check_logging_signals()
        
        # Read data and log until stopped
        if not self.should_stop_logging():
            
            # Read data
            if not self.debug:
                self.read_data()
            else:
                self.fake_read_data()
                
        # Stop
        else:
            
            self.stop_logging()
            
    
    #################################################
    # Start slot 
    #################################################
    @QtCore.pyqtSlot()
    def start(self):
        
        print("Reader received start signal")
        logthread('reader.trigger_read')
        
        # Begin blitz
        if not self.debug:
            self.begin_blitz()
            self.wait_for_refclk_started()
        
        # Track time
        self.start_time = perf_counter()
        
        # Create timer 
        self.reader_timer=QtCore.QTimer()
        self.reader_timer.setTimerType(QtCore.Qt.CoarseTimer)
        
        # Connect timer timeout with trigger signal
        self.reader_timer.timeout.connect(self.trigger_read)
            
        # Start plot timer
        self.reader_timer.start(self.capture_time * 1000 / 2)
        
        
    #################################################
    # Start logging 
    #################################################
    @QtCore.pyqtSlot()
    def start_logging(self):
        
        print("Reader received start logging signal")
        
        # Indicate that logging signal was caught
        self.start_logging_signal_caught = True
        
        
    #################################################
    # Reload logging directory
    #################################################
    @QtCore.pyqtSlot()
    def reload_parameters(self):
        
        print("Reader received reload parameters signal")
        
        if not self.logging:
            
            # Update from reader structure
            self.experiment_directory = self.reader_struct.experiment_directory
            self.logging_enabled = self.reader_struct.logging_enabled
            self.number_of_captures = self.reader_struct.number_of_captures
            self.debug = self.reader_struct.debug
            self.capture_time = self.reader_struct.capture_time
            
        else:
            
            print("logging directory cannot be changed while logging is active")
            
        
        
    #################################################
    # Stop logging 
    #################################################
    @QtCore.pyqtSlot()
    def stop_logging(self):
        
        print("Reader received stop logging signal")
        
        # Set flag
        self.stop_logging_signal_caught = True
            
        
    #################################################
    # Stop slot
    #################################################
    @QtCore.pyqtSlot()
    def stop(self):
        
        print("Reader received stop signal")
        
        # End the stream
        if not self.debug:
            self.end_blitz()
            
        # Stop timer
        self.reader_timer.stop()
        
        # Stop logging if enabled
        if self.logging:
            self.stop_logging()
            
        # Emit finished signal
        self.finished.emit(0)

