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
from numpy import empty

class YieldStruct():
    '''Data structure for storing yield information'''
    
    # Constructor
    def __init__(self, number_of_chips):
        
        # Save number of chips
        self.number_of_chips = number_of_chips
        
        # Structures for holding working sources and detectors
        self.working_nir_sources = empty((number_of_chips,), dtype=bool)
        self.working_ir_sources = empty((number_of_chips,), dtype=bool)
        self.detectors = empty((number_of_chips,), dtype=bool)
        
        # Assume true
        self.working_nir_sources.fill(True)
        self.working_ir_sources.fill(True)
        self.detectors.fill(True)
        
        
    ################################
    # Override string method
    ################################ 
    def __str__(self):
        
        # Create string
        s = ''
        
        # Detectors
        s = s + "detectors="
        for c in range(self.number_of_chips):
            if self.detectors[c]:
                s = s + str(c) + ","
        if s[len(s)-1] == ",":
            s = s[0:len(s)-1]
        s = s + '\n'
        
        # Working NIR sources
        s = s + "working_nir_sources="
        for c in range(self.number_of_chips):
            if self.working_nir_sources[c]:
                s = s + str(c) + ","
        if s[len(s)-1] == ",":
            s = s[0:len(s)-1]
        s = s + '\n'
        
        # Working IR sources
        s = s + "working_ir_sources="
        for c in range(self.number_of_chips):
            if self.working_ir_sources[c]:
                s = s + str(c) + ","
        if s[len(s)-1] == ",":
            s = s[0:len(s)-1]
        s = s + '\n'
            
        # Return
        return s
        
        
    ################################
    # Interpret a yield file
    ################################
    def interpret_yield_file(self, filepath):
            
        # Read yield file
        print("Reading yield file at " + str(filepath))
        f = open(filepath, "r")
        ll = f.readlines()
        f.close()
        
        # Interpret line list
        self.__interpret_yield_line_list(ll)
        
        
    ################################
    # Interpret a yield string
    ################################
    def interpret_yield_string(self, yield_string):
            
        # Read yield file
        ll = yield_string.splitlines(keepends=True)
        
        # Interpret line list
        self.__interpret_yield_line_list(ll)
        
        
    ################################
    # Interpret a yield line lis
    ################################
    def __interpret_yield_line_list(self, ll):
        
        # Get values
        def get_vals(l):
            
            # Split the line at the equals sign
            v = l.split('=')
            
            # Check length
            if len(v) <= 1:
                return []
                
            # Select what comes after equals sign if equals sign was found
            v = v[1]
                
            # Split the line further by comma
            v = v.strip().split(',')
            
            # Check length to make sure it wasn't just a comma
            if len(v) <= 1:
                return []
            
            # Remove whitespace
            try:
                v = [int(i.strip()) for i in v]
            except ValueError:
                print("Invalid entry in this line of the yield file: " + str(l))
                return []
            
            # Check to make sure numbers don't fall below 0 or above number_of_chips
            vf = []
            for i in v:
                if (i>=0) and (i<self.number_of_chips):
                    vf.append(i)
                    
            # Sort and remove duplicates
            vf = list(set(vf))
            
            # Return list
            return vf
        
        # Defaults
        new_detectors = []
        new_working_nir_sources = []
        new_working_ir_sources = []
        
        # Go through lines
        for l in ll:
            
            # Find lines
            if 'detectors' in l:
                new_detectors = get_vals(l)
            elif 'working_nir_sources' in l:
                new_working_nir_sources = get_vals(l)
            elif 'working_ir_sources' in l:
                new_working_ir_sources = get_vals(l)
                
        # Update class members
        for c in range(self.number_of_chips):
            self.detectors[c] = c in new_detectors
            self.working_nir_sources[c] = c in new_working_nir_sources
            self.working_ir_sources[c] = c in new_working_ir_sources
            
                
                
# Runnable
if __name__ == "__main__":
    
    # Filepath
    fp = 'C:\\Users\\Dell-User\\Dropbox\\MOANA\\Python\\MOANA3_Python37_Codes\\chips\\moana3\\data\\rigid_4by4_hbo2_testing\\data\\nirsetting4_0p8Virsetting3_1p0V_Trial5\\yield.txt'
    
    y = YieldStruct(16)
    y.interpret_yield_file(fp)
    
    # Create test setup file
    f = open('C:\\Users\\Dell-User\\Desktop\\yield_out.txt', 'w')
    f.write(str(y))
    f.close()
    