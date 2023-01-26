# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:06:25 2022

@author: Kevin Renehan
"""

from copy import deepcopy


class DynamicPacketException(Exception):
    pass


class DynamicPacket:
    
    # Class variables
    __number_of_chips = 0
    __patterns_per_frame = 0


    
    
    # ====================================================
    # Initialize the data packet
    # ====================================================
    def __init__(self, number_of_chips, patterns_per_frame):
        
        # Initialize class variables
        self.__number_of_chips = number_of_chips
        self.__patterns_per_frame = patterns_per_frame
        
        # Create template
        self.__dynamic_packet_template = {  
                                    'vcsel_enable': '0',          \
                                    'nir_vcsel_enable': '0',      \
                                    'ir_vcsel_enable': '0',       \
                                    'driver_dll_word': '00000',       \
                                    'clk_flip': '0',              \
                                    'aqc_dll_coarse_word': '0000',   \
                                    'aqc_dll_fine_word': '000',     \
                                    'aqc_dll_finest_word': '0',   \
                                 }
            
        # Create template
        self.__dynamic_packet_bitorder_and_index = {
                                    0: ('aqc_dll_finest_word', 0),
                                    1: ('aqc_dll_fine_word', 2),
                                    2: ('aqc_dll_fine_word', 1),
                                    3: ('aqc_dll_fine_word', 0),
                                    4: ('aqc_dll_coarse_word', 3),
                                    5: ('aqc_dll_coarse_word', 2),
                                    6: ('aqc_dll_coarse_word', 1),
                                    7: ('aqc_dll_coarse_word', 0),
                                    8: ('clk_flip', 0),
                                    9: ('driver_dll_word', 4),
                                    10: ('driver_dll_word', 3),
                                    11: ('driver_dll_word', 2),
                                    12: ('driver_dll_word', 1),
                                    13: ('driver_dll_word', 0),
                                    14: ('ir_vcsel_enable', 0),
                                    15: ('nir_vcsel_enable', 0),
                                    16: ('vcsel_enable', 0),
                                }
        self.__number_of_dynamic_bits = 17
        

        # Create chip dictionary
        chip_packet = {}
        
        # Fill chip dictionary with copies of packet template
        for c in range(number_of_chips):
            chip_packet[c] = self.__dynamic_packet_template.copy()
        
        # Create pattern dictionary
        pattern_packet = {}
        
        # Fill pattern dictionary with copies of chip packet
        for p in range(patterns_per_frame):
            pattern_packet[p] = deepcopy(chip_packet)
            
        # Store
        self.__dynamic_frame_structure = pattern_packet
            


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
    # Patterns per frame property
    # ====================================================
    @property 
    def patterns_per_frame(self):
        return self.__patterns_per_frame
    
    @patterns_per_frame.setter
    def patterns_per_frame(self, new_patterns_per_frame):
        print("Cannot set patterns per frame after initialization")
        
        
    # ====================================================
    # Function to show values of the dynamic frame structure
    # ====================================================
    def show(self, pattern_list='all', chip_list='all'):
        
        # Check for pattern
        if pattern_list == 'all':
            pattern_list = range(self.__patterns_per_frame)

        # Check for chip
        if chip_list == 'all':
            chip_list = range(self.__number_of_chips)
        
        # Check dimensions
        if (min(pattern_list) < 0) or (max(pattern_list) > self.__patterns_per_frame):
            raise DynamicPacketException("Pattern index out of range in call to show()")
        if (min(chip_list) < 0) or (max(chip_list) > self.__number_of_chips):
            raise DynamicPacketException("Chip index out of range in call to show()")
            
        # Print header        
        print("------------------ Dynamic Frame Structure ------------------")
        
        # Print pattern info
        for p in pattern_list:
            print("    Pattern " + str(p) + ":")
            
            # Print chip info
            for c in chip_list:
                print("        Chip " + str(c) + ":")
                print("            vcsel_enable          : " + self.__dynamic_frame_structure[p][c]['vcsel_enable'])
                print("            nir_vcsel_enable      : " + self.__dynamic_frame_structure[p][c]['nir_vcsel_enable'])
                print("            ir_vcsel_enable       : " + self.__dynamic_frame_structure[p][c]['ir_vcsel_enable'])
                print("            driver_dll_word       : " + self.__dynamic_frame_structure[p][c]['driver_dll_word'])
                print("            clk_flip              : " + self.__dynamic_frame_structure[p][c]['clk_flip'])
                print("            aqc_dll_coarse_word   : " + self.__dynamic_frame_structure[p][c]['aqc_dll_coarse_word'])
                print("            aqc_dll_fine_word     : " + self.__dynamic_frame_structure[p][c]['aqc_dll_fine_word'])
                print("            aqc_dll_finest_word   : " + self.__dynamic_frame_structure[p][c]['aqc_dll_finest_word'])
                
                
    # ====================================================
    # Function to return string f values of the dynamic frame structure
    # ====================================================
    def write(self, pattern_list='all', chip_list='all'):
        
        # Check for pattern
        if pattern_list == 'all':
            pattern_list = range(self.__patterns_per_frame)

        # Check for chip
        if chip_list == 'all':
            chip_list = range(self.__number_of_chips)
        
        # Check dimensions
        if (min(pattern_list) < 0) or (max(pattern_list) > self.__patterns_per_frame):
            raise DynamicPacketException("Pattern index out of range in call to show()")
        if (min(chip_list) < 0) or (max(chip_list) > self.__number_of_chips):
            raise DynamicPacketException("Chip index out of range in call to show()")
            
        # Print header        
        s = "------------------ Dynamic Frame Structure ------------------" + '\n'
        
        # Print pattern info
        for p in pattern_list:
            s = s + "    Pattern " + str(p) + ":" + '\n'
            
            # Print chip info
            for c in chip_list:
                s = s + "        Chip " + str(c) + ":" + '\n'
                s = s + "            vcsel_enable          : " + self.__dynamic_frame_structure[p][c]['vcsel_enable'] + '\n'
                s = s + "            nir_vcsel_enable      : " + self.__dynamic_frame_structure[p][c]['nir_vcsel_enable'] + '\n'
                s = s + "            ir_vcsel_enable       : " + self.__dynamic_frame_structure[p][c]['ir_vcsel_enable'] + '\n'
                s = s + "            driver_dll_word       : " + self.__dynamic_frame_structure[p][c]['driver_dll_word'] + '\n'
                s = s + "            clk_flip              : " + self.__dynamic_frame_structure[p][c]['clk_flip'] + '\n'
                s = s + "            aqc_dll_coarse_word   : " + self.__dynamic_frame_structure[p][c]['aqc_dll_coarse_word'] + '\n'
                s = s + "            aqc_dll_fine_word     : " + self.__dynamic_frame_structure[p][c]['aqc_dll_fine_word'] + '\n'
                s = s + "            aqc_dll_finest_word   : " + self.__dynamic_frame_structure[p][c]['aqc_dll_finest_word'] + '\n'
                
        # Return string
        return s
    
    
    # ====================================================
    # Function to fill values of the dynamic frame structure
    # ====================================================
    def fill(self, pattern_list='all', chip_list='all', field_dict={}):
        
        # Check for pattern
        if pattern_list == 'all':
            pattern_list = range(self.__patterns_per_frame)

        # Check for chip
        if chip_list == 'all':
            chip_list = range(self.__number_of_chips)
            
        # Check for fields
        if len(field_dict) == 0:
            return 0
    
        # Check dimensions
        if (min(pattern_list) < 0) or (max(pattern_list) > self.__patterns_per_frame):
            raise DynamicPacketException("Pattern index out of range in call to fill()")
        if (min(chip_list) < 0) or (max(chip_list) > self.__number_of_chips):
            raise DynamicPacketException("Chip index out of range in call to fill()")
            
        # Check that fields are valid
        for f in field_dict:
            if f not in self.__dynamic_packet_template:
                raise DynamicPacketException("Field " + f + " not valid in call to fill()")
            
        # Fill
        for p in pattern_list:
            for c in chip_list:
                for f in field_dict:
                    
                    # Verify that field has correct length
                    if len(field_dict[f]) != len(self.__dynamic_packet_template[f]):
                        raise DynamicPacketException("Field " + f + " should be " + str(len(self.__dynamic_packet_template[f])) + " bits, but has " + str(len(field_dict[f])) + " bits in call to fill()")
                    
                    # Debug
                    # print("Filling pattern {}, chip {}, field {} with {}".format(p,c,f,field_dict[f]))
                    
                    # Update field
                    self.__dynamic_frame_structure[p][c][f] = field_dict[f]
        
        # Success
        return 0
                    
        
    # ====================================================
    # Function to create pipe in bytearray from dynamic frame structure
    # ====================================================
    def create_pipe_in(self):
    
        # Initialize bytearray of correct size
        barray = bytearray(17*2*self.__patterns_per_frame)
        
        # Initialize bit-strings
        bstr = []
        
        # Append 
        for p in range(self.__patterns_per_frame):
            
            # Loop through each dynamic bit
            for f_and_i in range(self.__number_of_dynamic_bits):
                
                # Pull out the field and index for each bit
                f, i = self.__dynamic_packet_bitorder_and_index[f_and_i]
                
                # Loop through 16 bits, with chip 15 being in the MSB position
                for c in range(15, -1, -1):
                    
                    # Default value for bit 
                    b = '0'
                    
                    # If the bit is associated with a chip, pull it out of dynamic frame structure
                    if c < self.__number_of_chips:
                    
                        # Extract bit value
                        b = self.__dynamic_frame_structure[p][c][f][i]
                        
                        # Debug
                        # print("Filling pattern {}, field {}, index {}, chip {} with {}".format( p, f, i, c, b))
                        
                    # Add to bitstring
                    bstr.append(b)
                    
        # Convert bitstring
        bstr = ''.join(bstr)
        # for i in range(len(bstr)//16):
        #     print(bstr[i*16:(i+1)*16])
        
        # Loop through bitstring and fill bytearray
        for bt in range(len(barray)):
            
            val = bstr[bt*8:(bt+1)*8]
            barray[bt] = int(val , base=2)
            # print("Filling byte {} with {}".format(bt, barray[bt]))
        
        # Return bytearray for pipe in
        return barray
    
    
# Runnable
if __name__ == "__main__":
    
    # Init
    a = DynamicPacket(2, 2)
    
    # Set every chip in every pattern to have clock flip of '1'
    a.fill(field_dict={'clk_flip': '1'})
    
    # Set chip 0 in every pattern to have VCSEL enabled
    a.fill(chip_list=[0], field_dict={'vcsel_enable': '1'})
    
    # Set chip 1 in pattern 1 to have coarse word of 1100
    a.fill(chip_list=[1], pattern_list=[1], field_dict={'aqc_dll_coarse_word': '1100'})
    
    # Show the result
    a.show()
    
    # Create the pipe in
    b = a.create_pipe_in()

    
    
    
    
    
    
    