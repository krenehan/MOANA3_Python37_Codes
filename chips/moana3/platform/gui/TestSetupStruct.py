# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:43:37 2021

The TestSetup class encapsulates information passed between the TestSetupDialog class and the main GUI. 
It takes care of all relevant type checking and validity checking internally as to minimize the complexity in the Qt classes. 
Parameters that are not checked are typically just left as strings, and are left as publicly accessible member variables with no associated property.
Values in constructor are defaults.


@author: Kevin Renehan
"""

from os.path import exists


class TestSetupStruct():
    '''Data structure for storing test setup information'''
    
    # Constructor
    def __init__(self, function_pointer=None ):
        
        # Logo path
        self.__logo_path = ''
        self.__logo_found = False
        
        # Status of delay line object
        self.__delay_line_object_set = False
        
        # # Callback function for invalidating measurements per pattern
        # self.__reload_dynamic_packet = self.__empty
        
        # Logging
        default_logging = False
        default_logging_directory = ""
        default_logging_directory_set = False
        
        # Control settings
        default_number_of_chips = 16
        default_pad_captured_mask = 65535
        default_number_of_captures = 100
        default_clock_frequency = 50e6
        default_period = 1/default_clock_frequency * 1e9 # nanoseconds
        default_time_gating_setting = 0.0
        default_measurements_per_pattern = 312500
        default_patterns_per_frame = 32
        default_number_of_frames = 50
        
        # External settings
        default_nir_vcsel_bias = 0.0
        default_ir_vcsel_bias = 0.0
        
        # Test settings
        default_participant_name = ""
        default_test_type = ""
        default_device_id = ""
        default_test_number = 1
        default_patch_location = ""
        
        # Constant or derived settings
        default_subtractor_value = int(round((1/default_clock_frequency) * 0.5 / 65e-12, 0))
        default_subtractor_offset = 0
        default_delay = default_period - 1 + default_time_gating_setting
        
        # Keep track of default delay
        self.__default_delay = default_delay
        
        # Conditions
        default_conditions = ""
        
        # Dictionary
        self.full_test_setup_dict = { \
                                     'Logging': default_logging, \
                                     'Logging Directory': default_logging_directory, \
                                     'Logging Directory Set': default_logging_directory_set, \
                                     'Conditions': default_conditions, \
                                     'Number of Chips': default_number_of_chips, \
                                     'Pad Captured Mask': default_pad_captured_mask, \
                                     'Number of Captures': default_number_of_captures, \
                                     'Clock Frequency': default_clock_frequency, \
                                     'Period': default_period, \
                                     'Delay': default_delay, \
                                     'Time Gating Setting': default_time_gating_setting, \
                                     'Measurements per Pattern': default_measurements_per_pattern, \
                                     'Patterns per Frame': default_patterns_per_frame, \
                                     'Number of Frames': default_number_of_frames, \
                                     'NIR VCSEL Bias': default_nir_vcsel_bias, \
                                     'IR VCSEL Bias': default_ir_vcsel_bias, \
                                     'Participant Name': default_participant_name, \
                                     'Test Type': default_test_type, \
                                     'Device ID': default_device_id, \
                                     'Test Number': default_test_number, \
                                     'Patch Location': default_patch_location, \
                                     'Subtractor Value': default_subtractor_value, \
                                     'Subtractor Offset': default_subtractor_offset, \
                                     'Base Subtractor Value': default_subtractor_value, \
                                     }
        
        
    ################################
    # Override string method
    ################################ 
    def __str__(self):
        
        # Create string
        s = ''
        for k in self.full_test_setup_dict:
            s = s + k + ": " + str(self.full_test_setup_dict[k]) + "\n"
            
        # Return
        return s
    
    
    # ################################
    # # Empty function
    # ################################ 
    # def __empty(self):
    #     pass
    
    
    # ################################
    # # Callback for reloading dynamic packet
    # ################################ 
    # def register_reload_dynamic_packet_callback(self, function_pointer):
    #     self.__reload_dynamic_packet = function_pointer
        
        
    ################################
    # Logging property
    ################################    
    @property
    def logging(self):
        return self.full_test_setup_dict['Logging']
    
    @logging.setter
    def logging(self, new_logging):
        try:
            new_logging = bool(new_logging)
            self.full_test_setup_dict['Logging'] = new_logging
        except (TypeError, ValueError):
            print("Logging setting not valid")
            
            
    ################################
    # Logging directory property
    ################################    
    @property
    def logging_directory(self):
        return self.full_test_setup_dict['Logging Directory']
    
    @logging_directory.setter
    def logging_directory(self, new_logging_directory):
        try:
            self.full_test_setup_dict['Logging Directory Set'] = exists(str(new_logging_directory))
            self.full_test_setup_dict['Logging Directory'] = new_logging_directory
                
        except (TypeError, ValueError):
            print("Logging directory not valid")
            
            
    ################################
    # Logging directory set property
    ################################    
    @property
    def logging_directory_set(self):
        return self.full_test_setup_dict['Logging Directory Set']
    
    @logging_directory_set.setter
    def logging_directory_set(self, new_logging_directory_set):
        print("Logging directory set cannot be modified direectly")
            
            
    ################################
    # Logo path property
    ################################  
    @property
    def logo_path(self):
        return self.__logo_path
    
    @logo_path.setter
    def logo_path(self, new_logo_path):
        try:
            self.__logo_found = exists(new_logo_path)
            if self.__logo_found:
                self.__logo_path = new_logo_path
        except (TypeError, ValueError):
            print("Logo path not valid")
            
            
    ################################
    # Logo found property
    ################################
    @property
    def logo_found(self):
        return self.__logo_found
    
    @logo_found.setter
    def logo_found(self, new_logo_found):
        print("Logo found cannot be modified externally")
        
            
    ################################
    # Number of chips property
    ################################
    @property
    def number_of_chips(self):
        return self.full_test_setup_dict['Number of Chips']
    
    @number_of_chips.setter
    def number_of_chips(self, new_number_of_chips):
        print("Number of chips cannot be changed")
        
        
    ################################
    # Number of captures property
    ################################
    @property
    def number_of_captures(self):
        return self.full_test_setup_dict['Number of Captures']
    
    @number_of_captures.setter
    def number_of_captures(self, new_number_of_captures):
        try:
            new_number_of_captures = int(new_number_of_captures)
            if new_number_of_captures > 0:
                self.full_test_setup_dict['Number of Captures'] = new_number_of_captures
            else:
                print("Number of captures not accepted")
        except (TypeError, ValueError):
            print("Number of captures not valid")
            

    ################################
    # Clock frequency property
    ################################
    @property
    def clock_frequency(self):
        return self.full_test_setup_dict['Clock Frequency']
    
    @clock_frequency.setter
    def clock_frequency(self, new_clock_frequency):
        try:
            new_clock_frequency = float(new_clock_frequency)
            if new_clock_frequency in (25e6, 50e6, 100e6):
                self.full_test_setup_dict['Clock Frequency'] = new_clock_frequency
                self.full_test_setup_dict['Period'] = 1/self.full_test_setup_dict['Clock Frequency'] * 1e9
            else:
                print("Clock frequency not accepted")
        except (TypeError, ValueError):
            print("Clock frequency not valid")
            

    ################################
    # Period property
    ################################
    @property
    def period(self):
        return self.full_test_setup_dict['Period']
    
    @period.setter
    def period(self, new_period):
        print("Period cannot be set directly")
            
            
    ################################
    # Time gating setting property
    ################################
    @property
    def time_gating_setting(self):
        return self.full_test_setup_dict['Time Gating Setting']
    
    @time_gating_setting.setter
    def time_gating_setting(self, new_time_gating_setting):
        try:
            new_time_gating_setting = round(float(new_time_gating_setting), 3)
            if (new_time_gating_setting >= 0.0) and (new_time_gating_setting <= 15.0):
                self.full_test_setup_dict['Time Gating Setting'] = new_time_gating_setting
                self.full_test_setup_dict['Delay'] = round(self.__default_delay + self.time_gating_setting, 3)
            else:
                print("Time gating setting not accepted")
        except (TypeError, ValueError):
            print("Time gating setting not valid")
            
    
    ################################
    # Measurements per pattern property
    ################################
    @property
    def measurements_per_pattern(self):
        return self.full_test_setup_dict['Measurements per Pattern']
    
    @measurements_per_pattern.setter
    def measurements_per_pattern(self, new_measurements_per_pattern):
        try:
            new_measurements_per_pattern = int(new_measurements_per_pattern)
            if (new_measurements_per_pattern >= 20000) and (new_measurements_per_pattern < 2**24-1):
                self.full_test_setup_dict['Measurements per Pattern'] = new_measurements_per_pattern
            else:
                print("Measurements per pattern setting not accepted")
        except (TypeError, ValueError):
            print("Measurements per pattern not valid")
            
            
    ################################
    # Patterns per frame property
    ################################
    @property
    def patterns_per_frame(self):
        return self.full_test_setup_dict['Patterns per Frame']
    
    @patterns_per_frame.setter
    def patterns_per_frame(self, new_patterns_per_frame):
        try:
            new_patterns_per_frame = int(new_patterns_per_frame)
            if new_patterns_per_frame != self.full_test_setup_dict['Patterns per Frame']:
                # self.__reload_dynamic_packet()
                if (new_patterns_per_frame > 0) and (new_patterns_per_frame <= 128):
                    self.full_test_setup_dict['Patterns per Frame'] = new_patterns_per_frame
                else:
                    print("Patterns per frame setting not accepted")
        except (ValueError, TypeError):
            print("Patterns per frame not valid")

            
    ################################
    # Number of frames property
    ################################
    @property
    def number_of_frames(self):
        return self.full_test_setup_dict['Number of Frames']
    
    @number_of_frames.setter
    def number_of_frames(self, new_number_of_frames):
        try:
            new_number_of_frames = int(new_number_of_frames)
            if (new_number_of_frames > 0):
                self.full_test_setup_dict['Number of Frames'] = new_number_of_frames
            else:
                print("Number of frames setting not accepted")
        except (ValueError, TypeError):
            print("Number of frames setting not valid")
            
            
    ################################
    # NIR VCSEL bias property
    ################################
    @property
    def nir_vcsel_bias(self):
        return self.full_test_setup_dict['NIR VCSEL Bias']
    
    @nir_vcsel_bias.setter
    def nir_vcsel_bias(self, new_nir_vcsel_bias):
        try:
            new_nir_vcsel_bias = float(new_nir_vcsel_bias)
            new_nir_vcsel_bias = round(new_nir_vcsel_bias, ndigits=1)
            if (abs(new_nir_vcsel_bias) <= 1.2):
                self.full_test_setup_dict['NIR VCSEL Bias'] = new_nir_vcsel_bias
            else:
                print("NIR VCSEL bias not accepted, should be less than 1.2V")
        except (ValueError, TypeError):
            print("NIR VCSEL bias not valid")
            
            
    ################################
    # IR VCSEL bias property
    ################################
    @property
    def ir_vcsel_bias(self):
        return self.full_test_setup_dict['IR VCSEL Bias']
    
    @ir_vcsel_bias.setter
    def ir_vcsel_bias(self, new_ir_vcsel_bias):
        try:
            new_ir_vcsel_bias = float(new_ir_vcsel_bias)
            new_ir_vcsel_bias = round(new_ir_vcsel_bias, ndigits=1)
            if (abs(new_ir_vcsel_bias) <= 1.2):
                self.full_test_setup_dict['IR VCSEL Bias'] = new_ir_vcsel_bias
            else:
                print("IR VCSEL bias not accepted, should be less than 1.2V")
        except (ValueError, TypeError):
            print("IR VCSEL bias not valid")
            
            
    ################################
    # Participant name property
    ################################
    @property
    def participant_name(self):
        return self.full_test_setup_dict['Participant Name']
    
    @participant_name.setter
    def participant_name(self, new_participant_name):
        try:
            self.full_test_setup_dict['Participant Name'] = str(new_participant_name)
        except (TypeError, ValueError):
            print("Participant name string not valid")
            
            
    ################################
    # Test type property
    ################################
    @property
    def test_type(self):
        return self.full_test_setup_dict['Test Type']
    
    @test_type.setter
    def test_type(self, new_test_type):
        try:
            self.full_test_setup_dict['Test Type'] = str(new_test_type)
        except (TypeError, ValueError):
            print("Test type string not valid")
            
            
    ################################
    # Device ID property
    ################################
    @property
    def device_id(self):
        return self.full_test_setup_dict['Device ID']
    
    @device_id.setter
    def device_id(self, new_device_id):
        try:
            self.full_test_setup_dict['Device ID'] = str(new_device_id)
        except (TypeError, ValueError):
            print("Device ID string not valid")
            
            
    ################################
    # Test number property
    ################################
    @property
    def test_number(self):
        return self.full_test_setup_dict['Test Number']
    
    @test_number.setter
    def test_number(self, new_test_number):
        try:
            self.full_test_setup_dict['Test Number'] = int(new_test_number)
        except (TypeError, ValueError):
            print("Test number not valid")
            
            
    ################################
    # Patch location property
    ################################
    @property
    def patch_location(self):
        return self.full_test_setup_dict['Patch Location']
    
    @patch_location.setter
    def patch_location(self, new_patch_location):
        try:
            self.full_test_setup_dict['Patch Location'] = str(new_patch_location)
        except (TypeError, ValueError):
            print("Patch location string not valid")
            
            
    ################################
    # Subtractor offset property
    ################################
    @property
    def subtractor_offset(self):
        return self.full_test_setup_dict['Subtractor Offset']
    
    @subtractor_offset.setter
    def subtractor_offset(self, new_subtractor_offset):
        try:
            new_subtractor_offset = int(new_subtractor_offset)
            new_subtractor_value = self.full_test_setup_dict['Base Subtractor Value'] + new_subtractor_offset
            if (new_subtractor_value >= 0) and (new_subtractor_value < 1024):
                self.full_test_setup_dict['Subtractor Offset'] = new_subtractor_offset
                self.full_test_setup_dict['Subtractor Value'] = new_subtractor_value
            else:
                print("Subtractor offset not accepted")
        except (ValueError, TypeError):
            print("Subtractor offset not valid: " + str(new_subtractor_offset))
            
            
    ################################
    # Base subtractor value property
    ################################
    @property
    def base_subtractor_value(self):
        return self.full_test_setup_dict['Subtractor Value']
    
    @base_subtractor_value.setter
    def base_subtractor_value(self, new_base_subtractor_value):
        try:
            new_base_subtractor_value = int(new_base_subtractor_value)
            if (new_base_subtractor_value >= 0) and (new_base_subtractor_value < 1024):
                self.full_test_setup_dict['Base Subtractor Value'] = new_base_subtractor_value
                
                # Check to see if subtractor offset is acceptable with new base subtractor value
                new_subtractor_value = self.full_test_setup_dict['Base Subtractor Value'] + self.full_test_setup_dict['Subtractor Offset']
                if (new_subtractor_value >= 0) and (new_subtractor_value < 1024):
                    
                    # If subtractor value is still acceptable after considering offset, accept the value
                    self.full_test_setup_dict['Subtractor Value'] = new_subtractor_value
                    
                else:
                    
                    # If previous subtractor offset is going to cause problems with subtractor value, set offset back to 0 and subtractor to base value
                    self.full_test_setup_dict['Subtractor Offset'] = 0
                    self.full_test_setup_dict['Subtractor Value'] = self.full_test_setup_dict['Base Subtractor Value']
            else:
                print("Subtractor value not accepted")

        except (ValueError, TypeError):
            print("Subtractor value not valid")
    
    
    ################################
    # Subtractor value property
    ################################
    @property
    def subtractor_value(self):
        return self.full_test_setup_dict['Subtractor Value']
    
    @subtractor_value.setter
    def subtractor_value(self, new_subtractor_value):
            print("Subtractor_value cannot be set directly")
    
    
    ################################
    # Delay property
    ################################
    @property
    def delay(self):
        return self.full_test_setup_dict['Delay']
    
    @delay.setter
    def delay(self, new_delay):
            print("Delay cannot be set directly")
            
            
    ################################
    # Conditions property
    ################################
    @property
    def conditions(self):
        return self.full_test_setup_dict['Conditions']
    
    @conditions.setter
    def conditions(self, new_conditions):
        try:
            self.full_test_setup_dict['Conditions'] = str(new_conditions)
        except (TypeError, ValueError):
            print("Conditions string not valid")
            
            
    ################################
    # Pad captured mask property
    ################################
    @property
    def pad_captured_mask(self):
        return self.full_test_setup_dict['Pad Captured Mask']
    
    @pad_captured_mask.setter
    def pad_captured_mask(self, new_pad_captured_mask):
        try:
            new_pad_captured_mask = int(new_pad_captured_mask)
            if (new_pad_captured_mask > 0) and (new_pad_captured_mask < 2**16):
                self.full_test_setup_dict['Pad Captured Mask'] = new_pad_captured_mask
        except (TypeError, ValueError):
            print("Pad captured mask not valid: " + str(new_pad_captured_mask))
            
            
    ################################
    # Frame time property
    ################################
    @property
    def frame_time(self):
        return  self.full_test_setup_dict['Patterns per Frame'] *\
                self.full_test_setup_dict['Measurements per Pattern'] * self.full_test_setup_dict['Period'] / 1e9
    
    @frame_time.setter
    def frame_time(self, new_frame_time):
        print("Cannot set frame time")
            
            
    ################################
    # Capture time property
    ################################
    @property
    def capture_time(self):
        return  self.full_test_setup_dict['Number of Frames'] * \
                self.full_test_setup_dict['Patterns per Frame'] *\
                self.full_test_setup_dict['Measurements per Pattern'] * self.full_test_setup_dict['Period'] / 1e9
    
    @capture_time.setter
    def capture_time(self, new_capture_time):
        print("Cannot set capture time")
        
        

    ################################
    # Refresh delay after delay line has been initialized
    ################################
    def refresh_actual_delay(self, delay_line_object):
        
        # Store delay line object
        self.dut_delay_line = delay_line_object
        
        # Keep track of status
        self.__delay_line_object_set = True
        
        # Find delay of delay line given coarse, fine, finest, clock flip bits in the dynamic packet file
        delay = self.dut_delay_line.get_setting(self.delay)[4]
        
        # Update default delay
        self.__default_delay = delay
        
        # Set the delay
        self.full_test_setup_dict['Delay'] = delay
        
        
    ################################
    # Refresh delay from dynamic packet file input
    ################################
    def update_time_gating_setting_from_dynamic_packet(self, clk_flip, coarse, fine, finest):
        
        if not self.__delay_line_object_set:
            print("Time gating setting not updated because delay line was not set")
        else:
            # Find delay of delay line given coarse, fine, finest, clock flip bits in the dynamic packet file
            delay = self.dut_delay_line.get_delay(clk_flip, coarse, fine, finest)
            
            # Find new values for delay and time gating setting
            time_gating_setting = delay - self.__default_delay
            print("{}, {}, {}".format(self.delay, delay, time_gating_setting))
            
            # Update the time gating setting accordingly
            self.time_gating_setting = time_gating_setting
        
            
    ################################
    # Interpret a test setup file
    ################################
    def interpret_test_setup_file(self, filepath):
    
        # Open file and create list of lines
        print("Reading test setup file at " + str(filepath))
        f = open(filepath, "r")
        ll = f.readlines()
        f.close()
        
        # Interpret the line list
        self.__interpret_test_setup_line_list(ll)
        
        
    ################################
    # Interpret a test setup string
    ################################
    def interpret_test_setup_string(self, test_setup_string):
    
        # Open file and create list of lines
        ll = test_setup_string.splitlines(keepends=True)
        
        # Interpret the line list
        self.__interpret_test_setup_line_list(ll)
        
        
    ################################
    # Interpret a list of lines from test setup file
    ################################
    def __interpret_test_setup_line_list(self, ll):
        
        # Interpret lines
        ldict = {}
        for l in ll:
            s = l.split(": ", 1)
            if len(s) != 2:
                continue
            else:
                prefix, suffix = s
            prefix = prefix.strip()
            suffix = suffix.strip()
            ldict[prefix] = suffix
        
        # Go through all keys
        for k in ldict:
            
            # Inherited keys
            if k == "Conditions":
                self.conditions = ldict[k]
            elif k == "Pad Captured Mask":
                self.pad_captured_mask = ldict[k]
            elif k == "Number of Captures":
                self.number_of_captures = ldict[k]
            elif k == "Clock Frequency":
                self.clock_frequency = ldict[k]
            elif k == "Time Gating Setting":
                self.time_gating_setting = ldict[k]
            elif k == "Measurements per Pattern":
                self.measurements_per_pattern = ldict[k]
            elif k == "Number of Frames":
                self.number_of_frames == ldict[k]
            elif k == "NIR VCSEL Bias":
                self.nir_vcsel_bias = ldict[k]
            elif k == "IR VCSEL Bias":
                self.ir_vcsel_bias = ldict[k]
            elif k == "Participant Name":
                self.participant_name = ldict[k]
            elif k == "Test Type":
                self.test_type = ldict[k]
            elif k == "Device ID":
                self.device_id = ldict[k]
            elif k == "Test Number":
                self.test_number = ldict[k]
            elif k == "Patch Location":
                self.patch_location = ldict[k]
            elif k == "Base Subtractor Value":
                self.base_subtractor_value = ldict[k]
            elif k == "Subtractor Offset":
                self.subtractor_offset = ldict[k]
                
            # Ignored keys
            elif k == "Logging":
                continue
            elif k == "Logging Directory":
                continue
            elif k == "Logging Directory Set":
                continue
            elif k == "Number of Chips":
                continue
            elif k == "Period":
                continue
            elif k == "Subtractor Value":
                continue
            elif k == "Patterns per Frame":
                continue
            elif k == "Delay":
                continue
            
            # Accept all other keys
            else:
                self.full_test_setup_dict[k] = ldict[k]
                
                
# Runnable
if __name__ == "__main__":
    
    # Filepath
    fp = 'C:\\Users\\Dell-User\\Dropbox\\MOANA\\Python\\MOANA3_Python37_Codes\\chips\\moana3\\data\\rigid_4by4_hbo2_testing\\data\\nirsetting4_0p8Virsetting3_1p0V_Trial5\\test_setup.txt'
    
    ts = TestSetupStruct()
    ts.interpret_test_setup_file(fp)
    
    # Create test setup file
    f = open('C:\\Users\\Dell-User\\Desktop\\ts_out.txt', 'w')
    f.write(str(ts))
    f.close()
    