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

class TestSetup():
    '''Data structure for storing test setup information'''
    
    # Constructor
    def __init__(self):
        
        # Stream mode
        self.__stream_mode = False
        
        # Logging
        self.__logging = False
        self.__logging_directory = ""
        self.__logging_directory_set = False
        
        # Logo path
        self.__logo_path = ''
        self.__logo_found = False
        
        # Control settings
        self.__number_of_chips = 16
        self.__number_of_captures = 10000
        self.__clock_frequency = 50e6
        self.__period = 1/self.__clock_frequency
        self.__vcsel_setting = 2
        self.__time_gating_setting = 0.0
        self.__measurements_per_pattern = 32000
        self.__patterns_per_frame = 8
        self.__number_of_frames = 1
        
        # External settings
        self.__vcsel_bias = 0.0
        self.__laser_wavelength = 670
        self.__laser_power = 0.0
        self.__laser_bandwidth = 10
        self.__fiber_type = ""
        self.__other_equipment = ""
        
        # Test settings
        self.__participant_name = ""
        self.__test_type = ""
        self.__test_geometry = ""
        self.__patch_location = ""
        self.__phantom_number = ""
        self.__solution_number = ""
        self.__roi_size = ""
        self.__roi_ua = ""
        
        # Constant or derived settings
        self.__spad_voltage = 28.7
        self.__vrst_voltage = 3.3
        self.__subtractor_offset = 0
        self.__base_subtractor_value = int(round((1/self.__clock_frequency) * 0.5 / 70e-12, 0)) - 20#int(round((1/self.__clock_frequency) * 0.5 / 70e-12, 0))
        self.__subtractor_value = self.__base_subtractor_value
        self.__delay = self.__period * 1e9 + 150e-3 + self.__time_gating_setting - 2#self.__period*1e9 + 150e-3 + self.__time_gating_setting - 8
        
        # Conditions
        self.__conditions = ""
        
        
    ################################
    # Override string method
    ################################ 
    def __str__(self):
        
        # Create string
        s = \
            "Conditions: " + str(self.__conditions) + "\n" \
            "Number of Chips: " + str(self.__number_of_chips) + "\n" \
            "Number of Captures: " + str(self.__number_of_captures) + "\n" \
            "Clock Frequency: " + str(self.__clock_frequency) + "\n" \
            "Period: " + str(self.__period) + "\n" \
            "Delay: " + str(self.__delay) + "\n" \
            "VCSEL Setting: " + str(self.__vcsel_setting) + "\n" \
            "Time Gating Setting: " + str(self.__time_gating_setting) + "\n" \
            "Measurements per Pattern: " + str(self.__measurements_per_pattern) + "\n" \
            "Patterns per Frame: " + str(self.__patterns_per_frame) + "\n" \
            "Number of Frames: " + str(self.__number_of_frames) + "\n" \
            "VCSEL Bias: " + str(self.__vcsel_bias) + "\n" \
            "Laser Wavelength: " + str(self.__laser_wavelength) + "\n" \
            "Laser Power: " + str(self.__laser_power) + "\n" \
            "Laser Bandwidth: " + str(self.__laser_bandwidth) + "\n" \
            "Fiber Type: " + str(self.__fiber_type) + "\n" \
            "Other Equipment: " + str(self.__other_equipment) + "\n" \
            "Participant Name: " + str(self.__participant_name) + "\n" \
            "Test Type: " + str(self.__test_type) + "\n" \
            "Test Geometry: " + str(self.__test_geometry) + "\n" \
            "Patch Location: " + str(self.__patch_location) + "\n" \
            "Phantom Number: " + str(self.__phantom_number) + "\n" \
            "Solution Number: " + str(self.__solution_number) + "\n" \
            "ROI Size: " + str(self.__roi_size) + "\n" \
            "ROI ua: " + str(self.__roi_ua) + "\n" \
            "SPAD Voltage: " + str(self.__spad_voltage) + "\n" \
            "VRST Voltage: " + str(self.__vrst_voltage) + "\n" \
            "Subtractor Offset: " + str(self.__subtractor_offset) + "\n" \
            "Base Subtractor Value: " + str(self.__base_subtractor_value) + "\n" \
            "Subtractor Value: " + str(self.__subtractor_value) + "\n" \
            "Logging: " + str(self.__logging) + "\n" + \
            "Logging Directory: " + str(self.__logging_directory) + "\n" + \
            "Logging Directory Set: " + str(self.__logging_directory_set) + "\n" + \
            "Logo Path: " + str(self.__logo_path) + "\n" \
            "Logo Found: " + str(self.__logo_found) + "\n" \
                
        return s
    
    
    # TODO: Implement this function
    def fromFile(f):
        pass

            
    ################################
    # Stream mode property
    ################################    
    @property
    def stream_mode(self):
        return self.__stream_mode
    
    @stream_mode.setter
    def stream_mode(self, new_stream_mode):
        try:
            new_stream_mode = bool(new_stream_mode)
            self.__stream_mode = new_stream_mode
        except (TypeError, ValueError):
            print("Stream mode setting not valid")
        
        
    ################################
    # Logging property
    ################################    
    @property
    def logging(self):
        return self.__logging
    
    @logging.setter
    def logging(self, new_logging):
        try:
            new_logging = bool(new_logging)
            self.__logging = new_logging
        except (TypeError, ValueError):
            print("Logging setting not valid")
            
            
    ################################
    # Logging directory property
    ################################    
    @property
    def logging_directory(self):
        return self.__logging_directory
    
    @logging_directory.setter
    def logging_directory(self, new_logging_directory):
        try:
            self.__logging_directory_set = exists(str(new_logging_directory))
            self.__logging_directory = new_logging_directory
                
        except (TypeError, ValueError):
            print("Logging directory not valid")
            
            
    ################################
    # Logging directory set property
    ################################    
    @property
    def logging_directory_set(self):
        return self.__logging_directory_set
    
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
    def number_of_chips_str(self):
        return str(self.__number_of_chips)
    
    @property
    def number_of_chips(self):
        return self.__number_of_chips
    
    @number_of_chips.setter
    def number_of_chips(self, new_number_of_chips):
        print("Number of chips cannot be changed")
        
        
    ################################
    # Number of captures property
    ################################
    @property
    def number_of_captures_str(self):
        return str(self.__number_of_captures)
    
    @property
    def number_of_captures(self):
        return self.__number_of_captures
    
    @number_of_captures.setter
    def number_of_captures(self, new_number_of_captures):
        try:
            if int(new_number_of_captures) > 0:
                self.__number_of_captures = new_number_of_captures
            else:
                print("Number of captures not accepted")
        except (TypeError, ValueError):
            print("Time gating setting not valid")
            

    ################################
    # Clock frequency property
    ################################
    @property
    def clock_frequency_str(self):
        return str(self.__clock_frequency)
    
    @property
    def clock_frequency(self):
        return self.__clock_frequency
    
    @clock_frequency.setter
    def clock_frequency(self, new_clock_frequency):
        try:
            new_clock_frequency = float(new_clock_frequency)
            if (new_clock_frequency >= 20e6) and (new_clock_frequency <= 100e6):
                self.__clock_frequency = new_clock_frequency
                self.__period = 1/self.__clock_frequency
            else:
                print("Clock frequency not accepted")
        except (TypeError, ValueError):
            print("Clock frequency not valid")
            

    ################################
    # Period property
    ################################
    @property
    def period_str(self):
        return str(self.__period)
    
    @property
    def period(self):
        return self.__period
    
    @period.setter
    def period(self, new_period):
        print("Period cannot be set directly")
            
            
    ################################
    # VCSEL setting property
    ################################
    @property
    def vcsel_setting_str(self):
        return str(self.__vcsel_setting)
    
    @property
    def vcsel_setting(self):
        return self.__vcsel_setting
    
    @vcsel_setting.setter
    def vcsel_setting(self, new_vcsel_setting):
        try:
            new_vcsel_setting = int(new_vcsel_setting)
            if (new_vcsel_setting >= 0) and (new_vcsel_setting <= 3):
                self.__vcsel_setting = new_vcsel_setting
            else:
                print("VCSEL setting not accepted")
        except (TypeError, ValueError):
            print("VCSEL setting not valid")
            
            
    ################################
    # Time gating setting property
    ################################
    @property
    def time_gating_setting_str(self):
        return str(self.__time_gating_setting)
    
    @property
    def time_gating_setting(self):
        return self.__time_gating_setting
    
    @time_gating_setting.setter
    def time_gating_setting(self, new_time_gating_setting):
        try:
            new_time_gating_setting = float(new_time_gating_setting)
            if (new_time_gating_setting >= 0.0) and (new_time_gating_setting <= 25.0):
                self.__time_gating_setting = new_time_gating_setting
                self.__delay = self.__period*1e9 + 150e-3 + self.__time_gating_setting - 2
            else:
                print("Time gating setting not accepted")
        except (TypeError, ValueError):
            print("Time gating setting not valid")
            
    
    ################################
    # Measurements per pattern property
    ################################
    @property
    def measurements_per_pattern_str(self):
        return str(self.__measurements_per_pattern)
    
    @property
    def measurements_per_pattern(self):
        return self.__measurements_per_pattern
    
    @measurements_per_pattern.setter
    def measurements_per_pattern(self, new_measurements_per_pattern):
        try:
            new_measurements_per_pattern = int(new_measurements_per_pattern)
            if (new_measurements_per_pattern >= 1800) and (new_measurements_per_pattern < 32768):
                self.__measurements_per_pattern = new_measurements_per_pattern
            else:
                print("Measurements per pattern setting not accepted")
        except (TypeError, ValueError):
            print("Measurements per pattern not valid")
            
            
    ################################
    # Patterns per frame property
    ################################
    @property
    def patterns_per_frame_str(self):
        return str(self.__patterns_per_frame)
    
    @property
    def patterns_per_frame(self):
        return self.__patterns_per_frame
    
    @patterns_per_frame.setter
    def patterns_per_frame(self, new_patterns_per_frame):
        try:
            new_patterns_per_frame = int(new_patterns_per_frame)
            if (new_patterns_per_frame > 0) and (new_patterns_per_frame <= 16):
                self.__patterns_per_frame = new_patterns_per_frame
            else:
                print("Patterns per frame setting not accepted")
        except (ValueError, TypeError):
            print("Patterns per frame not valid")

            
    ################################
    # Number of frames property
    ################################
    @property
    def number_of_frames_str(self):
        return str(self.__number_of_frames)
    
    @property
    def number_of_frames(self):
        return self.__number_of_frames
    
    @number_of_frames.setter
    def number_of_frames(self, new_number_of_frames):
        try:
            new_number_of_frames = int(new_number_of_frames)
            if (new_number_of_frames > 0):
                self.__number_of_frames = new_number_of_frames
            else:
                print("Number of frames setting not accepted")
        except (ValueError, TypeError):
            print("Number of frames setting not valid")
            
            
    ################################
    # VCSEL bias property
    ################################
    @property
    def vcsel_bias_str(self):
        return str(self.__vcsel_bias)
    
    @property
    def vcsel_bias(self):
        return self.__vcsel_bias
    
    @vcsel_bias.setter
    def vcsel_bias(self, new_vcsel_bias):
        try:
            new_vcsel_bias = float(new_vcsel_bias)
            if (new_vcsel_bias <= 0.0):
                self.__vcsel_bias = new_vcsel_bias
            else:
                print("VCSEL bias not accepted")
        except (ValueError, TypeError):
            print("VCSEL bias not valid")
        
        
    ################################
    # Laser wavelength property
    ################################
    @property
    def laser_wavelength_str(self):
        return str(self.__laser_wavelength)
    
    @property
    def laser_wavelength(self):
        return self.__laser_wavelength
    
    @laser_wavelength.setter
    def laser_wavelength(self, new_laser_wavelength):
        try:
            new_laser_wavelength = int(new_laser_wavelength)
            if (new_laser_wavelength > 0) and (new_laser_wavelength < 1200):
                self.__laser_wavelength = new_laser_wavelength
            else:
                print("Laser wavelength not accepted")
        except (ValueError, TypeError):
            print("Laser wavelength not valid")
            
            
    ################################
    # Laser power property
    ################################
    @property
    def laser_power_str(self):
        return str(self.__laser_power)
    
    @property
    def laser_power(self):
        return self.__laser_power
    
    @laser_power.setter
    def laser_power(self, new_laser_power):
        try:
            new_laser_power = float(new_laser_power)
            if (new_laser_power >= 0):
                self.__laser_power = new_laser_power
            else:
                print("Laser power not accepted")
        except (ValueError, TypeError):
            print("Laser power not valid")
            
            
    ################################
    # Laser bandwidth property
    ################################
    @property
    def laser_bandwidth_str(self):
        return str(self.__laser_bandwidth)
    
    @property
    def laser_bandwidth(self):
        return self.__laser_bandwidth
    
    @laser_bandwidth.setter
    def laser_bandwidth(self, new_laser_bandwidth):
        try:
            new_laser_bandwidth = int(new_laser_bandwidth)
            if (new_laser_bandwidth > 0):
                self.__laser_bandwidth = new_laser_bandwidth
            else:
                print("Laser bandwidth not accepted")
        except (ValueError, TypeError):
            print("Laser bandwidth not valid")
            
            
    ################################
    # Fiber type property
    ################################
    @property
    def fiber_type_str(self):
        return self.__fiber_type
    
    @property
    def fiber_type(self):
        return self.__fiber_type
    
    @fiber_type.setter
    def fiber_type(self, new_fiber_type):
        try:
            self.__fiber_type = str(new_fiber_type)
        except (TypeError, ValueError):
            print("Fiber type string not valid")
            
            
    ################################
    # Other equipment property
    ################################
    @property
    def other_equipment_str(self):
        return self.__other_equipment
    
    @property
    def other_equipment(self):
        return self.__other_equipment
    
    @other_equipment.setter
    def other_equipment(self, new_other_equipment):
        try:
            self.__other_equipment = str(new_other_equipment)
        except (TypeError, ValueError):
            print("Other equipment string not valid")
            
            
    ################################
    # Participant name property
    ################################
    @property
    def participant_name_str(self):
        return self.__participant_name
    
    @property
    def participant_name(self):
        return self.__participant_name
    
    @participant_name.setter
    def participant_name(self, new_participant_name):
        try:
            self.__participant_name = str(new_participant_name)
        except (TypeError, ValueError):
            print("Participant name string not valid")
            
            
    ################################
    # Test type property
    ################################
    @property
    def test_type_str(self):
        return self.__test_type
    
    @property
    def test_type(self):
        return self.__test_type
    
    @test_type.setter
    def test_type(self, new_test_type):
        try:
            self.__test_type = str(new_test_type)
        except (TypeError, ValueError):
            print("Test type string not valid")
            
            
    ################################
    # Test geometry property
    ################################
    @property
    def test_geometry_str(self):
        return self.__test_geometry
    
    @property
    def test_geometry(self):
        return self.__test_geometry
    
    @test_geometry.setter
    def test_geometry(self, new_test_geometry):
        try:
            self.__test_geometry = str(new_test_geometry)
        except (TypeError, ValueError):
            print("Test geometry string not valid")
            
            
    ################################
    # Patch location property
    ################################
    @property
    def patch_location_str(self):
        return self.__patch_location
    
    @property
    def patch_location(self):
        return self.__patch_location
    
    @patch_location.setter
    def patch_location(self, new_patch_location):
        try:
            self.__patch_location = str(new_patch_location)
        except (TypeError, ValueError):
            print("Patch location string not valid")
            
            
    ################################
    # Phantom number property
    ################################
    @property
    def phantom_number_str(self):
        return self.__phantom_number

    @property
    def phantom_number(self):
        return self.__phantom_number
    
    @phantom_number.setter
    def phantom_number(self, new_phantom_number):
        try:
            self.__phantom_number = str(new_phantom_number)
        except (TypeError, ValueError):
            print("Phantom number string not valid")
            
            
    ################################
    # Solution number property
    ################################
    @property
    def solution_number_str(self):
        return self.__solution_number

    @property
    def solution_number(self):
        return self.__solution_number
    
    @solution_number.setter
    def solution_number(self, new_solution_number):
        try:
            self.__solution_number = str(new_solution_number)
        except (TypeError, ValueError):
            print("Solution number string not valid")
            
            
    ################################
    # ROI size property
    ################################
    @property
    def roi_size_str(self):
        return self.__roi_size

    @property
    def roi_size(self):
        return self.__roi_size
    
    @roi_size.setter
    def roi_size(self, new_roi_size):
        try:
            self.__roi_size = str(new_roi_size)
        except (TypeError, ValueError):
            print("ROI size string not valid")
            
            
    ################################
    # ROI ua property
    ################################
    @property
    def roi_ua_str(self):
        return self.__roi_ua

    @property
    def roi_ua(self):
        return self.__roi_ua
    
    @roi_ua.setter
    def roi_ua(self, new_roi_ua):
        try:
            self.__roi_ua = str(new_roi_ua)
        except (TypeError, ValueError):
            print("ROI ua string not valid")
            
            
    ################################
    # SPAD voltage property
    ################################
    @property
    def spad_voltage_str(self):
        return str(self.__spad_voltage)
    
    @property
    def spad_voltage(self):
        return self.__spad_voltage
    
    @spad_voltage.setter
    def spad_voltage(self, new_spad_voltage):
        try:
            new_spad_voltage = float(new_spad_voltage)
            if (new_spad_voltage > 27.2) and (new_spad_voltage < 32.2):
                self.__spad_voltage = new_spad_voltage
            else:
                print("SPAD voltage not accepted")
        except (ValueError, TypeError):
            print("SPAD voltage not valid")
            
            
    ################################
    # VRST voltage property
    ################################
    @property
    def vrst_voltage_str(self):
        return str(self.__vrst_voltage)
    
    @property
    def vrst_voltage(self):
        return self.__vrst_voltage
    
    @vrst_voltage.setter
    def vrst_voltage(self, new_vrst_voltage):
        try:
            new_vrst_voltage = float(new_vrst_voltage)
            if (new_vrst_voltage > 0) and (new_vrst_voltage < 5):
                self.__vrst_voltage = new_vrst_voltage
            else:
                print("VRST voltage not accepted")
        except (ValueError, TypeError):
            print("VRST voltage not valid")
            
            
    ################################
    # Subtractor offset property
    ################################
    @property
    def subtractor_offset_str(self):
        return str(self.__subtractor_offset)
    
    @property
    def subtractor_offset(self):
        return self.__subtractor_offset
    
    @subtractor_offset.setter
    def subtractor_offset(self, new_subtractor_offset):
        try:
            new_subtractor_offset = int(new_subtractor_offset)
            new_subtractor_value = self.__base_subtractor_value + new_subtractor_offset
            if (new_subtractor_value >= 0) and (new_subtractor_value < 1024):
                self.__subtractor_offset = new_subtractor_offset
                self.__subtractor_value = new_subtractor_value
            else:
                print("Subtractor offset not accepted")
        except (ValueError, TypeError):
            print("Subtractor offset not valid")
            
            
    ################################
    # Subtractor value property
    ################################
    @property
    def subtractor_value_str(self):
        return str(self.__subtractor_value)
    
    @property
    def subtractor_value(self):
        return self.__subtractor_value
    
    @subtractor_value.setter
    def subtractor_value(self, new_base_subtractor_value):
        try:
            new_base_subtractor_value = int(new_base_subtractor_value)
            if (new_base_subtractor_value >= 0) and (new_base_subtractor_value < 1024):
                self.__base_subtractor_value = new_base_subtractor_value
                
                # Check to see if subtractor offset is acceptable with new base subtractor value
                new_subtractor_value = self.__base_subtractor_value + self.__subtractor_offset
                if (new_subtractor_value >= 0) and (new_subtractor_value < 1024):
                    
                    # If subtractor value is still acceptable after considering offset, accept the value
                    self.__subtractor_value = new_subtractor_value
                    
                else:
                    
                    # If previous subtractor offset is going to cause problems with subtractor value, set offset back to 0 and subtractor to base value
                    self.__subtractor_offset = 0
                    self.__subtractor_value = self.__base_subtractor_value
            else:
                print("Subtractor value not accepted")

        except (ValueError, TypeError):
            print("Subtractor value not valid")
    
    
    ################################
    # Delay property
    ################################
    @property
    def delay_str(self):
        return str(round(self.__delay, 2))
    
    @property
    def delay(self):
        return self.__delay
    
    @delay.setter
    def delay(self, new_delay):
            print("Delay cannot be set directly")
            
            
    ################################
    # Conditions property
    ################################
    @property
    def conditions_str(self):
        return self.__conditions

    @property
    def conditions(self):
        return self.__conditions
    
    @conditions.setter
    def conditions(self, new_conditions):
        try:
            self.__conditions = str(new_conditions)
        except (TypeError, ValueError):
            print("Conditions string not valid")
    
    