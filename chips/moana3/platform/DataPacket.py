# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:32:25 2021

@author: Dell-User
"""

from numpy import empty, flip, reshape, mean, zeros, transpose

class DataPacket:
    
    # Class variables
    __number_of_chips = 0
    __number_of_frames = 0
    __patterns_per_frame = 0
    __receive_array_size = 0
    __period = 0
    
    # Bin axis
    __chip_axis = 0
    __frame_axis = 1
    __pattern_axis = 2
    __bin_axis = 3
    
    # Constants
    __bins_per_histogram = 150
    __words_per_histogram = 300
    __bytes_per_histogram = 600

    # Mean-related variables
    __compute_mean = True
    __reduced_number_of_frames = 1

    
    
    # ====================================================
    # Initialize the data packet
    # ====================================================
    def __init__(self, number_of_chips, number_of_frames, patterns_per_frame, measurements_per_pattern, period, compute_mean=True):
        
        # Initialize class variables
        self.__number_of_chips = number_of_chips
        self.__number_of_frames = number_of_frames 
        self.__patterns_per_frame = patterns_per_frame
        self.__measurements_per_pattern = measurements_per_pattern
        self.__period = period
        
        # Calculate receive array size
        self.__receive_array_size = self.__number_of_frames*self.__patterns_per_frame*self.__number_of_chips*self.__bins_per_histogram
        
        # Create the read buffer
        self.rbuf = bytearray(self.__bytes_per_histogram*self.__number_of_frames*self.__number_of_chips*self.__patterns_per_frame)
        
        # Create the data array
        self.receive_array = empty((self.__receive_array_size), dtype=int)
        
        # Create morphed array
        if compute_mean:
            self.__morphed_array = zeros((self.__number_of_chips, self.__reduced_number_of_frames, self.__patterns_per_frame, self.__bins_per_histogram), dtype=int)
        else:
            self.__morphed_array = zeros((self.__number_of_chips, self.__number_of_frames, self.__patterns_per_frame, self.__bins_per_histogram), dtype=int)
            
        # Compute mean also sets number of frames to 1
        self.__compute_mean = compute_mean
                
    # ====================================================
    # Data property
    # ====================================================
    @property
    def data(self):
        return self.__morphed_array
    
    @data.setter
    def data(self, new_receive_array):
        self.receive_array = new_receive_array
        self.__update_data()
            

    def __update_data(self):
        
        # Reshape receive array
        a = reshape(self.receive_array, (self.__number_of_frames, self.__patterns_per_frame, self.__number_of_chips, self.__bins_per_histogram))
        
        # Flip
        a = flip(a, axis=(0,1,2,3))
        
        # Transpose
        a = transpose(a, axes=(2, 0, 1, 3))
        
        # Compute mean
        if self.__compute_mean:
            a = mean(a, axis=(1,), keepdims=True, dtype=int)
            
        # Zero out the zeroeth bin
        a = transpose(a, axes=(3,0,1,2))
        a[0].fill(0)
        a = transpose(a, axes=(1,2,3,0))
            
        # Store
        self.__morphed_array = a
        
        # if self.__compute_mean:
        #     self.__morphed_array = mean(flip(reshape(self.receive_array, (self.__number_of_chips, self.__number_of_frames, self.__patterns_per_frame, self.__bins_per_histogram)), axis=[self.__chip_axis, self.__pattern_axis, self.__bin_axis]), axis=self.__frame_axis, keepdims=True, dtype=int)
        # else:
        #     self.__morphed_array = flip(reshape(self.receive_array, (self.__number_of_chips, self.__number_of_frames, self.__patterns_per_frame, self.__bins_per_histogram)), axis=[self.__chip_axis, self.__pattern_axis, self.__bin_axis])
            
        
    # ====================================================
    # Number of chips property
    # ====================================================
    @property 
    def number_of_chips(self):
        return self.__number_of_chips
    
    @number_of_chips.setter
    def number_of_chips(self, new_number_of_chips):
        print("Cannot set number of chips after initialization")
        
        
    # ====================================================
    # Number of frames property (includes property for accessing real number of frames, disregarding any averaging)
    # ====================================================
    @property 
    def actual_number_of_frames(self):
        return self.__number_of_frames
    
    @property 
    def number_of_frames(self):
        if self.__compute_mean:
            return self.__reduced_number_of_frames
        else:
            return self.__number_of_frames
    
    @number_of_frames.setter
    def number_of_frames(self, new_number_of_frames):
        print("Cannot set number of frames after initialization")
        
        
    # ====================================================
    # Patterns per frame property
    # ====================================================
    @property 
    def patterns_per_frame(self):
        return self.__patterns_per_frame
    
    @patterns_per_frame.setter
    def patterns_per_frame(self, new_patterns_per_frame):
        print("Cannot set patterns per frame after initialization")
        
        
    # ====================================================
    # Measurements per pattern property
    # ====================================================
    @property 
    def measurements_per_pattern(self):
        return self.__measurements_per_pattern
    
    @measurements_per_pattern.setter
    def measurements_per_pattern(self, new_measurements_per_pattern):
        print("Cannot set measurements per pattern after initialization")
        
        
    # ====================================================
    # Bins per histogram property
    # ====================================================
    @property 
    def bins_per_histogram(self):
        return self.__bins_per_histogram
    
    @bins_per_histogram.setter
    def bins_per_histogram(self, new_bins_per_histogram):
        print("Cannot set bins per histogram after initialization")
        
        
    # ====================================================
    # Integration time property
    # ====================================================    
    @property
    def integration_time(self):
        if self.__compute_mean:
            return self.__measurements_per_pattern * self.__period
        else:
            return self.__measurements_per_pattern * self.__period * self.__number_of_frames
        
    @integration_time.setter
    def integration_time(self, new_integration_time):
        print("Cannot set integration time directly")
        
        
    # ====================================================
    # Capture time property
    # ====================================================    
    @property
    def capture_time(self):
        return self.__measurements_per_pattern * (self.__period / 1e9) * self.__patterns_per_frame * self.__number_of_frames
        
    @capture_time.setter
    def capture_time(self, new_capture_time):
        print("Cannot set capture time directly")
        
        
    # ====================================================
    # Period property
    # ====================================================
    @property 
    def period(self):
        return self.__period
    
    @period.setter
    def period(self, new_period):
        print("Cannot set period after initialization")
      
        
    # ====================================================
    # Receive array size property
    # ====================================================
    @property 
    def receive_array_size(self):
        return self.__receive_array_size
    
    @receive_array_size.setter
    def receive_array_size(self, new_receive_array_size):
        print("Cannot set receive array size after initialization")
        
        
if __name__ == "__main__":
    a = DataPacket(2, 2, 2)
    print(a.data[1][1][1])
        
        