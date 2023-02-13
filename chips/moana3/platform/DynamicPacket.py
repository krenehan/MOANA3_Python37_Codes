# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 15:06:25 2022

@author: Kevin Renehan
"""

from copy import deepcopy
import numpy as np

class DynamicPacketException(Exception):
    pass


class DynamicPacket:
    
    # Class variables
    __number_of_chips = 0
    __patterns_per_frame = 0
    __number_of_wavelengths = 0
    
    # Wavelength
    __nir_index = 0
    __ir_index = 1

    
    
    # ====================================================
    # Initialize the data packet
    # ====================================================
    def __init__(self, number_of_chips, patterns_per_frame):
        
        # Initialize class variables
        self.__number_of_chips = number_of_chips
        self.__patterns_per_frame = patterns_per_frame
        self.__number_of_wavelengths = 2
        
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
        
        # Emitter pattern
        self.emitter_pattern = np.zeros((self.__patterns_per_frame, self.__number_of_chips, self.__number_of_wavelengths), dtype=bool)

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
    # Number of wavelengths property
    # ====================================================
    @property 
    def number_of_wavelengths(self):
        return self.__number_of_wavelengths
    
    @number_of_wavelengths.setter
    def number_of_wavelengths(self, new_number_of_wavelengths):
        print("Cannot set number of wavelengths")
        
        
    # ====================================================
    # NIR index property
    # ====================================================
    @property 
    def nir_index(self):
        return self.__nir_index
    
    @nir_index.setter
    def nir_index(self, new_nir_index):
        print("Cannot set NIR index")
        
        
    # ====================================================
    # IR index property
    # ====================================================
    @property 
    def ir_index(self):
        return self.__ir_index
    
    @ir_index.setter
    def ir_index(self, new_ir_index):
        print("Cannot set IR index")
        
    
    # ====================================================
    # Recreate function for redefinition of dynamic frame structure
    # ====================================================
    def __recreate(self, new_number_of_chips, new_patterns_per_frame):
        
        # Reset variables
        self.__number_of_chips = new_number_of_chips
        self.__patterns_per_frame = new_patterns_per_frame
        
        # Create chip dictionary
        chip_packet = {}
        
        # Fill chip dictionary with copies of packet template
        for c in range(new_number_of_chips):
            chip_packet[c] = self.__dynamic_packet_template.copy()
        
        # Create pattern dictionary
        pattern_packet = {}
        
        # Fill pattern dictionary with copies of chip packet
        for p in range(new_patterns_per_frame):
            pattern_packet[p] = deepcopy(chip_packet)
            
        # Store
        self.__dynamic_frame_structure = pattern_packet
        
        # Emitter pattern
        self.emitter_pattern = np.zeros((self.__patterns_per_frame, self.__number_of_chips, self.__number_of_wavelengths), dtype=bool)
        
        
    # ====================================================
    # Function to show values of the dynamic frame structure
    # ====================================================
    def show(self, pattern_list='all', chip_list='all'):
        
        # Print write
        print(self.write(pattern_list=pattern_list, chip_list=chip_list))
        
        
    # ====================================================
    # Override string method
    # ====================================================
    def __str__(self):
        return self.write()
                
    
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
    # Function to return string f values of the dynamic frame structure
    # ====================================================
    def read(self, filepath):
        
        # Interpret
        print("Interpreting dynamic packet file at " + filepath)
        
        # Get value from line
        def get_val(s):
            v = s.split(":")
            if len(v) < 2:
                return False, ''
            else:
                v = v[1].strip()
                return True, v
        
        # Open file and read lines
        f = open(filepath, 'r')
        ll = f.readlines() 
        f.close()
        
        # Find number of patterns
        for l in ll[::-1]:
            if "Pattern" in l:
                patterns_per_frame = int(l.split("Pattern ")[1].split(':')[0]) + 1
                break
        
        # Find number of chips
        for l in ll[::-1]:
            if "Chip" in l:
                number_of_chips = int(l.split("Chip ")[1].split(':')[0]) + 1
                break
        
        # Recreate the structure if patterns per frame or number of chips changes
        if (patterns_per_frame != self.__patterns_per_frame) or (number_of_chips != self.__number_of_chips):
            self.__recreate(number_of_chips, patterns_per_frame)
            
        # Variables for keeping track of which emitter fires in which pattern
        vcsel_enable = False
        ir_vcsel_enable = False
        nir_vcsel_enable = False
        pattern = 0
        chip = 0
        
        # Find the dynamic pattern for each chip and each pattern
        for i, l in enumerate(ll):
            
            # Check to see if we found a NIR emitter
            if (vcsel_enable and nir_vcsel_enable):
                self.emitter_pattern[pattern][chip][self.nir_index] = True
            
            # Check to see if we found an IR emitter
            if (vcsel_enable and ir_vcsel_enable):
                self.emitter_pattern[pattern][chip][self.ir_index] = True
            
            # Keep track of the pattern number
            if "Pattern" in l:
                
                # Get pattern number
                pattern = int(l.split("Pattern ")[1].split(':')[0])
                
                # Reset variables
                vcsel_enable = False
                ir_vcsel_enable = False
                nir_vcsel_enable = False
                
                # Go to next line
                continue
            
            # Keep track of the chip number
            if "Chip" in l:
                
                # Get chip number
                chip = int(l.split("Chip ")[1].split(':')[0])
                
                # Reset variables
                vcsel_enable = False
                ir_vcsel_enable = False
                nir_vcsel_enable = False
                
                # Go to next line
                continue
            
            # Find nir_vcsel_enable
            if "nir_vcsel_enable" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['nir_vcsel_enable'] = val
                
                # Check 
                if bool(int(val)):
                    nir_vcsel_enable = True
                    
                # Go to next line
                continue
            
            # Find ir_vcsel_enable
            if "ir_vcsel_enable" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['ir_vcsel_enable'] = val
                
                # Check 
                if bool(int(val)):
                    ir_vcsel_enable = True
                
                # Go to next line
                continue
            
            # Find vcsel_enable
            if "vcsel_enable" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['vcsel_enable'] = val
                
                # Check 
                if bool(int(val)):
                    vcsel_enable = True
                    
                # Go to next line
                continue
            
            # Find driver_dll_word
            if "driver_dll_word" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['driver_dll_word'] = val
                    
                # Go to next line
                continue
            
            # Find clk_flip
            if "clk_flip" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['clk_flip'] = val
                    
                # Go to next line
                continue
            
            # Find aqc_dll_coarse_word
            if "aqc_dll_coarse_word" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['aqc_dll_coarse_word'] = val
                   
                # Go to next line
                continue
            
            # Find aqc_dll_fine_word
            if "aqc_dll_fine_word" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['aqc_dll_fine_word'] = val
                    
                # Go to next line
                continue
            
            # Find aqc_dll_finest_word
            if "aqc_dll_finest_word" in l:
                
                # Get value
                succ, val = get_val(l)
                if succ:
                    self.__dynamic_frame_structure[pattern][chip]['aqc_dll_finest_word'] = val
                    
                # Go to next line
                continue
    
    
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
    # Function to check if the chip is an emitter for the pattern
    # ====================================================
    def is_emitter(self, pattern, chip):
        return (self.emitter_pattern[pattern][chip][self.nir_index] or self.emitter_pattern[pattern][chip][self.ir_index])
    
    
    # ====================================================
    # Function to check which chips are emitters are for pattern
    # ====================================================
    def emitters_for_pattern(self, pattern):
        
        # Reduce the wavelength axis
        arr = np.sum(self.emitter_pattern[pattern], axis=1, dtype=bool)
        
        # Find indices where we get true
        return tuple(arr.nonzero()[0])
    
    
    # ====================================================
    # Function to check whether the infrared or nir infrared pattern is active in pattern
    # ====================================================
    def wavelength_for_pattern(self, pattern):
        
        # Grab pattern and change to [wavelength:chip]
        arr = np.transpose(self.emitter_pattern[pattern], axes=(1,0))
        
        # Sum along the chip axis
        arr = np.sum(arr, axis=1, dtype=bool)
        
        # Return wavelength
        if arr[self.__nir_index]:
            return self.__nir_index
        elif arr[self.__ir_index]:
            return self.__ir_index
        
        # Find indices where we get true
        return tuple(arr.nonzero()[0])

        
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
    
    # Read file
    a.read("C:\\Users\\Dell-User\\Dropbox\\MOANA\\Python\\MOANA3_Python37_Codes\\chips\\moana3\\data\\rigid_4by4_hbo2_testing\\data\\nirsetting4_0p8Virsetting3_1p0V_Trial3\\dynamic_packet.txt")

    
    