# -*- coding: utf-8 -*-
"""
Created on Sun May 31 19:07:53 2020

@author: Dell-User
"""

import numpy as np


# ===========================================================
# DelayLine class to abstract from complexities of delay line
# ===========================================================
class DelayLine:
    
    # Internal clock period
    __clk_period = 10.0
            
    # Internal clock flip bit
    __clk_flip = False
    
    # List of indexes that are used to determine coarse and fine codes
    __index_list = [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, \
             32, 33, 34, 35, 36, 37, 39, 38, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, \
             56, 57, 58, 59, 60, 61, 62, 64, 65, 66, 67, 68, 69, 71, 70, 72, 73, 74, 75, 76, 77, 79, 78, 80, \
             81, 82, 83, 84, 85, 87, 86, 88, 89, 90, 91, 92, 93, 96, 97, 98, 99, 100, 101, 103, 102, 104, 105, \
             106, 107, 108, 109, 111, 110, 112, 113, 114, 115, 116, 117, 119, 118, 120, 121, 122, 123, 124, 125, 126, 127]
    
    # List of delays that result from indexes above (without clock flip bit set)
    __delay_list = [0.98, 1.19, 1.42, 1.66, 1.89, 2.12, 2.34, 2.58, 2.84, 3.06, 3.30, 3.52, 3.76, 3.84, 4.08, 4.31, 4.54, \
              4.77, 5.00, 5.23, 5.34, 5.57, 5.81, 6.04, 6.27, 6.49, 6.77, 7.00, 7.23, 7.46, 7.69, 7.91, 8.00, 8.15, \
              8.21, 8.44, 8.68, 8.90, 9.14, 9.36, 9.60, 9.68, 9.90, 10.14, 10.37, 10.60, 10.82, 11.06, 11.18, 11.41, \
              11.65, 11.88, 12.11, 12.33, 12.57, 12.62, 12.85, 13.09, 13.31, 13.55, 13.77, 13.88, 14.00, 14.10, \
              14.33, 14.57, 14.79, 15.02, 15.25, 15.33, 15.49, 15.56, 15.78, 16.02, 16.25, 16.48, 16.70, 16.87, \
              16.94, 17.08, 17.31, 17.55, 17.78, 18.00, 18.23, 18.49, 18.72, 18.96, 19.18, 19.41, 19.64, 19.75, \
              19.87, 19.97, 20.20, 20.43, 20.66, 20.89, 21.12, 21.18, 21.35, 21.41, 21.64, 21.87, 22.10, 22.33, \
              22.56, 22.72, 22.79, 22.95, 23.17, 23.41, 23.64, 23.87, 24.10, 24.33]
    
    # List of delays that result from indexes above (with clock flip bit set)
    __delay_list_clk_flip = [1.04, 1.26, 1.49, 1.73, 1.95, 2.19, 2.41, 2.65, 2.91, 3.13, 3.37, 3.59, 3.83, 3.92, 4.14, 4.38, 4.61, 4.84, \
                       5.06, 5.30, 5.41, 5.64, 5.88, 6.10, 6.34, 6.56, 6.80, 7.06, 7.30, 7.52, 7.76, 7.98, 8.06, 8.22, 8.27, 8.50, \
                       8.74, 8.97, 9.20, 9.42, 9.66, 9.74, 9.97, 10.20, 10.43, 10.66, 10.89, 11.12, 11.25, 11.47, 11.71, 11.94, 12.17, \
                       12.39, 12.63, 12.69, 12.92, 13.15, 13.38, 13.61, 13.84, 13.94, 14.07, 14.16, 14.39, 14.62, 14.85, 15.08, 15.31, \
                       15.39, 15.54, 15.61, 15.84, 16.08, 16.30, 16.53, 16.76, 16.92, 16.99, 17.13, 17.36, 17.60, 17.83, 18.06, 18.28, \
                       18.55, 18.78, 19.02, 19.25, 19.48, 19.70, 19.81, 19.94, 20.02, 20.25, 20.49, 20.72, 20.95, 21.17, 21.25, 21.41, \
                       21.47, 21.69, 21.93, 22.16, 22.39, 22.61, 22.78, 22.85, 23.00, 23.23, 23.46, 23.69, 23.92, 24.15, 24.38]
        

    
    # ===========================================================
    # Return the length of the list containing all acceptable delay line settings
    # ===========================================================
    def get_list_length(self):
        
        # Return the length
        return len(self.__index_list)

    
    # ===========================================================
    # Return the code associated with a certain delay
    # ===========================================================
    def get_code(self, delay):
        
        # Return a coarse and fine code
        if self.__clk_flip:
            return self.__get_code_clk_flip(delay)
        else:
            return self.__get_code(delay)
        
    
    # ===========================================================
    # Return the code associated with a certain delay when clock flip bit is set
    # ===========================================================
    def __get_code_clk_flip(self, delay):

        # Search for the delay setting
        matching_delay_list = np.nonzero(np.isclose(self.__delay_list_clk_flip, float(delay)))[0]
        
        # Return the index or an error code
        if bool(len(matching_delay_list)):
            
            # Return the coarse and fine code
            coarse = (self.__index_list[matching_delay_list[0]] & 0b1111000) >> 3
            fine = self.__index_list[matching_delay_list[0]] & 0b0000111 
            return coarse, fine
        
        else:
            
            # Return an error
            return None, None
        
    
    # ===========================================================
    # Return the code associated with a certain delay when clock flip bit is set
    # ===========================================================
    def __get_code(self, delay):

        # Search for the delay setting
        matching_delay_list = np.nonzero(np.isclose(self.__delay_list, float(delay)))[0]
        
        # Return the index or an error code
        if bool(len(matching_delay_list)):
            
            # Return the coarse and fine code
            coarse = (self.__index_list[matching_delay_list[0]] & 0b1111000) >> 3
            fine = self.__index_list[matching_delay_list[0]] & 0b0000111 
            return coarse, fine
        
        else:
            
            # Return an error
            return None, None
        
    
    # ===========================================================
    # Get the real delay of the delay line for an input code
    # ===========================================================
    def get_delay(self, coarse, fine):
        
        # Select a function depending on the status of the clock flip bit
        if self.__clk_flip:
            return self.__get_delay_clk_flip(coarse, fine)
        else: 
            return self.__get_delay(coarse, fine)
    
    
    # ===========================================================
    # Get the delay of the delay line without clock flip set
    # ===========================================================
    def __get_delay(self, coarse, fine):
        
        # Calculate the full delay line word
        word = (coarse << 3) + fine
        
        # Check to see that the delay line setting exists
        try:
            index = self.__index_list.index(word)
        except ValueError:
            print("Setting not found. Zero returned.")
            return 0.0
        
        # Return the exact delay
        return self.__delay_list[index]
        
    
    # ===========================================================
    # Get the delay of the delay line with clock flip set
    # ===========================================================
    def __get_delay_clk_flip(self, coarse, fine):
        
        # Calculate the full delay line word
        word = (coarse << 3) + fine
        
        # Check to see that the delay line setting exists
        try:
            index = self.__index_list.index(word)
        except ValueError: 
            print("Setting not found. Zero returned.")
            return 0.0
        
        # Return the exact delay
        return self.__delay_list_clk_flip[index] + self.__clk_period / 2.0
    
    
    # ===========================================================
    # Set the delay line
    # ===========================================================
    def set_delay_line(self, delay_ns):
        
        # Return the settings
        if self.__clk_flip:
            return self.__set_delay_line_clk_flip(delay_ns)
        else:
            return self.__set_delay_line(delay_ns)
        

    
    # ===========================================================
    # Set the delay line via a standard index value
    # ===========================================================
    def set_delay_line_by_index(self, index):
        
        # Get the word
        word = self.__index_list[index]
        
        # Calculate coarse and fine words
        coarse = (word & 0b1111000) >> 3
        fine = word & 0b111
        
        # Calculate bypass
        if (self.__clk_flip == False) and (word == 0):
            bypass = 1
        else:
            bypass = 0
        
        # Return 
        return bypass, coarse, fine

    
    # ===========================================================
    # Set the delay line without clock flip set
    # ===========================================================
    def __set_delay_line(self, delay_ns):
        
        # Default values
        bypass = 0; word = 0; coarse = 0; fine = 0
        
        # Find correct delay code
        if (delay_ns < 0.5):
            bypass = 1
        elif (delay_ns < 1.19):
            word = 0
        elif (delay_ns < 1.42):
            word = 1
        elif (delay_ns < 1.66):
            word = 2
        elif (delay_ns < 1.88):
            word = 3
        elif (delay_ns < 2.12):
            word = 4
        elif (delay_ns < 2.34):
            word = 5
        elif (delay_ns < 2.58):
            word = 6
        elif (delay_ns < 2.84):
            word = 10
        elif (delay_ns < 3.06):
            word = 11
        elif (delay_ns < 3.30):
            word = 12
        elif (delay_ns < 3.52):
            word = 13
        elif (delay_ns < 3.76):
            word = 14
        elif (delay_ns < 3.84):
            word = 16
        elif (delay_ns < 4.08):
            word = 17
        elif (delay_ns < 4.31):
            word = 18
        elif (delay_ns < 4.54):
            word = 19
        elif (delay_ns < 4.77):
            word = 20
        elif (delay_ns < 5.0):
            word = 21
        elif (delay_ns < 5.23):
            word = 22
        elif (delay_ns < 5.34):
            word = 24
        elif (delay_ns < 5.57):
            word = 25
        elif (delay_ns < 5.81):
            word = 26
        elif (delay_ns < 6.04):
            word = 27
        elif (delay_ns < 6.27):
            word = 28
        elif (delay_ns < 6.49):
            word = 29
        elif (delay_ns < 6.77):
            word = 32
        elif (delay_ns < 7.0):
            word = 33
        elif (delay_ns < 7.23):
            word = 34
        elif (delay_ns < 7.46):
            word = 35
        elif (delay_ns < 7.69):
            word = 36
        elif (delay_ns < 7.91):
            word = 37
        elif (delay_ns < 8.0):
            word = 39
        elif (delay_ns < 8.15):
            word = 38
        elif (delay_ns < 8.21):
            word = 40
        elif (delay_ns < 8.44):
            word = 41
        elif (delay_ns < 8.68):
            word = 42
        elif (delay_ns < 8.90):
            word = 43
        elif (delay_ns < 9.14):
            word = 44
        elif (delay_ns < 9.36):
            word = 45
        elif (delay_ns < 9.60):
            word = 46
        elif (delay_ns < 9.68):
            word = 48
        elif (delay_ns < 9.90):
            word = 49
        elif (delay_ns < 10.14):
            word = 50
        elif (delay_ns < 10.37):
            word = 51
        elif (delay_ns < 10.60):
            word = 52
        elif (delay_ns < 10.82):
            word = 53
        elif (delay_ns < 11.06):
            word = 54
        elif (delay_ns < 11.18):
            word = 56
        elif (delay_ns < 11.41):
            word = 57
        elif (delay_ns < 11.65):
            word = 58
        elif (delay_ns < 11.88):
            word = 59
        elif (delay_ns < 12.11):
            word = 60
        elif (delay_ns < 12.33):
            word = 61
        elif (delay_ns < 12.57):
            word = 62
        elif (delay_ns < 12.62):
            word = 64
        elif (delay_ns < 12.85):
            word = 65
        elif (delay_ns < 13.09):
            word = 66
        elif (delay_ns < 13.31):
            word = 67
        elif (delay_ns < 13.55):
            word = 68
        elif (delay_ns < 13.77):
            word = 69
        elif (delay_ns < 13.88):
            word = 71
        elif (delay_ns < 14.00):
            word = 70
        elif (delay_ns < 14.10):
            word = 72
        elif (delay_ns < 14.33):
            word = 73
        elif (delay_ns < 14.57):
            word = 74
        elif (delay_ns < 14.79):
            word = 75
        elif (delay_ns < 15.02):
            word = 76
        elif (delay_ns < 15.25):
            word = 77
        elif (delay_ns < 15.33):
            word = 79
        elif (delay_ns < 15.49):
            word = 78
        elif (delay_ns < 15.56):
            word = 80
        elif (delay_ns < 15.78):
            word = 81
        elif (delay_ns < 16.02):
            word = 82
        elif (delay_ns < 16.25):
            word = 83
        elif (delay_ns < 16.48):
            word = 84
        elif (delay_ns < 16.70):
            word = 85
        elif (delay_ns < 16.87):
            word = 87
        elif (delay_ns < 16.94):
            word = 86
        elif (delay_ns < 17.08):
            word = 88
        elif (delay_ns < 17.31):
            word = 89
        elif (delay_ns < 17.55):
            word = 90
        elif (delay_ns < 17.78):
            word = 91
        elif (delay_ns < 18.00):
            word = 92
        elif (delay_ns < 18.23):
            word = 93
        elif (delay_ns < 18.49):
            word = 96
        elif (delay_ns < 18.72):
            word = 97
        elif (delay_ns < 18.96):
            word = 98
        elif (delay_ns < 19.18):
            word = 99
        elif (delay_ns < 19.41):
            word = 100
        elif (delay_ns < 19.64):
            word = 101
        elif (delay_ns < 19.75):
            word = 103
        elif (delay_ns < 19.87):
            word = 102
        elif (delay_ns < 19.97):
            word = 104
        elif (delay_ns < 20.20):
            word = 105
        elif (delay_ns < 20.43):
            word = 106
        elif (delay_ns < 20.66):
            word = 107
        elif (delay_ns < 20.89):
            word = 108
        elif (delay_ns < 21.12):
            word = 109
        elif (delay_ns < 21.18):
            word = 111
        elif (delay_ns < 21.35):
            word = 110
        elif (delay_ns < 21.41):
            word = 112
        elif (delay_ns < 21.64):
            word = 113
        elif (delay_ns < 21.87):
            word = 114
        elif (delay_ns < 22.10):
            word = 115
        elif (delay_ns < 22.33):
            word = 116
        elif (delay_ns < 22.56):
            word = 117
        elif (delay_ns < 22.72):
            word = 119
        elif (delay_ns < 22.79):
            word = 118
        elif (delay_ns < 22.95):
            word = 120
        elif (delay_ns < 23.17):
            word = 121
        elif (delay_ns < 23.41):
            word = 122
        elif (delay_ns < 23.64):
            word = 123
        elif (delay_ns < 23.87):
            word = 124
        elif (delay_ns < 24.10):
            word = 125
        elif (delay_ns < 24.33):
            word = 126
        else:
            word = 127

        # Calculate coarse and fine words
        coarse = (word & 0b1111000) >> 3
        fine = word & 0b111
        
        # Return 
        return bypass, coarse, fine
    
    
    # ===========================================================
    # Set the delay line with clock flip set
    # ===========================================================
    def __set_delay_line_clk_flip(self, delay_ns):
        
        # Default values
        # Bypass not available with clk_flip enabled
        bypass = 0; word = 0; coarse = 0; fine = 0
        
        # Subtract half the clock period
        delay_ns_minus_half_period = delay_ns - self.__clk_period / 2.0
        
        # Find correct delay code
        if (delay_ns_minus_half_period < 1.26):
            word = 0
        elif (delay_ns_minus_half_period < 1.49):
            word = 1
        elif (delay_ns_minus_half_period < 1.73):
            word = 2
        elif (delay_ns_minus_half_period < 1.95):
            word = 3
        elif (delay_ns_minus_half_period < 2.19):
            word = 4
        elif (delay_ns_minus_half_period < 2.41):
            word = 5
        elif (delay_ns_minus_half_period < 2.65):
            word = 6
        elif (delay_ns_minus_half_period < 2.91):
            word = 10
        elif (delay_ns_minus_half_period < 3.13):
            word = 11
        elif (delay_ns_minus_half_period < 3.37):
            word = 12
        elif (delay_ns_minus_half_period < 3.59):
            word = 13
        elif (delay_ns_minus_half_period < 3.83):
            word = 14
        elif (delay_ns_minus_half_period < 3.92):
            word = 16
        elif (delay_ns_minus_half_period < 4.14):
            word = 17
        elif (delay_ns_minus_half_period < 4.38):
            word = 18
        elif (delay_ns_minus_half_period < 4.61):
            word = 19
        elif (delay_ns_minus_half_period < 4.84):
            word = 20
        elif (delay_ns_minus_half_period < 5.06):
            word = 21
        elif (delay_ns_minus_half_period < 5.30):
            word = 22
        elif (delay_ns_minus_half_period < 5.41):
            word = 24
        elif (delay_ns_minus_half_period < 5.64):
            word = 25
        elif (delay_ns_minus_half_period < 5.88):
            word = 26
        elif (delay_ns_minus_half_period < 6.10):
            word = 27
        elif (delay_ns_minus_half_period < 6.34):
            word = 28
        elif (delay_ns_minus_half_period < 6.56):
            word = 29
        elif (delay_ns_minus_half_period < 6.80):
            word = 32
        elif (delay_ns_minus_half_period < 7.06):
            word = 33
        elif (delay_ns_minus_half_period < 7.30):
            word = 34
        elif (delay_ns_minus_half_period < 7.52):
            word = 35
        elif (delay_ns_minus_half_period < 7.76):
            word = 36
        elif (delay_ns_minus_half_period < 7.98):
            word = 37
        elif (delay_ns_minus_half_period < 8.06):
            word = 39
        elif (delay_ns_minus_half_period < 8.22):
            word = 38
        elif (delay_ns_minus_half_period < 8.27):
            word = 40
        elif (delay_ns_minus_half_period < 8.50):
            word = 41
        elif (delay_ns_minus_half_period < 8.74):
            word = 42
        elif (delay_ns_minus_half_period < 8.97):
            word = 43
        elif (delay_ns_minus_half_period < 9.20):
            word = 44
        elif (delay_ns_minus_half_period < 9.42):
            word = 45
        elif (delay_ns_minus_half_period < 9.66):
            word = 46
        elif (delay_ns_minus_half_period < 9.74):
            word = 48
        elif (delay_ns_minus_half_period < 9.97):
            word = 49
        elif (delay_ns_minus_half_period < 10.20):
            word = 50
        elif (delay_ns_minus_half_period < 10.43):
            word = 51
        elif (delay_ns_minus_half_period < 10.66):
            word = 52
        elif (delay_ns_minus_half_period < 10.89):
            word = 53
        elif (delay_ns_minus_half_period < 11.12):
            word = 54
        elif (delay_ns_minus_half_period < 11.25):
            word = 56
        elif (delay_ns_minus_half_period < 11.47):
            word = 57
        elif (delay_ns_minus_half_period < 11.71):
            word = 58
        elif (delay_ns_minus_half_period < 11.94):
            word = 59
        elif (delay_ns_minus_half_period < 12.17):
            word = 60
        elif (delay_ns_minus_half_period < 12.39):
            word = 61
        elif (delay_ns_minus_half_period < 12.63):
            word = 62
        elif (delay_ns_minus_half_period < 12.69):
            word = 64
        elif (delay_ns_minus_half_period < 12.92):
            word = 65
        elif (delay_ns_minus_half_period < 13.15):
            word = 66
        elif (delay_ns_minus_half_period < 13.38):
            word = 67
        elif (delay_ns_minus_half_period < 13.61):
            word = 68
        elif (delay_ns_minus_half_period < 13.84):
            word = 69
        elif (delay_ns_minus_half_period < 13.94):
            word = 71
        elif (delay_ns_minus_half_period < 14.07):
            word = 70
        elif (delay_ns_minus_half_period < 14.16):
            word = 72
        elif (delay_ns_minus_half_period < 14.39):
            word = 73
        elif (delay_ns_minus_half_period < 14.62):
            word = 74
        elif (delay_ns_minus_half_period < 14.85):
            word = 75
        elif (delay_ns_minus_half_period < 15.08):
            word = 76
        elif (delay_ns_minus_half_period < 15.31):
            word = 77
        elif (delay_ns_minus_half_period < 15.39):
            word = 79
        elif (delay_ns_minus_half_period < 15.54):
            word = 78
        elif (delay_ns_minus_half_period < 15.61):
            word = 80
        elif (delay_ns_minus_half_period < 15.84):
            word = 81
        elif (delay_ns_minus_half_period < 16.08):
            word = 82
        elif (delay_ns_minus_half_period < 16.30):
            word = 83
        elif (delay_ns_minus_half_period < 16.53):
            word = 84
        elif (delay_ns_minus_half_period < 16.76):
            word = 85
        elif (delay_ns_minus_half_period < 16.92):
            word = 87
        elif (delay_ns_minus_half_period < 16.99):
            word = 86
        elif (delay_ns_minus_half_period < 17.13):
            word = 88
        elif (delay_ns_minus_half_period < 17.36):
            word = 89
        elif (delay_ns_minus_half_period < 17.60):
            word = 90
        elif (delay_ns_minus_half_period < 17.83):
            word = 91
        elif (delay_ns_minus_half_period < 18.06):
            word = 92
        elif (delay_ns_minus_half_period < 18.28):
            word = 93
        elif (delay_ns_minus_half_period < 18.55):
            word = 96
        elif (delay_ns_minus_half_period < 18.78):
            word = 97
        elif (delay_ns_minus_half_period < 19.02):
            word = 98
        elif (delay_ns_minus_half_period < 19.25):
            word = 99
        elif (delay_ns_minus_half_period < 19.48):
            word = 100
        elif (delay_ns_minus_half_period < 19.70):
            word = 101
        elif (delay_ns_minus_half_period < 19.81):
            word = 103
        elif (delay_ns_minus_half_period < 19.94):
            word = 102
        elif (delay_ns_minus_half_period < 20.02):
            word = 104
        elif (delay_ns_minus_half_period < 20.25):
            word = 105
        elif (delay_ns_minus_half_period < 20.49):
            word = 106
        elif (delay_ns_minus_half_period < 20.72):
            word = 107
        elif (delay_ns_minus_half_period < 20.95):
            word = 108
        elif (delay_ns_minus_half_period < 21.17):
            word = 109
        elif (delay_ns_minus_half_period < 21.25):
            word = 111
        elif (delay_ns_minus_half_period < 21.41):
            word = 110
        elif (delay_ns_minus_half_period < 21.47):
            word = 112
        elif (delay_ns_minus_half_period < 21.69):
            word = 113
        elif (delay_ns_minus_half_period < 21.93):
            word = 114
        elif (delay_ns_minus_half_period < 22.16):
            word = 115
        elif (delay_ns_minus_half_period < 22.39):
            word = 116
        elif (delay_ns_minus_half_period < 22.61):
            word = 117
        elif (delay_ns_minus_half_period < 22.78):
            word = 119
        elif (delay_ns_minus_half_period < 22.85):
            word = 118
        elif (delay_ns_minus_half_period < 23.00):
            word = 120
        elif (delay_ns_minus_half_period < 23.23):
            word = 121
        elif (delay_ns_minus_half_period < 23.46):
            word = 122
        elif (delay_ns_minus_half_period < 23.69):
            word = 123
        elif (delay_ns_minus_half_period < 23.92):
            word = 124
        elif (delay_ns_minus_half_period < 24.15):
            word = 125
        elif (delay_ns_minus_half_period < 24.38):
            word = 126
        else:
            word = 127

        # Calculate coarse and fine words
        coarse = (word & 0b1111000) >> 3
        fine = word & 0b111
        
        # Return 
        return bypass, coarse, fine
    
    
    # ===========================================================
    # Increment the delay line
    # Clock flip doesn't matter here because lists are the same
    # ===========================================================
    def delay_line_increment(self, coarse, fine):

        # Calculate the word
        word = (coarse << 3) + fine
        
        # Try to find the value in the list
        try:
            index = self.__index_list.index(word)
        except ValueError: 
            print("Setting not found. Same setting returned.")
            return coarse, fine
        
        # Return the new word
        if (index + 1) >= len(self.__index_list):
            print("Delay line at maximum delay setting")
            return coarse, fine
        else:
            new_word = self.__index_list[index+1]
            new_coarse = (new_word & 0b1111000) >> 3
            new_fine = new_word & 0b111
        
        # Return
        return new_coarse, new_fine
    
    
    # ===========================================================
    # Decrement the delay line
    # Clock flip doesn't matter here because lists are the same
    # ===========================================================
    def delay_line_decrement(self, coarse, fine):

        # Calculate the word
        word = (coarse << 3) + fine
        
        # Try to find the value in the list
        try:
            index = self.__index_list.index(word)
        except ValueError: 
            print("Setting not found. Same setting returned.")
            return coarse, fine
        
        # Return the new word
        if (index - 1) < 0:
            print("Delay line at minimum delay setting")
            return coarse, fine
        else:
            new_word = self.__index_list[index-1]
            new_coarse = (new_word & 0b1111000) >> 3
            new_fine = new_word & 0b111
        
        # Return
        return new_coarse, new_fine
    
    
    # ===========================================================
    # Set the value of the clock flip bit
    # ===========================================================
    def set_clk_flip(self, boolean):
        
        # Set internal clock flip bit
        self.__clk_flip = bool(boolean)
        
    
    # ===========================================================
    # Return the current value of __clk_flip
    # ===========================================================
    def get_clk_flip(self):
        
        # Return internal clock flip bit
        return self.__clk_flip
    
    
    # ===========================================================
    # Set the value of the clock period
    # ===========================================================
    def set_clk_period(self, period):
        
        # Set internal clock flip bit
        self.__clk_period = float(period)
        
    
    # ===========================================================
    # Return the current value of __clk_period
    # ===========================================================
    def get_clk_period(self):
        
        # Return internal clock period
        return self.__clk_period
    
    # ===========================================================
    # Return the longest delay available from the delay line
    # ===========================================================
    def get_longest_delay(self):
        
        # Return the longest delay
        if self.__clk_flip:
            return (self.__delay_list_clk_flip[self.get_list_length()-1] + self.__clk_period / 2.0)
        else:
            return self.__delay_list[self.get_list_length()-1]
    
    
    
    
    
    