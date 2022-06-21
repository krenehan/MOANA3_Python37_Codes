# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:21:28 2021

Data logging class for generating log files and data files. 
This file is meant to standardize the way that log files are generated so that logging remains consistent across experiments. 


@author: Kevin Renehan
"""

import os
import pandas as pd


class DataLogger:
    
    # Name of text file containing information about data files
    __description_file_name = 'description.csv'
    
    # Path to data folder
    __path_to_data_folder = '../../data/'
    
    # Descirption file information
    __description_header = None
    __description_row = ''
    __last_index = 0
    __separator = ','
    
    __data_file_name = ''
    
    # Status variables
    __experiment_set = False
    __experiment = 0
    __mode = 0
    __header_info_written = False

    # Data collection modes
    capture = 0
    stream = 1
    
    # Experiment types
    generic = 0
    phantom_with_solution = 1
    phantom_with_roi = 2
    ppg_with_laser = 3
    ppg_with_vcsel = 4
    
    
    # ===========================================================
    # Constructor
    # ===========================================================
    def __init__(self, logging_directory=None, experiment='generic', mode='capture', verbose=False):
        
        # The logging directory must be specified to initialize the class, default is the name of the experiment directory copied into the data folder
        if logging_directory is None:
            self.logging_directory = os.path.abspath(self.__path_to_data_folder + os.path.split(os.getcwd())[1]) + '/'
        else: 
            self.logging_directory = str(logging_directory)
            
        # Set the experiment type
        self.__set_experiment(experiment, mode)
            
        # Set the verbose variable
        self.__verbose = verbose
            
        # Assemble the full path to the description file
        self.__description_file_full_path = self.logging_directory + self.__description_file_name
        
        # Read the description file or create it if it does not exist
        self.__check_logging_directory_existence()
        self.__check_description_file_existence()
        

    # ===========================================================
    # Called by constructor to check that a logging directory exists, and if it does not, try to create it
    # ===========================================================
    def __check_logging_directory_existence(self):
        '''Check the existence of the logging directory'''
        if not os.path.exists(self.logging_directory):
            if self.__verbose:
                print("Making logging directory at " + str(self.logging_directory))
            os.mkdir(self.logging_directory)
        if os.path.exists(self.logging_directory):
            if self.__verbose:
                print("Found existing logging directory at " + str(self.logging_directory))
            return True
        else:
            print("Could not create logging directory")
            raise IOError
            
    
    # ===========================================================
    # Called by constructor to set experiment type and data collection mode
    # ===========================================================
    def __set_experiment(self, experiment, mode):
        '''Set the experiment type to determine what type of log file will be generated'''
        
        # Set the experiment type
        if experiment == 'generic':
            self.__experiment = self.generic
        elif experiment == 'phantom_with_solution':
            self.__experiment = self.phantom_with_solution
        elif experiment == 'phantom_with_roi':
            self.__experiment = self.phantom_with_roi
        elif experiment == 'ppg_with_laser':
            self.__experiment = self.ppg_with_laser
        elif experiment == 'ppg_with_vcsel':
            self.__experiment = self.ppg_with_vcsel
        else:
            print("Experiment type not valid")
            raise Exception
            
        # Set the data collection mode
        if mode == 'capture':
            self.__mode = self.capture
        elif mode == 'stream':
            self.__mode = self.stream
        else:
            print("Data collection mode not valid")
            raise Exception
            
        # Indicate that the experiment type has been set
        self.__experiment_set = True 
        

    # ===========================================================
    # Called by constructor to check the existence of the description file
    # ===========================================================
    def __check_description_file_existence(self):
        '''Check the existence of the description file, create if needed'''
        if not os.path.exists(self.__description_file_full_path):
            self.__create_new_description_file()
        else:
            self.__read_description_file()
            
            
    # ===========================================================
    # Reads an existing description file
    # ===========================================================
    def __read_description_file(self):
        '''Read the existing description file'''
        
        if self.__verbose:
            print("Reading existing description file at " + str(self.__description_file_full_path))
        
        # Read the file
        df = pd.read_csv(self.__description_file_full_path, sep=self.__separator)
        
        # Grab the last index and existing header of the description file
        self.__description_header = [ col for col in df.columns]
        self.__last_index = int(df['Index'][len(df['Index'])-1])
        
        if self.__verbose:
            print("Header is " + str(self.__description_header))
            print("Last Index " + str(self.__last_index))
            

    # ===========================================================
    # Creates a new description file with appropriate column titles
    # ===========================================================
    def __create_new_description_file(self):
        '''Create a new description file'''
        
        if self.__verbose:
            print("Making new description file at " + str(self.__description_file_full_path))
        
        # Retrieve the appropriate header
        self.__get_header()
        
        # Create the file
        desc_file = open(self.__description_file_full_path, 'w')
        for entry in range(len(self.__description_header)):
            desc_file.write(self.__description_header[entry])
            if entry == len(self.__description_header)-1:
                desc_file.write('\n')
            else:
                desc_file.write(self.__separator)
        desc_file.close()
        
        # Propagate relevant information
        self.__last_index = -1
        

    # ===========================================================
    # Writes a new row in the description file
    # ===========================================================
    def write_description_file_row(self, header_dict):
        '''Set the header structure'''
        
        if self.__header_info_written:
            print("Header info has already been written")
            print("Skipping call to set_header_info")
        
        if self.__verbose:
            print("Checking header structure")
        
        # Add Index column to the description file
        self.__description_row += str(self.__last_index + 1) + self.__separator
        
        # Keep track of how many categories were found
        found = 0
        
        # Look through each piece of info in the description header
        for entry in range(1, len(self.__description_header)):
                
            # If this is the stream variable, we update it
            if self.__description_header[entry] == 'Stream':
            
                # If we find 'Stream' we write out the setting
                if self.__mode == self.stream:
                    self.__description_row += 'True'
                else:
                    self.__description_row += 'False'
            
            # Check to see if the dictionary category is in the header
            elif self.__description_header[entry] in header_dict:
                
                if self.__verbose:
                    print("Found " + self.__description_header[entry] + " in dictionary")
                
                # Increment found
                found += 1
            
                # add to the description row
                self.__description_row += header_dict[self.__description_header[entry]]
                    
            else:
                
                # Tell that the category was not found in the input
                print("Value not given for " + self.__description_header[entry])
                    
            # Add separator
            if entry == len(self.__description_header) - 1:
                self.__description_row += '\n'
            else:
                self.__description_row += self.__separator
                
        if self.__verbose:
            print("Found " + str(found) + " fields")
                
        # Indicate if extra columns were found
        if found < len(header_dict):
            print("Extra categories detected in header")
            raise Exception
        
        # Write the row
        handle = open(self.__description_file_full_path, 'a')
        handle.write(self.__description_row)
        handle.close()
        
        # Record that header info has been written
        self.__header_info_written = True
    

    # ===========================================================
    # Select the appropriate header based on experiment type
    # ===========================================================
    def __get_header(self):
        '''Get the header dependent on experiment type'''
        
        # Set the experiment type
        if self.__experiment == self.generic:
            self.__description_header = [ \
                            'Index', \
                            'Notes', \
                            'Date', \
                            'Time', \
                            'Number Of Chips', \
                            'Delay', \
                            'Clock Frequency', \
                            'Number of Frames', \
                            'Patterns per Frame', \
                            'Measurements per Pattern', \
                            'Subtractor Value', \
                            'ClkFlip', \
                            'Driver Setting', \
                            'SPAD Voltage', \
                            'VRST Voltage', \
                            'VCSEL Bias', \
                            'Pattern Pipe', \
                            'Stream', \
                           ]
                
        elif self.__experiment == self.phantom_with_solution:
            self.__description_header = [ \
                            'Index', \
                            'Notes', \
                            'Date', \
                            'Time', \
                            'Number Of Chips', \
                            'Phantom' \
                            'Solution' \
                            'Delay', \
                            'Clock Frequency', \
                            'Number of Frames', \
                            'Patterns per Frame', \
                            'Measurements per Pattern', \
                            'Subtractor Value', \
                            'ClkFlip', \
                            'Driver Setting', \
                            'SPAD Voltage', \
                            'VRST Voltage', \
                            'VCSEL Bias', \
                            'Pattern Pipe', \
                            'Stream', \
                            ]
            
        elif self.__experiment == self.phantom_with_roi:
            self.__description_header = [ \
                            'Index', \
                            'Notes', \
                            'Date', \
                            'Time', \
                            'Number Of Chips', \
                            'Phantom' \
                            'ROI Size' \
                            'ROI uA' \
                            'Delay', \
                            'Clock Frequency', \
                            'Number of Frames', \
                            'Patterns per Frame', \
                            'Measurements per Pattern', \
                            'Subtractor Value', \
                            'ClkFlip', \
                            'Driver Setting', \
                            'SPAD Voltage', \
                            'VRST Voltage', \
                            'VCSEL Bias', \
                            'Pattern Pipe', \
                            'Stream', \
                            ]
        
        elif self.__experiment == self.ppg_with_laser:
            self.__description_header = [ \
                            'Index', \
                            'Notes', \
                            'Date', \
                            'Time', \
                            'Number Of Chips', \
                            'Laser Power', \
                            'Geometry', \
                            'Location', \
                            'Wavelength' \
                            'Bandwidth', \
                            'Delay', \
                            'Clock Frequency', \
                            'Number of Frames', \
                            'Patterns per Frame', \
                            'Measurements per Pattern', \
                            'Subtractor Value', \
                            'ClkFlip', \
                            'Driver Setting', \
                            'SPAD Voltage', \
                            'VRST Voltage', \
                            'Pattern Pipe', \
                            'Stream', \
                            ]
        
        elif self.__experiment == self.ppg_with_vcsel:
            self.__description_header = [ \
                            'Index', \
                            'Notes', \
                            'Date', \
                            'Time', \
                            'Number Of Chips', \
                            'Laser Power', \
                            'Geometry', \
                            'Location', \
                            'Wavelength' \
                            'Bandwidth', \
                            'Delay', \
                            'Clock Frequency', \
                            'Number of Frames', \
                            'Patterns per Frame', \
                            'Measurements per Pattern', \
                            'Subtractor Value', \
                            'ClkFlip', \
                            'Driver Setting', \
                            'SPAD Voltage', \
                            'VRST Voltage', \
                            'VCSEL Bias', \
                            'Pattern Pipe', \
                            'Stream', \
                            ]

        
    # ===========================================================
    # Write to the data file
    # ===========================================================
    def write_to_data_file(self, data):
        '''Write information to the data file'''
        
        # Determine if this is a stream
        if self.__description_header:
            pass
        