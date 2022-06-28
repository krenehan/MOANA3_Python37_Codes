# -*- coding: utf-8 -*-
"""
Created on Sun May 31 19:07:53 2020

@author: Dell-User
"""

import numpy as np
from delay_charac import *
from delay_charac_clkflip import *
# ===========================================================
# DelayLine class to abstract from complexities of delay line
# ===========================================================
class DelayLine:
    
    # Internal clock period
    __clk_period = 10.0
            
    # Internal clock flip bit
    __clk_flip = False
    
    # List of indexes that are used to determine coarse and fine codes
    __index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, \
             30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, \
             56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, \
             81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, \
             106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, \
             128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, \
             150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, \
             172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, \
             194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, \
             216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, \
             238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254]
    
    # List of delays that result from indexes above (without clock flip bit set)
    __delay_list = get_step()
    
    # List of delays that result from indexes above (with clock flip bit set)
    __delay_list_clk_flip = get_step_clkflip()

    
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
        if (delay_ns < 0.01):
            bypass = 1
        elif (delay_ns < 0.039):
            word = 0
        elif (delay_ns < 0.097):
            word = 1
        elif (delay_ns < 0.139):
            word = 2
        elif (delay_ns < 0.198):
            word = 3
        elif (delay_ns < 0.238):
            word = 4
        elif (delay_ns < 0.307):
            word = 5
        elif (delay_ns < 0.348):
            word = 6
        elif (delay_ns < 0.405):
            word = 7
        elif (delay_ns < 0.45):
            word = 8
        elif (delay_ns < 0.528):
            word = 9
        elif (delay_ns < 0.566):
            word = 10            
        elif (delay_ns < 0.631):
            word = 11
        elif (delay_ns < 0.673):
            word = 12
        elif (delay_ns < 0.73):
            word = 13
        elif (delay_ns < 0.774):
            word = 14
        elif (delay_ns < 0.872):
            word = 15           
        elif (delay_ns < 0.921):
            word = 16
        elif (delay_ns < 0.981):
            word = 17
        elif (delay_ns < 1.028):
            word = 18
        elif (delay_ns < 1.088):
            word = 19
        elif (delay_ns < 1.124):
            word = 20
        elif (delay_ns < 1.19):
            word = 21
        elif (delay_ns < 1.234):
            word = 22
        elif (delay_ns < 1.285):
            word = 23
        elif (delay_ns < 1.326):
            word = 24         
        elif (delay_ns < 1.406):
            word = 25
        elif (delay_ns < 1.447):
            word = 26
        elif (delay_ns < 1.514):
            word = 27
        elif (delay_ns < 1.555):
            word = 28
        elif (delay_ns < 1.622):
            word = 29
        elif (delay_ns < 1.78):
            word = 31
        elif (delay_ns < 1.817):
            word = 32            
        elif (delay_ns < 1.886):
            word = 33
        elif (delay_ns < 1.931):
            word = 34
        elif (delay_ns < 2.000):
            word = 35
        elif (delay_ns < 2.043):
            word = 36
        elif (delay_ns < 2.108):
            word = 37
        elif (delay_ns < 2.144):
            word = 38
        elif (delay_ns < 2.197):
            word = 39
        elif (delay_ns < 2.226):
            word = 40
        elif (delay_ns < 2.296):
            word = 41
        elif (delay_ns < 2.343):
            word = 42
        elif (delay_ns < 2.44):
            word = 43
        elif (delay_ns < 2.449):
            word = 44
        elif (delay_ns < 2.518):
            word = 45
        elif (delay_ns < 2.563):
            word = 46
        elif (delay_ns < 2.681):
            word = 47
        elif (delay_ns < 2.715):
            word = 48
        elif (delay_ns < 2.779):
            word = 49
        elif (delay_ns < 2.826):
            word = 50
        elif (delay_ns < 2.888):
            word = 51
        elif (delay_ns < 2.93):
            word = 52
        elif (delay_ns < 3.003):
            word = 53
        elif (delay_ns < 3.042):
            word = 54
        elif (delay_ns < 3.104):
            word = 55
        elif (delay_ns < 3.142):
            word = 56
        elif (delay_ns < 3.215):
            word = 57
        elif (delay_ns < 3.254):
            word = 58
        elif (delay_ns < 3.311):
            word = 59
        elif (delay_ns < 3.366):
            word = 60
        elif (delay_ns < 3.43):
            word = 61
        elif (delay_ns < 3.474):
            word = 62
        elif (delay_ns < 3.599):
            word = 63
        elif (delay_ns < 3.638):
            word = 64
        elif (delay_ns < 3.701):
            word = 65
        elif (delay_ns < 3.741):
            word = 66
        elif (delay_ns < 3.801):
            word = 67
        elif (delay_ns < 3.845):
            word = 68
        elif (delay_ns < 3.905):
            word = 69
        elif (delay_ns < 3.949):
            word = 70
        elif (delay_ns < 4.01):
            word = 71
        elif (delay_ns < 4.055):
            word = 72
        elif (delay_ns < 4.128):
            word = 73
        elif (delay_ns < 4.173):
            word = 74
        elif (delay_ns < 4.232):
            word = 75
        elif (delay_ns < 4.273):
            word = 76
        elif (delay_ns < 4.331):
            word = 77
        elif (delay_ns < 4.372):
            word = 78
        elif (delay_ns < 4.492):
            word = 79
        elif (delay_ns < 4.523):
            word = 80
        elif (delay_ns < 4.593):
            word = 81
        elif (delay_ns < 4.636):
            word = 82
        elif (delay_ns < 4.699):
            word = 83
        elif (delay_ns < 4.739):
            word = 84
        elif (delay_ns < 4.801):
            word = 85
        elif (delay_ns < 4.844):
            word = 86
        elif (delay_ns < 4.899):
            word = 87
        elif (delay_ns < 4.939):
            word = 88
        elif (delay_ns < 5.021):
            word = 89
        elif (delay_ns < 5.057):
            word = 90
        elif (delay_ns < 5.126):
            word = 91
        elif (delay_ns < 5.17):
            word = 92
        elif (delay_ns < 5.234):
            word = 93
        elif (delay_ns < 5.273):
            word = 94
        elif (delay_ns < 5.395):
            word = 95
        elif (delay_ns < 5.432):
            word = 96
        elif (delay_ns < 5.496):
            word = 97
        elif (delay_ns < 5.537):
            word = 98
        elif (delay_ns < 5.609):
            word = 99
        elif (delay_ns < 5.725):
            word = 100
        elif (delay_ns < 5.797):
            word = 101
        elif (delay_ns < 5.836):
            word = 102
        elif (delay_ns < 5.885):
            word = 103
        elif (delay_ns < 5.919):
            word = 104
        elif (delay_ns < 5.996):
            word = 105
        elif (delay_ns < 6.041):
            word = 106
        elif (delay_ns < 6.104):
            word = 107
        elif (delay_ns < 6.15):
            word = 108
        elif (delay_ns < 6.224):
            word = 109
        elif (delay_ns < 6.263):
            word = 110
        elif (delay_ns < 6.383):
            word = 111
        elif (delay_ns < 6.415):
            word = 112
        elif (delay_ns < 6.479):
            word = 113
        elif (delay_ns < 6.52):
            word = 114
        elif (delay_ns < 6.584):
            word = 115
        elif (delay_ns < 6.628):
            word = 116
        elif (delay_ns < 6.698):
            word = 117
        elif (delay_ns < 6.738):
            word = 118
        elif (delay_ns < 6.799):
            word = 119
        elif (delay_ns < 6.832):
            word = 120
        elif (delay_ns < 6.908):
            word = 121
        elif (delay_ns < 6.946):
            word = 122
        elif (delay_ns < 7.005):
            word = 123
        elif (delay_ns < 7.047):
            word = 124
        elif (delay_ns < 7.112):
            word = 125
        elif (delay_ns < 7.153):
            word = 126
        elif (delay_ns < 7.262):
            word = 127
        elif (delay_ns < 7.299 ):
            word = 128
        elif (delay_ns < 7.369):
            word = 129
        elif (delay_ns < 7.406):
            word = 130
        elif (delay_ns < 7.472):
            word = 131
        elif (delay_ns < 7.505):
            word = 132
        elif (delay_ns < 7.577):
            word = 133
        elif (delay_ns < 7.614):
            word = 134
        elif (delay_ns < 7.673):
            word = 135
        elif (delay_ns < 7.715):
            word = 136
        elif (delay_ns < 7.795):
            word = 137
        elif (delay_ns < 7.833):
            word = 138
        elif (delay_ns < 7.902):
            word = 139
        elif (delay_ns < 7.936):
            word = 140
        elif (delay_ns < 8.004):
            word = 141
        elif (delay_ns < 8.037):
            word = 142
        elif (delay_ns < 8.162):
            word = 143
        elif (delay_ns < 8.191 ):
            word = 144
        elif (delay_ns < 8.269):
            word = 145
        elif (delay_ns < 8.303):
            word = 146
        elif (delay_ns < 8.377):
            word = 147
        elif (delay_ns < 8.413):
            word = 148
        elif (delay_ns < 8.478):
            word = 149
        elif (delay_ns < 8.513):
            word = 150
        elif (delay_ns < 8.572):
            word = 151
        elif (delay_ns < 8.606):
            word = 152
        elif (delay_ns < 8.682):
            word = 153
        elif (delay_ns < 8.722):
            word = 154
        elif (delay_ns < 8.796):
            word = 155
        elif (delay_ns < 8.83):
            word = 156
        elif (delay_ns < 8.905):
            word = 157
        elif (delay_ns < 8.938):
            word = 158
        elif (delay_ns < 9.07):
            word = 159
        elif (delay_ns < 9.104):
            word = 160
        elif (delay_ns < 9.172):
            word = 161
        elif (delay_ns < 9.211):
            word = 162
        elif (delay_ns < 9.29):
            word = 163
        elif (delay_ns < 9.327):
            word = 164
        elif (delay_ns < 9.394):
            word = 165
        elif (delay_ns < 9.433):
            word = 166
        elif (delay_ns < 9.493):
            word = 167
        elif (delay_ns < 9.531):
            word = 168
        elif (delay_ns < 9.612):
            word = 169
        elif (delay_ns < 9.643):
            word = 170
        elif (delay_ns < 9.71):
            word = 171
        elif (delay_ns < 9.75):
            word = 172
        elif (delay_ns < 9.822):
            word = 173
        elif (delay_ns < 9.861):
            word = 174
        elif (delay_ns < 10.00):
            word = 175
        elif (delay_ns < 10.032):
            word = 176
        elif (delay_ns < 10.103):
            word = 177
        elif (delay_ns < 10.136):
            word = 178
        elif (delay_ns < 10.208):
            word = 179
        elif (delay_ns < 10.253):
            word = 180
        elif (delay_ns < 10.329):
            word = 181
        elif (delay_ns < 10.365):
            word = 182
        elif (delay_ns < 10.43):
            word = 183
        elif (delay_ns < 10.468):
            word = 184
        elif (delay_ns < 10.542):
            word = 185
        elif (delay_ns < 10.577):
            word = 186
        elif (delay_ns < 10.645):
            word = 187
        elif (delay_ns < 10.681):
            word = 188  
        elif (delay_ns < 10.752):
            word = 189
        elif (delay_ns < 10.786):
            word = 190
        elif (delay_ns < 10.884):
            word = 191
        elif (delay_ns < 10.926):
            word = 192
        elif (delay_ns < 10.994):
            word = 193
        elif (delay_ns < 11.027):
            word = 194 
        elif (delay_ns < 11.09):
            word = 195
        elif (delay_ns < 11.124):
            word = 196
        elif (delay_ns < 11.201):
            word = 197
        elif (delay_ns < 11.23):
            word = 198
        elif (delay_ns < 11.29):
            word = 199
        elif (delay_ns < 11.311):
            word = 200
        elif (delay_ns < 11.401):
            word = 201
        elif (delay_ns < 11.437):
            word = 202
        elif (delay_ns < 11.51):
            word = 203
        elif (delay_ns < 11.544):
            word = 204
        elif (delay_ns < 11.612):
            word = 205           
        elif (delay_ns < 11.644):
            word = 206
        elif (delay_ns < 11.771):
            word = 207
        elif (delay_ns < 11.803):
            word = 208
        elif (delay_ns < 11.873):
            word = 209
        elif (delay_ns < 11.904):
            word = 210           
        elif (delay_ns < 11.981):
            word = 211
        elif (delay_ns < 12.014):
            word = 212
        elif (delay_ns < 12.086):
            word = 213
        elif (delay_ns < 12.119):
            word = 214
        elif (delay_ns < 12.178):
            word = 215
        elif (delay_ns < 12.208):
            word = 216
        elif (delay_ns < 12.294):
            word = 217
        elif (delay_ns < 12.326):
            word = 218
        elif (delay_ns < 12.406):
            word = 219        
        elif (delay_ns < 12.429):
            word = 220
        elif (delay_ns < 12.507):
            word = 221
        elif (delay_ns < 12.539):
            word = 222
        elif (delay_ns < 12.657):
            word = 223
        elif (delay_ns < 12.689):
            word = 224
        elif (delay_ns < 12.758):
            word = 225
        elif (delay_ns < 12.786):
            word = 226            
        elif (delay_ns < 12.868):
            word = 227
        elif (delay_ns < 12.901):
            word = 228
        elif (delay_ns < 12.987):
            word = 229
        elif (delay_ns < 13.013):
            word = 230
        elif (delay_ns < 13.077):
            word = 231
        elif (delay_ns < 13.111):
            word = 232
        elif (delay_ns < 13.192):
            word = 233
        elif (delay_ns < 13.223):
            word = 234
        elif (delay_ns < 13.3):
            word = 235
        elif (delay_ns < 13.328):
            word = 236
        elif (delay_ns < 13.41):
            word = 237
        elif (delay_ns < 13.438):
            word = 238
        elif (delay_ns < 13.587):
            word = 239
        elif (delay_ns < 13.594):
            word = 240
        elif (delay_ns < 13.667):
            word = 241
        elif (delay_ns < 13.696):
            word = 242
        elif (delay_ns < 13.773):
            word = 243
        elif (delay_ns < 13.804):
            word = 244
        elif (delay_ns < 13.883):
            word = 245
        elif (delay_ns < 13.905):
            word = 246
        elif (delay_ns < 13.98):
            word = 247
        elif (delay_ns < 14.011):
            word = 248
        elif (delay_ns < 14.097):
            word = 249
        elif (delay_ns < 14.127):
            word = 250
        elif (delay_ns < 14.199):
            word = 251
        elif (delay_ns < 14.229):
            word = 252
        elif (delay_ns < 14.307):
            word = 253         
        else:
            word = 254

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
        if (delay_ns_minus_half_period < 0.044):
            word = 0
        elif (delay_ns_minus_half_period <0.106 ):
            word = 1
        elif (delay_ns_minus_half_period < 0.156):
            word = 2
        elif (delay_ns_minus_half_period < 0.22):
            word = 3
        elif (delay_ns_minus_half_period < 0.262):
            word = 4
        elif (delay_ns_minus_half_period < 0.33):
            word = 5
        elif (delay_ns_minus_half_period < 0.366):
            word = 6
        elif (delay_ns_minus_half_period < 0.424):
            word = 7
        elif (delay_ns_minus_half_period < 0.465):
            word = 8
        elif (delay_ns_minus_half_period < 0.533):
            word = 9
        elif (delay_ns_minus_half_period < 0.584):
            word = 10
        elif (delay_ns_minus_half_period < 0.642):
            word = 11
        elif (delay_ns_minus_half_period < 0.684):
            word = 12
        elif (delay_ns_minus_half_period < 0.747):
            word = 13
        elif (delay_ns_minus_half_period < 0.796):
            word = 14
        elif (delay_ns_minus_half_period < 0.893):
            word = 15
        elif (delay_ns_minus_half_period < 0.935):
            word = 16
        elif (delay_ns_minus_half_period < 0.995):
            word = 17
        elif (delay_ns_minus_half_period < 1.038):
            word = 18
        elif (delay_ns_minus_half_period < 1.106):
            word = 19
        elif (delay_ns_minus_half_period < 1.152):
            word = 20
        elif (delay_ns_minus_half_period < 1.214):
            word = 21
        elif (delay_ns_minus_half_period < 1.257):
            word = 22
        elif (delay_ns_minus_half_period < 1.319):
            word = 23
        elif (delay_ns_minus_half_period < 1.36):
            word = 24
        elif (delay_ns_minus_half_period < 1.437):
            word = 25
        elif (delay_ns_minus_half_period < 1.477):
            word = 26
        elif (delay_ns_minus_half_period < 1.54):
            word = 27
        elif (delay_ns_minus_half_period < 1.579):
            word = 28
        elif (delay_ns_minus_half_period < 1.639):
            word = 29
        elif (delay_ns_minus_half_period < 1.689):
            word = 30
        elif (delay_ns_minus_half_period < 1.806):
            word = 31
        elif (delay_ns_minus_half_period < 1.852):
            word = 32
        elif (delay_ns_minus_half_period < 1.915):
            word = 33
        elif (delay_ns_minus_half_period < 1.952):
            word = 34
        elif (delay_ns_minus_half_period < 2.022):
            word = 35
        elif (delay_ns_minus_half_period < 2.063):
            word = 36
        elif (delay_ns_minus_half_period < 2.128):
            word = 37
        elif (delay_ns_minus_half_period < 2.176):
            word = 38
        elif (delay_ns_minus_half_period < 2.232):
            word = 39
        elif (delay_ns_minus_half_period < 2.276):
            word = 40
        elif (delay_ns_minus_half_period < 2.339):
            word = 41
        elif (delay_ns_minus_half_period < 2.389):
            word = 42
        elif (delay_ns_minus_half_period < 2.45):
            word = 43
        elif (delay_ns_minus_half_period < 2.491):
            word = 44
        elif (delay_ns_minus_half_period < 2.553):
            word = 45
        elif (delay_ns_minus_half_period < 2.597):
            word = 46
        elif (delay_ns_minus_half_period < 2.712):
            word = 47
        elif (delay_ns_minus_half_period < 2.757):
            word = 48
        elif (delay_ns_minus_half_period < 2.813):
            word = 49
        elif (delay_ns_minus_half_period < 2.856):
            word = 50
        elif (delay_ns_minus_half_period < 2.919):
            word = 51
        elif (delay_ns_minus_half_period < 2.968):
            word = 52
        elif (delay_ns_minus_half_period < 3.031):
            word = 53
        elif (delay_ns_minus_half_period < 3.075):
            word = 54
        elif (delay_ns_minus_half_period < 3.128):
            word = 55
        elif (delay_ns_minus_half_period < 3.18):
            word = 56
        elif (delay_ns_minus_half_period < 3.249):
            word = 57
        elif (delay_ns_minus_half_period < 3.287):
            word = 58
        elif (delay_ns_minus_half_period < 3.357):
            word = 59
        elif (delay_ns_minus_half_period < 3.398):
            word = 60
        elif (delay_ns_minus_half_period < 3.468):
            word = 61
        elif (delay_ns_minus_half_period < 3.51):
            word = 62
        elif (delay_ns_minus_half_period < 3.625):
            word = 63
        elif (delay_ns_minus_half_period < 3.667):
            word = 64
        elif (delay_ns_minus_half_period < 3.719):
            word = 65
        elif (delay_ns_minus_half_period < 3.771):
            word = 66
        elif (delay_ns_minus_half_period < 3.83):
            word = 67
        elif (delay_ns_minus_half_period < 3.876):
            word = 68
        elif (delay_ns_minus_half_period < 3.943):
            word = 69
        elif (delay_ns_minus_half_period < 3.989):
            word = 70
        elif (delay_ns_minus_half_period < 4.043):
            word = 71
        elif (delay_ns_minus_half_period < 4.084):
            word = 72
        elif (delay_ns_minus_half_period < 4.162):
            word = 73
        elif (delay_ns_minus_half_period < 4.206):
            word = 74
        elif (delay_ns_minus_half_period < 4.263):
            word = 75
        elif (delay_ns_minus_half_period < 4.31):
            word = 76
        elif (delay_ns_minus_half_period < 4.377):
            word = 77
        elif (delay_ns_minus_half_period < 4.415):
            word = 78
        elif (delay_ns_minus_half_period < 4.536):
            word = 79
        elif (delay_ns_minus_half_period < 4.574):
            word = 80
        elif (delay_ns_minus_half_period < 4.637):
            word = 81
        elif (delay_ns_minus_half_period < 4.682):
            word = 82
        elif (delay_ns_minus_half_period < 4.744):
            word = 83
        elif (delay_ns_minus_half_period < 4.788):
            word = 84
        elif (delay_ns_minus_half_period < 4.855):
            word = 85
        elif (delay_ns_minus_half_period < 4.898):
            word = 86
        elif (delay_ns_minus_half_period < 4.955):
            word = 87
        elif (delay_ns_minus_half_period < 5.001):
            word = 88
        elif (delay_ns_minus_half_period < 5.072):
            word = 89
        elif (delay_ns_minus_half_period < 5.108):
            word = 90
        elif (delay_ns_minus_half_period < 5.179):
            word = 91
        elif (delay_ns_minus_half_period < 5.215):
            word = 92
        elif (delay_ns_minus_half_period < 5.279):
            word = 93
        elif (delay_ns_minus_half_period < 5.323):
            word = 94
        elif (delay_ns_minus_half_period < 5.448):
            word = 95
        elif (delay_ns_minus_half_period < 5.493):
            word = 96
        elif (delay_ns_minus_half_period < 5.554):
            word = 97
        elif (delay_ns_minus_half_period < 5.6):
            word = 98
        elif (delay_ns_minus_half_period < 5.66):
            word = 99
        elif (delay_ns_minus_half_period < 5.715):
            word = 100
        elif (delay_ns_minus_half_period < 5.778):
            word = 101
        elif (delay_ns_minus_half_period < 5.817):
            word = 102
        elif (delay_ns_minus_half_period < 5.87):
            word = 103
        elif (delay_ns_minus_half_period < 5.91):
            word = 104
        elif (delay_ns_minus_half_period < 5.984):
            word = 105
        elif (delay_ns_minus_half_period < 6.027):
            word = 106
        elif (delay_ns_minus_half_period < 6.093):
            word = 107
        elif (delay_ns_minus_half_period < 6.124):
            word = 108
        elif (delay_ns_minus_half_period < 6.192):
            word = 109
        elif (delay_ns_minus_half_period < 6.234):
            word = 110
        elif (delay_ns_minus_half_period < 6.35):
            word = 111
        elif (delay_ns_minus_half_period < 6.398):
            word = 112
        elif (delay_ns_minus_half_period < 6.461):
            word = 113
        elif (delay_ns_minus_half_period < 6.507):
            word = 114
        elif (delay_ns_minus_half_period < 6.574):
            word = 115
        elif (delay_ns_minus_half_period < 6.601):
            word = 116
        elif (delay_ns_minus_half_period < 6.68):
            word = 117
        elif (delay_ns_minus_half_period < 6.709):
            word = 118
        elif (delay_ns_minus_half_period < 6.775):
            word = 119
        elif (delay_ns_minus_half_period < 6.807):
            word = 120
        elif (delay_ns_minus_half_period < 6.884):
            word = 121
        elif (delay_ns_minus_half_period < 6.927):
            word = 122
        elif (delay_ns_minus_half_period < 6.993):
            word = 123
        elif (delay_ns_minus_half_period < 7.037):
            word = 124
        elif (delay_ns_minus_half_period < 7.103):
            word = 125
        elif (delay_ns_minus_half_period < 7.139):
            word = 126
        elif (delay_ns_minus_half_period < 7.247):
            word = 127
        elif (delay_ns_minus_half_period < 7.285):
            word = 128
        elif (delay_ns_minus_half_period < 7.344):
            word = 129
        elif (delay_ns_minus_half_period < 7.38):
            word = 130
        elif (delay_ns_minus_half_period < 7.45):
            word = 131
        elif (delay_ns_minus_half_period < 7.49):
            word = 132
        elif (delay_ns_minus_half_period < 7.557):
            word = 133
        elif (delay_ns_minus_half_period < 7.599):
            word = 134
        elif (delay_ns_minus_half_period < 7.657):
            word = 135
        elif (delay_ns_minus_half_period < 7.696):
            word = 136
        elif (delay_ns_minus_half_period < 7.769):
            word = 137
        elif (delay_ns_minus_half_period < 7.805):
            word = 138
        elif (delay_ns_minus_half_period < 7.876):
            word = 139    
        elif (delay_ns_minus_half_period < 7.918):
            word = 140
        elif (delay_ns_minus_half_period < 7.988):
            word = 141
        elif (delay_ns_minus_half_period < 8.025):
            word = 142
        elif (delay_ns_minus_half_period < 8.151):
            word = 143
        elif (delay_ns_minus_half_period < 8.187):
            word = 144
        elif (delay_ns_minus_half_period < 8.252):
            word = 145
        elif (delay_ns_minus_half_period < 8.299):
            word = 146
        elif (delay_ns_minus_half_period < 8.363):
            word = 147
        elif (delay_ns_minus_half_period < 8.399):
            word = 148
        elif (delay_ns_minus_half_period < 8.467):
            word = 149
        elif (delay_ns_minus_half_period < 8.505):
            word = 150
        elif (delay_ns_minus_half_period < 8.569):
            word = 151
        elif (delay_ns_minus_half_period < 8.606):
            word = 152
        elif (delay_ns_minus_half_period < 8.678):
            word = 153
        elif (delay_ns_minus_half_period < 8.724):
            word = 154
        elif (delay_ns_minus_half_period < 8.775):
            word = 155
        elif (delay_ns_minus_half_period < 8.819):
            word = 156
        elif (delay_ns_minus_half_period < 8.888):
            word = 157
        elif (delay_ns_minus_half_period < 8.924):
            word = 158
        elif (delay_ns_minus_half_period < 9.056):
            word = 159
        elif (delay_ns_minus_half_period < 9.087):
            word = 160
        elif (delay_ns_minus_half_period < 9.157):
            word = 161
        elif (delay_ns_minus_half_period < 9.195):
            word = 162
        elif (delay_ns_minus_half_period < 9.265):
            word = 163
        elif (delay_ns_minus_half_period < 9.302):
            word = 164
        elif (delay_ns_minus_half_period < 9.368):
            word = 165
        elif (delay_ns_minus_half_period < 9.399):
            word = 166
        elif (delay_ns_minus_half_period < 9.46):
            word = 167
        elif (delay_ns_minus_half_period < 9.505):
            word = 168
        elif (delay_ns_minus_half_period < 9.571):
            word = 169
        elif (delay_ns_minus_half_period < 9.612):
            word = 170
        elif (delay_ns_minus_half_period < 9.683):
            word = 171
        elif (delay_ns_minus_half_period < 9.723):
            word = 172
        elif (delay_ns_minus_half_period < 9.795):
            word = 173
        elif (delay_ns_minus_half_period < 9.827):
            word = 174
        elif (delay_ns_minus_half_period < 9.959):
            word = 175
        elif (delay_ns_minus_half_period < 10.002):
            word = 176
        elif (delay_ns_minus_half_period < 10.063):
            word = 177
        elif (delay_ns_minus_half_period < 10.106):
            word = 178
        elif (delay_ns_minus_half_period < 10.173):
            word = 179
        elif (delay_ns_minus_half_period < 10.212):
            word = 180
        elif (delay_ns_minus_half_period < 10.276):
            word = 181
        elif (delay_ns_minus_half_period < 10.316):
            word = 182
        elif (delay_ns_minus_half_period < 10.372):
            word = 183
        elif (delay_ns_minus_half_period < 10.409):
            word = 184
        elif (delay_ns_minus_half_period < 10.48):
            word = 185
        elif (delay_ns_minus_half_period < 10.522):
            word = 186
        elif (delay_ns_minus_half_period < 10.587):
            word = 187
        elif (delay_ns_minus_half_period < 10.629):
            word = 188
        elif (delay_ns_minus_half_period < 10.703):
            word = 189
        elif (delay_ns_minus_half_period < 10.74):
            word = 190
        elif (delay_ns_minus_half_period < 10.836):
            word = 191
        elif (delay_ns_minus_half_period < 10.868):
            word = 192
        elif (delay_ns_minus_half_period < 10.933):
            word = 193
        elif (delay_ns_minus_half_period < 10.973):
            word = 194
        elif (delay_ns_minus_half_period < 11.039):
            word = 195
        elif (delay_ns_minus_half_period < 11.078):
            word = 196
        elif (delay_ns_minus_half_period < 11.153):
            word = 197
        elif (delay_ns_minus_half_period < 11.192):
            word = 198
        elif (delay_ns_minus_half_period < 11.249):
            word = 199
        elif (delay_ns_minus_half_period < 11.311):
            word = 200
        elif (delay_ns_minus_half_period < 11.379):
            word = 201
        elif (delay_ns_minus_half_period < 11.417):
            word = 202
        elif (delay_ns_minus_half_period < 11.488):
            word = 203
        elif (delay_ns_minus_half_period < 11.535):
            word = 204
        elif (delay_ns_minus_half_period < 11.605):
            word = 205
        elif (delay_ns_minus_half_period < 11.639):
            word = 206
        elif (delay_ns_minus_half_period < 11.771):
            word = 207
        elif (delay_ns_minus_half_period < 11.811):
            word = 208
        elif (delay_ns_minus_half_period < 11.877):
            word = 209
        elif (delay_ns_minus_half_period < 11.906):
            word = 210
        elif (delay_ns_minus_half_period < 11.979):
            word = 211
        elif (delay_ns_minus_half_period < 12.018):
            word = 212
        elif (delay_ns_minus_half_period < 12.085):
            word = 213
        elif (delay_ns_minus_half_period < 12.123):
            word = 214
        elif (delay_ns_minus_half_period < 12.19):
            word = 215
        elif (delay_ns_minus_half_period < 12.228):
            word = 216
        elif (delay_ns_minus_half_period < 12.31):
            word = 217
        elif (delay_ns_minus_half_period < 12.338):
            word = 218
        elif (delay_ns_minus_half_period < 12.407):
            word = 219
        elif (delay_ns_minus_half_period < 12.447):
            word = 220
        elif (delay_ns_minus_half_period < 12.506):
            word = 221
        elif (delay_ns_minus_half_period < 12.546):
            word = 222
        elif (delay_ns_minus_half_period < 12.668):
            word = 223
        elif (delay_ns_minus_half_period < 12.702):
            word = 224
        elif (delay_ns_minus_half_period < 12.774):
            word = 225
        elif (delay_ns_minus_half_period < 12.808):
            word = 226
        elif (delay_ns_minus_half_period < 12.876):
            word = 227
        elif (delay_ns_minus_half_period < 12.913):
            word = 228
        elif (delay_ns_minus_half_period < 12.985):
            word = 229
        elif (delay_ns_minus_half_period < 13.02):
            word = 230
        elif (delay_ns_minus_half_period < 13.084):
            word = 231
        elif (delay_ns_minus_half_period < 13.116):
            word = 232
        elif (delay_ns_minus_half_period < 13.193):
            word = 233
        elif (delay_ns_minus_half_period < 13.232):
            word = 234
        elif (delay_ns_minus_half_period < 13.302):
            word = 235
        elif (delay_ns_minus_half_period < 13.338):
            word = 236
        elif (delay_ns_minus_half_period < 13.408):
            word = 237
        elif (delay_ns_minus_half_period < 13.45):
            word = 238
        elif (delay_ns_minus_half_period < 13.579):
            word = 239    
        elif (delay_ns_minus_half_period < 13.607):
            word = 240
        elif (delay_ns_minus_half_period < 13.68):
            word = 241
        elif (delay_ns_minus_half_period < 13.72):
            word = 242
        elif (delay_ns_minus_half_period < 13.796):
            word = 243
        elif (delay_ns_minus_half_period < 13.821):
            word = 244
        elif (delay_ns_minus_half_period < 13.901):
            word = 245
        elif (delay_ns_minus_half_period < 13.928):
            word = 246
        elif (delay_ns_minus_half_period < 13.994):
            word = 247
        elif (delay_ns_minus_half_period < 14.025):
            word = 248
        elif (delay_ns_minus_half_period < 14.106):
            word = 249
        elif (delay_ns_minus_half_period < 14.141):
            word = 250
        elif (delay_ns_minus_half_period < 14.213):
            word = 251
        elif (delay_ns_minus_half_period < 14.248):
            word = 252
        elif (delay_ns_minus_half_period < 14.322):
            word = 253   
        else:
            word = 254

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
    
    
    
    
    
    