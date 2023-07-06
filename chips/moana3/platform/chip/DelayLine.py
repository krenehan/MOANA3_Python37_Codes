# -*- coding: utf-8 -*-
"""
Created on Sun May 31 19:07:53 2020

@author: Dell-User
"""



# ===========================================================
# DelayLine class to abstract from complexities of delay line
# ===========================================================
class DelayLine:
    
    # Status bits
    __clock_specified = False
    
    # Internal clock period
    __clk_period_ns = 10.0
    
    # Clock duty cycle
    __clk_duty_cycle = 0.5
    
    # Clock phase times
    __clk_positive_time_ns = 5.0
    __clk_negative_time_ns = 5.0
            
    # Internal clock flip bit
    __clk_flip = False
    __clk_flip_set_manually = False
    
    # Fixed, minimum delay of delay line with bypass bit set
    __base_delay_ns = 1.945
    
    
    ##########################################################################################################################
    ##########################################################################################################################
    #                                               PROPERTY DEFINITIONS                                                     #
    ##########################################################################################################################
    ##########################################################################################################################


    # ===========================================================
    # clk_flip property
    # ===========================================================
    @property
    def clk_flip(self):
        return self.__clk_flip
    
    @clk_flip.setter
    def clk_flip(self, new):
        self.__clk_flip = bool(new)
        self.__clk_flip_set_manually = True
        
        
    # ===========================================================
    # clk_period_ns property
    # ===========================================================
    @property 
    def clk_period_ns(self):
        return self.__clk_period_ns
    
    @clk_period_ns.setter
    def clk_period_ns(self, new):
        raise DelayLineException("clk_period_ns can only be set through specify_clock")
        
        
    # ===========================================================
    # clk_period_ns property
    # ===========================================================
    @property 
    def clk_duty_cycle(self):
        return self.__clk_duty_cycle
    
    @clk_duty_cycle.setter
    def clk_duty_cycle(self, new):
        raise DelayLineException("clk_duty_cycle can only be set through specify_clock")
        
        
    # ===========================================================
    # clk_positive_time_ns property
    # ===========================================================
    @property 
    def clk_positive_time_ns(self):
        return self.__clk_positive_time_ns
    
    @clk_positive_time_ns.setter
    def clk_positive_time_ns(self, new):
        raise DelayLineException("clk_positive_time_ns can only be set through specify_clock")
        
        
    # ===========================================================
    # clk_negative_time_ns property
    # ===========================================================
    @property 
    def clk_negative_time_ns(self):
        return self.__clk_negative_time_ns
    
    @clk_negative_time_ns.setter
    def clk_negative_time_ns(self, new):
        raise DelayLineException("clk_negative_time_ns can only be set through specify_clock")
        
        
    # ===========================================================
    # clk_negative_time_ns property
    # ===========================================================
    @property 
    def base_delay_ns(self):
        return self.__base_delay_ns
    
    @base_delay_ns.setter
    def base_delay_ns(self, new):
        raise DelayLineException("base_delay_ns cannot be modified")
        
        
    ##########################################################################################################################
    ##########################################################################################################################
    #                                               USER FACING FUNCTIONS                                                    #
    ##########################################################################################################################
    ##########################################################################################################################
    
    
    # ===========================================================
    # Specify the clock 
    # ===========================================================
    def specify_clock(self, period_ns, duty_cycle):
        '''
        Specify the clock going to the chip so that the delay line can be set correctly.

        Parameters
        ----------
        period_ns : float
            Period of the clock, specified in nanoseconds. A 100MHz clock would have period_ns = 10.0.
        duty_cycle : float
            duty cycle of the clock, specified as a decimal between 0.0 and 1.0 (non-inclusive). A 100MHz clock with t+ = 6ns and t- = 4ns would have duty_cycle = 0.6.

        Raises
        ------
        DelayLineException
            Any invalid parameters or incorrect usage of functions will cause a DelayLineException.

        Returns
        -------
        None.

        '''
        
        # Check that clock period is specified in ns
        if period_ns < 1.0:
            raise DelayLineException("Clock period should be specified in nanoseconds")
        else:
            self.__clk_period_ns = float(period_ns)
            
        # Check that duty cycle is between 0 and 1
        if (duty_cycle > 0) and (duty_cycle < 1):
            self.__clk_duty_cycle = float(duty_cycle)
        else:
            raise DelayLineException("Duty cycle must be between 0 and 1")
            
        # Calculate clock times
        self.__clk_positive_time_ns = self.__clk_period_ns * self.__clk_duty_cycle
        self.__clk_negative_time_ns = self.__clk_period_ns * (1.0 - self.__clk_duty_cycle)
        
        # Update status bit
        self.__clock_specified = True
        
        
    # ===========================================================
    # Get the delay of the delay line
    # ===========================================================
    def get_delay(self, clk_flip, coarse, fine, finest):
        
        # Set clock flip
        if clk_flip:
            print("run clk flip function")
            func = self.__get_setting_clk_flip
        else:
            func = self.__get_setting
        
        # Start with 0 delay
        delay = 0.0
        
        # Search
        while func(delay)[0:3] != (coarse, fine, finest):
            
            # If setting does not match, we increment the delay
            delay = delay + 0.025
    
        # Get the delay of the result
        clk_flip, coarse, fine, finest, actual_delay = self.get_setting(delay)
        print("{}, {}, {}, {}".format(clk_flip, coarse, fine, finest))
        
        # Return the actual delay
        return actual_delay
    
    
    # ===========================================================
    # Set the delay line
    # ===========================================================
    def get_setting(self, requested_delay_ns):
        '''
        Get the setting corresponding to a certain delay

        Parameters
        ----------
        requested_delay_ns : float
            The delay requested from the delay line, specified in nanoseconds. 

        Raises
        ------
        DelayLineException
            Raised when delay value is too large for delay line.

        Returns
        -------
        clk_flip : bool
            Clock flip bit for delay line.
        coarse : int
            Coarse code for delay line.
        fine : int
            Fine code for delay line.
        finest : int
            Finest code for delay line.
        actual_delay_ns : float
            The actual delay of the returned setting, specified in nanoseconds.

        '''
        
        # Check that clock has been specified
        if not self.__clock_specified:
            raise DelayLineException("specify_clock() must be called prior to get_setting()")
            
        # Increment the requested delay slightly (this ensures that get_setting returns same code)
        requested_delay_ns += 0.01
                
        # Determine if clk_flip should be inferred, or it it was set manually by user
        if not self.__clk_flip_set_manually:
            
            # Determine if delay value is large enough to use clock flip
            clk_flip_has_slack = (requested_delay_ns - self.__base_delay_ns - self.__clk_positive_time_ns) > 0
            if clk_flip_has_slack:
                self.__clk_flip = True
            else:
                self.__clk_flip = False
        
        # Get the delay line code
        if self.__clk_flip:
            coarse, fine, finest, actual_delay_ns = self.__get_setting_clk_flip(requested_delay_ns)
        else:
            coarse, fine, finest, actual_delay_ns = self.__get_setting(requested_delay_ns)
            
        # Return
        return self.__clk_flip, coarse, fine, finest, actual_delay_ns
            
        
    ##########################################################################################################################
    ##########################################################################################################################
    #                                                 INTERNAL FUNCTIONS                                                     #
    ##########################################################################################################################
    ##########################################################################################################################


    # ===========================================================
    # Set the delay line without clock flip set
    # ===========================================================
    def __get_setting(self, requested_delay_ns):
        
        # Subtract base delay from delay_ns
        adjusted_delay_ns = requested_delay_ns - self.__base_delay_ns
        
        # Find correct delay code
        if (adjusted_delay_ns <= 0.039):
            word = 0
            actual_delay_ns = 0.0 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.097):
            word = 1
            actual_delay_ns = 0.039 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.139):
            word = 2
            actual_delay_ns = 0.097 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.198):
            word = 3
            actual_delay_ns = 0.139 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.238):
            word = 4
            actual_delay_ns = 0.198 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.307):
            word = 5
            actual_delay_ns = 0.238 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.348):
            word = 6
            actual_delay_ns = 0.307 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.405):
            word = 7
            actual_delay_ns = 0.348 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.45):
            word = 8
            actual_delay_ns = 0.405 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.528):
            word = 9
            actual_delay_ns = 0.45 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.566):
            word = 10
            actual_delay_ns = 0.528 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.631):
            word = 11
            actual_delay_ns = 0.566 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.673):
            word = 12
            actual_delay_ns = 0.631 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.73):
            word = 13
            actual_delay_ns = 0.673 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.774):
            word = 14
            actual_delay_ns = 0.73 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.872):
            word = 15
            actual_delay_ns = 0.774 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.921):
            word = 16
            actual_delay_ns = 0.872 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.981):
            word = 17
            actual_delay_ns = 0.921 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.028):
            word = 18
            actual_delay_ns = 0.981 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.088):
            word = 19
            actual_delay_ns = 1.028 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.124):
            word = 20
            actual_delay_ns = 1.088 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.19):
            word = 21
            actual_delay_ns = 1.124 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.234):
            word = 22
            actual_delay_ns = 1.19 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.285):
            word = 23
            actual_delay_ns = 1.234 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.326):
            word = 24
            actual_delay_ns = 1.285 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.406):
            word = 25
            actual_delay_ns = 1.326 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.447):
            word = 26
            actual_delay_ns = 1.406 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.514):
            word = 27
            actual_delay_ns = 1.447 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.555):
            word = 28
            actual_delay_ns = 1.514 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.622):
            word = 29
            actual_delay_ns = 1.555 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.661):
            word = 30
            actual_delay_ns = 1.622 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.78):
            word = 31
            actual_delay_ns = 1.661 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.817):
            word = 32
            actual_delay_ns = 1.78 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.886):
            word = 33
            actual_delay_ns = 1.817 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.931):
            word = 34
            actual_delay_ns = 1.886 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.0):
            word = 35
            actual_delay_ns = 1.931 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.043):
            word = 36
            actual_delay_ns = 2.0 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.108):
            word = 37
            actual_delay_ns = 2.043 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.144):
            word = 38
            actual_delay_ns = 2.108 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.197):
            word = 39
            actual_delay_ns = 2.144 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.226):
            word = 40
            actual_delay_ns = 2.197 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.296):
            word = 41
            actual_delay_ns = 2.226 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.343):
            word = 42
            actual_delay_ns = 2.296 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.404):
            word = 43
            actual_delay_ns = 2.343 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.449):
            word = 44
            actual_delay_ns = 2.404 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.518):
            word = 45
            actual_delay_ns = 2.449 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.563):
            word = 46
            actual_delay_ns = 2.518 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.681):
            word = 47
            actual_delay_ns = 2.563 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.715):
            word = 48
            actual_delay_ns = 2.681 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.779):
            word = 49
            actual_delay_ns = 2.715 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.826):
            word = 50
            actual_delay_ns = 2.779 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.888):
            word = 51
            actual_delay_ns = 2.826 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.93):
            word = 52
            actual_delay_ns = 2.888 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.003):
            word = 53
            actual_delay_ns = 2.93 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.042):
            word = 54
            actual_delay_ns = 3.003 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.104):
            word = 55
            actual_delay_ns = 3.042 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.142):
            word = 56
            actual_delay_ns = 3.104 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.215):
            word = 57
            actual_delay_ns = 3.142 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.254):
            word = 58
            actual_delay_ns = 3.215 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.311):
            word = 59
            actual_delay_ns = 3.254 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.366):
            word = 60
            actual_delay_ns = 3.311 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.43):
            word = 61
            actual_delay_ns = 3.366 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.474):
            word = 62
            actual_delay_ns = 3.43 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.599):
            word = 63
            actual_delay_ns = 3.474 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.638):
            word = 64
            actual_delay_ns = 3.599 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.701):
            word = 65
            actual_delay_ns = 3.638 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.741):
            word = 66
            actual_delay_ns = 3.701 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.801):
            word = 67
            actual_delay_ns = 3.741 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.845):
            word = 68
            actual_delay_ns = 3.801 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.905):
            word = 69
            actual_delay_ns = 3.845 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.949):
            word = 70
            actual_delay_ns = 3.905 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.01):
            word = 71
            actual_delay_ns = 3.949 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.055):
            word = 72
            actual_delay_ns = 4.01 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.128):
            word = 73
            actual_delay_ns = 4.055 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.173):
            word = 74
            actual_delay_ns = 4.128 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.232):
            word = 75
            actual_delay_ns = 4.173 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.273):
            word = 76
            actual_delay_ns = 4.232 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.331):
            word = 77
            actual_delay_ns = 4.273 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.372):
            word = 78
            actual_delay_ns = 4.331 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.492):
            word = 79
            actual_delay_ns = 4.372 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.523):
            word = 80
            actual_delay_ns = 4.492 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.593):
            word = 81
            actual_delay_ns = 4.523 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.636):
            word = 82
            actual_delay_ns = 4.593 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.699):
            word = 83
            actual_delay_ns = 4.636 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.739):
            word = 84
            actual_delay_ns = 4.699 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.801):
            word = 85
            actual_delay_ns = 4.739 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.844):
            word = 86
            actual_delay_ns = 4.801 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.899):
            word = 87
            actual_delay_ns = 4.844 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.939):
            word = 88
            actual_delay_ns = 4.899 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.021):
            word = 89
            actual_delay_ns = 4.939 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.057):
            word = 90
            actual_delay_ns = 5.021 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.126):
            word = 91
            actual_delay_ns = 5.057 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.17):
            word = 92
            actual_delay_ns = 5.126 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.234):
            word = 93
            actual_delay_ns = 5.17 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.273):
            word = 94
            actual_delay_ns = 5.234 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.395):
            word = 95
            actual_delay_ns = 5.273 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.432):
            word = 96
            actual_delay_ns = 5.395 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.496):
            word = 97
            actual_delay_ns = 5.432 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.537):
            word = 98
            actual_delay_ns = 5.496 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.609):
            word = 99
            actual_delay_ns = 5.537 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.725):
            word = 100
            actual_delay_ns = 5.609 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.797):
            word = 101
            actual_delay_ns = 5.725 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.836):
            word = 102
            actual_delay_ns = 5.797 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.885):
            word = 103
            actual_delay_ns = 5.836 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.919):
            word = 104
            actual_delay_ns = 5.885 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.996):
            word = 105
            actual_delay_ns = 5.919 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.041):
            word = 106
            actual_delay_ns = 5.996 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.104):
            word = 107
            actual_delay_ns = 6.041 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.15):
            word = 108
            actual_delay_ns = 6.104 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.224):
            word = 109
            actual_delay_ns = 6.15 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.263):
            word = 110
            actual_delay_ns = 6.224 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.383):
            word = 111
            actual_delay_ns = 6.263 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.415):
            word = 112
            actual_delay_ns = 6.383 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.479):
            word = 113
            actual_delay_ns = 6.415 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.52):
            word = 114
            actual_delay_ns = 6.479 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.584):
            word = 115
            actual_delay_ns = 6.52 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.628):
            word = 116
            actual_delay_ns = 6.584 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.698):
            word = 117
            actual_delay_ns = 6.628 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.738):
            word = 118
            actual_delay_ns = 6.698 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.799):
            word = 119
            actual_delay_ns = 6.738 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.832):
            word = 120
            actual_delay_ns = 6.799 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.908):
            word = 121
            actual_delay_ns = 6.832 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.946):
            word = 122
            actual_delay_ns = 6.908 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.005):
            word = 123
            actual_delay_ns = 6.946 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.047):
            word = 124
            actual_delay_ns = 7.005 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.112):
            word = 125
            actual_delay_ns = 7.047 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.153):
            word = 126
            actual_delay_ns = 7.112 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.262):
            word = 127
            actual_delay_ns = 7.153 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.299):
            word = 128
            actual_delay_ns = 7.262 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.369):
            word = 129
            actual_delay_ns = 7.299 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.406):
            word = 130
            actual_delay_ns = 7.369 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.472):
            word = 131
            actual_delay_ns = 7.406 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.505):
            word = 132
            actual_delay_ns = 7.472 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.577):
            word = 133
            actual_delay_ns = 7.505 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.614):
            word = 134
            actual_delay_ns = 7.577 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.673):
            word = 135
            actual_delay_ns = 7.614 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.715):
            word = 136
            actual_delay_ns = 7.673 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.795):
            word = 137
            actual_delay_ns = 7.715 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.833):
            word = 138
            actual_delay_ns = 7.795 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.902):
            word = 139
            actual_delay_ns = 7.833 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.936):
            word = 140
            actual_delay_ns = 7.902 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.004):
            word = 141
            actual_delay_ns = 7.936 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.037):
            word = 142
            actual_delay_ns = 8.004 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.162):
            word = 143
            actual_delay_ns = 8.037 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.191):
            word = 144
            actual_delay_ns = 8.162 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.269):
            word = 145
            actual_delay_ns = 8.191 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.303):
            word = 146
            actual_delay_ns = 8.269 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.377):
            word = 147
            actual_delay_ns = 8.303 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.413):
            word = 148
            actual_delay_ns = 8.377 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.478):
            word = 149
            actual_delay_ns = 8.413 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.513):
            word = 150
            actual_delay_ns = 8.478 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.572):
            word = 151
            actual_delay_ns = 8.513 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.606):
            word = 152
            actual_delay_ns = 8.572 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.682):
            word = 153
            actual_delay_ns = 8.606 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.722):
            word = 154
            actual_delay_ns = 8.682 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.796):
            word = 155
            actual_delay_ns = 8.722 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.83):
            word = 156
            actual_delay_ns = 8.796 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.905):
            word = 157
            actual_delay_ns = 8.83 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.938):
            word = 158
            actual_delay_ns = 8.905 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.07):
            word = 159
            actual_delay_ns = 8.938 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.104):
            word = 160
            actual_delay_ns = 9.07 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.172):
            word = 161
            actual_delay_ns = 9.104 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.211):
            word = 162
            actual_delay_ns = 9.172 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.29):
            word = 163
            actual_delay_ns = 9.211 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.327):
            word = 164
            actual_delay_ns = 9.29 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.394):
            word = 165
            actual_delay_ns = 9.327 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.433):
            word = 166
            actual_delay_ns = 9.394 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.493):
            word = 167
            actual_delay_ns = 9.433 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.531):
            word = 168
            actual_delay_ns = 9.493 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.612):
            word = 169
            actual_delay_ns = 9.531 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.643):
            word = 170
            actual_delay_ns = 9.612 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.71):
            word = 171
            actual_delay_ns = 9.643 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.75):
            word = 172
            actual_delay_ns = 9.71 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.822):
            word = 173
            actual_delay_ns = 9.75 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.861):
            word = 174
            actual_delay_ns = 9.822 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.0):
            word = 175
            actual_delay_ns = 9.861 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.032):
            word = 176
            actual_delay_ns = 10.0 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.103):
            word = 177
            actual_delay_ns = 10.032 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.136):
            word = 178
            actual_delay_ns = 10.103 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.208):
            word = 179
            actual_delay_ns = 10.136 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.253):
            word = 180
            actual_delay_ns = 10.208 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.329):
            word = 181
            actual_delay_ns = 10.253 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.365):
            word = 182
            actual_delay_ns = 10.329 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.43):
            word = 183
            actual_delay_ns = 10.365 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.468):
            word = 184
            actual_delay_ns = 10.43 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.542):
            word = 185
            actual_delay_ns = 10.468 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.577):
            word = 186
            actual_delay_ns = 10.542 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.645):
            word = 187
            actual_delay_ns = 10.577 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.681):
            word = 188
            actual_delay_ns = 10.645 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.752):
            word = 189
            actual_delay_ns = 10.681 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.786):
            word = 190
            actual_delay_ns = 10.752 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.884):
            word = 191
            actual_delay_ns = 10.786 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.926):
            word = 192
            actual_delay_ns = 10.884 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.994):
            word = 193
            actual_delay_ns = 10.926 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.027):
            word = 194
            actual_delay_ns = 10.994 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.09):
            word = 195
            actual_delay_ns = 11.027 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.124):
            word = 196
            actual_delay_ns = 11.09 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.201):
            word = 197
            actual_delay_ns = 11.124 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.23):
            word = 198
            actual_delay_ns = 11.201 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.29):
            word = 199
            actual_delay_ns = 11.23 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.311):
            word = 200
            actual_delay_ns = 11.29 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.401):
            word = 201
            actual_delay_ns = 11.311 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.437):
            word = 202
            actual_delay_ns = 11.401 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.51):
            word = 203
            actual_delay_ns = 11.437 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.544):
            word = 204
            actual_delay_ns = 11.51 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.612):
            word = 205
            actual_delay_ns = 11.544 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.644):
            word = 206
            actual_delay_ns = 11.612 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.771):
            word = 207
            actual_delay_ns = 11.644 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.803):
            word = 208
            actual_delay_ns = 11.771 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.873):
            word = 209
            actual_delay_ns = 11.803 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.904):
            word = 210
            actual_delay_ns = 11.873 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.981):
            word = 211
            actual_delay_ns = 11.904 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.014):
            word = 212
            actual_delay_ns = 11.981 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.086):
            word = 213
            actual_delay_ns = 12.014 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.119):
            word = 214
            actual_delay_ns = 12.086 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.178):
            word = 215
            actual_delay_ns = 12.119 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.208):
            word = 216
            actual_delay_ns = 12.178 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.294):
            word = 217
            actual_delay_ns = 12.208 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.326):
            word = 218
            actual_delay_ns = 12.294 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.406):
            word = 219
            actual_delay_ns = 12.326 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.429):
            word = 220
            actual_delay_ns = 12.406 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.507):
            word = 221
            actual_delay_ns = 12.429 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.539):
            word = 222
            actual_delay_ns = 12.507 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.657):
            word = 223
            actual_delay_ns = 12.539 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.689):
            word = 224
            actual_delay_ns = 12.657 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.758):
            word = 225
            actual_delay_ns = 12.689 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.786):
            word = 226
            actual_delay_ns = 12.758 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.868):
            word = 227
            actual_delay_ns = 12.786 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.901):
            word = 228
            actual_delay_ns = 12.868 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.987):
            word = 229
            actual_delay_ns = 12.901 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.013):
            word = 230
            actual_delay_ns = 12.987 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.077):
            word = 231
            actual_delay_ns = 13.013 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.111):
            word = 232
            actual_delay_ns = 13.077 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.192):
            word = 233
            actual_delay_ns = 13.111 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.223):
            word = 234
            actual_delay_ns = 13.192 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.3):
            word = 235
            actual_delay_ns = 13.223 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.328):
            word = 236
            actual_delay_ns = 13.3 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.41):
            word = 237
            actual_delay_ns = 13.328 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.438):
            word = 238
            actual_delay_ns = 13.41 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.587):
            word = 239
            actual_delay_ns = 13.438 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.594):
            word = 240
            actual_delay_ns = 13.587 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.667):
            word = 241
            actual_delay_ns = 13.594 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.696):
            word = 242
            actual_delay_ns = 13.667 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.773):
            word = 243
            actual_delay_ns = 13.696 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.804):
            word = 244
            actual_delay_ns = 13.773 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.883):
            word = 245
            actual_delay_ns = 13.804 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.905):
            word = 246
            actual_delay_ns = 13.883 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.98):
            word = 247
            actual_delay_ns = 13.905 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.011):
            word = 248
            actual_delay_ns = 13.98 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.097):
            word = 249
            actual_delay_ns = 14.011 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.127):
            word = 250
            actual_delay_ns = 14.097 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.199):
            word = 251
            actual_delay_ns = 14.127 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.229):
            word = 252
            actual_delay_ns = 14.199 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.307):
            word = 253
            actual_delay_ns = 14.229 + self.__base_delay_ns
            
        else:
            word = 254
            actual_delay_ns = 14.307 + self.__base_delay_ns
            raise DelayLineException("Delay value is too large")
    
    
        # Calculate coarse and fine words
        coarse =    (word & 0b11110000) >> 4
        fine =      (word & 0b00001110) >> 1
        finest =    (word & 0b00000001)
        
        # Return 
        return coarse, fine, finest, actual_delay_ns
    
    
    # ===========================================================
    # Set the delay line with clock flip set
    # ===========================================================
    def __get_setting_clk_flip(self, requested_delay_ns):
        
        # Subtract the base delay and the positive phase of the clock period
        adjusted_delay_ns = requested_delay_ns - self.base_delay_ns - self.__clk_positive_time_ns
        
        # Find correct delay code
        if (adjusted_delay_ns <= 0.044):
            word = 0
            actual_delay_ns = 0.0 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.106):
            word = 1
            actual_delay_ns = 0.044 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.156):
            word = 2
            actual_delay_ns = 0.106 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.22):
            word = 3
            actual_delay_ns = 0.156 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.262):
            word = 4
            actual_delay_ns = 0.22 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.33):
            word = 5
            actual_delay_ns = 0.262 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.366):
            word = 6
            actual_delay_ns = 0.33 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.424):
            word = 7
            actual_delay_ns = 0.366 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.465):
            word = 8
            actual_delay_ns = 0.424 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.533):
            word = 9
            actual_delay_ns = 0.465 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.584):
            word = 10
            actual_delay_ns = 0.533 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.642):
            word = 11
            actual_delay_ns = 0.584 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.684):
            word = 12
            actual_delay_ns = 0.642 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.747):
            word = 13
            actual_delay_ns = 0.684 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.796):
            word = 14
            actual_delay_ns = 0.747 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.893):
            word = 15
            actual_delay_ns = 0.796 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.935):
            word = 16
            actual_delay_ns = 0.893 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 0.995):
            word = 17
            actual_delay_ns = 0.935 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.038):
            word = 18
            actual_delay_ns = 0.995 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.106):
            word = 19
            actual_delay_ns = 1.038 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.152):
            word = 20
            actual_delay_ns = 1.106 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.214):
            word = 21
            actual_delay_ns = 1.152 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.257):
            word = 22
            actual_delay_ns = 1.214 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.319):
            word = 23
            actual_delay_ns = 1.257 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.36):
            word = 24
            actual_delay_ns = 1.319 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.437):
            word = 25
            actual_delay_ns = 1.36 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.477):
            word = 26
            actual_delay_ns = 1.437 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.54):
            word = 27
            actual_delay_ns = 1.477 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.579):
            word = 28
            actual_delay_ns = 1.54 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.639):
            word = 29
            actual_delay_ns = 1.579 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.689):
            word = 30
            actual_delay_ns = 1.639 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.806):
            word = 31
            actual_delay_ns = 1.689 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.852):
            word = 32
            actual_delay_ns = 1.806 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.915):
            word = 33
            actual_delay_ns = 1.852 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 1.952):
            word = 34
            actual_delay_ns = 1.915 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.022):
            word = 35
            actual_delay_ns = 1.952 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.063):
            word = 36
            actual_delay_ns = 2.022 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.128):
            word = 37
            actual_delay_ns = 2.063 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.176):
            word = 38
            actual_delay_ns = 2.128 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.232):
            word = 39
            actual_delay_ns = 2.176 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.276):
            word = 40
            actual_delay_ns = 2.232 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.339):
            word = 41
            actual_delay_ns = 2.276 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.389):
            word = 42
            actual_delay_ns = 2.339 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.45):
            word = 43
            actual_delay_ns = 2.389 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.491):
            word = 44
            actual_delay_ns = 2.45 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.553):
            word = 45
            actual_delay_ns = 2.491 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.597):
            word = 46
            actual_delay_ns = 2.553 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.712):
            word = 47
            actual_delay_ns = 2.597 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.757):
            word = 48
            actual_delay_ns = 2.712 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.813):
            word = 49
            actual_delay_ns = 2.757 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.856):
            word = 50
            actual_delay_ns = 2.813 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.919):
            word = 51
            actual_delay_ns = 2.856 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 2.968):
            word = 52
            actual_delay_ns = 2.919 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.031):
            word = 53
            actual_delay_ns = 2.968 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.075):
            word = 54
            actual_delay_ns = 3.031 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.128):
            word = 55
            actual_delay_ns = 3.075 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.18):
            word = 56
            actual_delay_ns = 3.128 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.249):
            word = 57
            actual_delay_ns = 3.18 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.287):
            word = 58
            actual_delay_ns = 3.249 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.357):
            word = 59
            actual_delay_ns = 3.287 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.398):
            word = 60
            actual_delay_ns = 3.357 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.468):
            word = 61
            actual_delay_ns = 3.398 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.51):
            word = 62
            actual_delay_ns = 3.468 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.625):
            word = 63
            actual_delay_ns = 3.51 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.667):
            word = 64
            actual_delay_ns = 3.625 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.719):
            word = 65
            actual_delay_ns = 3.667 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.771):
            word = 66
            actual_delay_ns = 3.719 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.83):
            word = 67
            actual_delay_ns = 3.771 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.876):
            word = 68
            actual_delay_ns = 3.83 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.943):
            word = 69
            actual_delay_ns = 3.876 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 3.989):
            word = 70
            actual_delay_ns = 3.943 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.043):
            word = 71
            actual_delay_ns = 3.989 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.084):
            word = 72
            actual_delay_ns = 4.043 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.162):
            word = 73
            actual_delay_ns = 4.084 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.206):
            word = 74
            actual_delay_ns = 4.162 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.263):
            word = 75
            actual_delay_ns = 4.206 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.31):
            word = 76
            actual_delay_ns = 4.263 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.377):
            word = 77
            actual_delay_ns = 4.31 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.415):
            word = 78
            actual_delay_ns = 4.377 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.536):
            word = 79
            actual_delay_ns = 4.415 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.574):
            word = 80
            actual_delay_ns = 4.536 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.637):
            word = 81
            actual_delay_ns = 4.574 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.682):
            word = 82
            actual_delay_ns = 4.637 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.744):
            word = 83
            actual_delay_ns = 4.682 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.788):
            word = 84
            actual_delay_ns = 4.744 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.855):
            word = 85
            actual_delay_ns = 4.788 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.898):
            word = 86
            actual_delay_ns = 4.855 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 4.955):
            word = 87
            actual_delay_ns = 4.898 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.001):
            word = 88
            actual_delay_ns = 4.955 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.072):
            word = 89
            actual_delay_ns = 5.001 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.108):
            word = 90
            actual_delay_ns = 5.072 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.179):
            word = 91
            actual_delay_ns = 5.108 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.215):
            word = 92
            actual_delay_ns = 5.179 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.279):
            word = 93
            actual_delay_ns = 5.215 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.323):
            word = 94
            actual_delay_ns = 5.279 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.448):
            word = 95
            actual_delay_ns = 5.323 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.493):
            word = 96
            actual_delay_ns = 5.448 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.554):
            word = 97
            actual_delay_ns = 5.493 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.6):
            word = 98
            actual_delay_ns = 5.554 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.66):
            word = 99
            actual_delay_ns = 5.6 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.715):
            word = 100
            actual_delay_ns = 5.66 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.778):
            word = 101
            actual_delay_ns = 5.715 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.817):
            word = 102
            actual_delay_ns = 5.778 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.87):
            word = 103
            actual_delay_ns = 5.817 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.91):
            word = 104
            actual_delay_ns = 5.87 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 5.984):
            word = 105
            actual_delay_ns = 5.91 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.027):
            word = 106
            actual_delay_ns = 5.984 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.093):
            word = 107
            actual_delay_ns = 6.027 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.124):
            word = 108
            actual_delay_ns = 6.093 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.192):
            word = 109
            actual_delay_ns = 6.124 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.234):
            word = 110
            actual_delay_ns = 6.192 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.35):
            word = 111
            actual_delay_ns = 6.234 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.398):
            word = 112
            actual_delay_ns = 6.35 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.461):
            word = 113
            actual_delay_ns = 6.398 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.507):
            word = 114
            actual_delay_ns = 6.461 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.574):
            word = 115
            actual_delay_ns = 6.507 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.601):
            word = 116
            actual_delay_ns = 6.574 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.68):
            word = 117
            actual_delay_ns = 6.601 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.709):
            word = 118
            actual_delay_ns = 6.68 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.775):
            word = 119
            actual_delay_ns = 6.709 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.807):
            word = 120
            actual_delay_ns = 6.775 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.884):
            word = 121
            actual_delay_ns = 6.807 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.927):
            word = 122
            actual_delay_ns = 6.884 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 6.993):
            word = 123
            actual_delay_ns = 6.927 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.037):
            word = 124
            actual_delay_ns = 6.993 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.103):
            word = 125
            actual_delay_ns = 7.037 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.139):
            word = 126
            actual_delay_ns = 7.103 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.247):
            word = 127
            actual_delay_ns = 7.139 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.285):
            word = 128
            actual_delay_ns = 7.247 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.344):
            word = 129
            actual_delay_ns = 7.285 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.38):
            word = 130
            actual_delay_ns = 7.344 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.45):
            word = 131
            actual_delay_ns = 7.38 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.49):
            word = 132
            actual_delay_ns = 7.45 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.557):
            word = 133
            actual_delay_ns = 7.49 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.599):
            word = 134
            actual_delay_ns = 7.557 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.657):
            word = 135
            actual_delay_ns = 7.599 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.696):
            word = 136
            actual_delay_ns = 7.657 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.769):
            word = 137
            actual_delay_ns = 7.696 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.805):
            word = 138
            actual_delay_ns = 7.769 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.876):
            word = 139
            actual_delay_ns = 7.805 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.918):
            word = 140
            actual_delay_ns = 7.876 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 7.988):
            word = 141
            actual_delay_ns = 7.918 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.025):
            word = 142
            actual_delay_ns = 7.988 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.151):
            word = 143
            actual_delay_ns = 8.025 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.187):
            word = 144
            actual_delay_ns = 8.151 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.252):
            word = 145
            actual_delay_ns = 8.187 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.299):
            word = 146
            actual_delay_ns = 8.252 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.363):
            word = 147
            actual_delay_ns = 8.299 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.399):
            word = 148
            actual_delay_ns = 8.363 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.467):
            word = 149
            actual_delay_ns = 8.399 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.505):
            word = 150
            actual_delay_ns = 8.467 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.569):
            word = 151
            actual_delay_ns = 8.505 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.606):
            word = 152
            actual_delay_ns = 8.569 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.678):
            word = 153
            actual_delay_ns = 8.606 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.724):
            word = 154
            actual_delay_ns = 8.678 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.775):
            word = 155
            actual_delay_ns = 8.724 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.819):
            word = 156
            actual_delay_ns = 8.775 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.888):
            word = 157
            actual_delay_ns = 8.819 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 8.924):
            word = 158
            actual_delay_ns = 8.888 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.056):
            word = 159
            actual_delay_ns = 8.924 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.087):
            word = 160
            actual_delay_ns = 9.056 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.157):
            word = 161
            actual_delay_ns = 9.087 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.195):
            word = 162
            actual_delay_ns = 9.157 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.265):
            word = 163
            actual_delay_ns = 9.195 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.302):
            word = 164
            actual_delay_ns = 9.265 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.368):
            word = 165
            actual_delay_ns = 9.302 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.399):
            word = 166
            actual_delay_ns = 9.368 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.46):
            word = 167
            actual_delay_ns = 9.399 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.505):
            word = 168
            actual_delay_ns = 9.46 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.571):
            word = 169
            actual_delay_ns = 9.505 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.612):
            word = 170
            actual_delay_ns = 9.571 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.683):
            word = 171
            actual_delay_ns = 9.612 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.723):
            word = 172
            actual_delay_ns = 9.683 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.795):
            word = 173
            actual_delay_ns = 9.723 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.827):
            word = 174
            actual_delay_ns = 9.795 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 9.959):
            word = 175
            actual_delay_ns = 9.827 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.002):
            word = 176
            actual_delay_ns = 9.959 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.063):
            word = 177
            actual_delay_ns = 10.002 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.106):
            word = 178
            actual_delay_ns = 10.063 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.173):
            word = 179
            actual_delay_ns = 10.106 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.212):
            word = 180
            actual_delay_ns = 10.173 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.276):
            word = 181
            actual_delay_ns = 10.212 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.316):
            word = 182
            actual_delay_ns = 10.276 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.372):
            word = 183
            actual_delay_ns = 10.316 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.409):
            word = 184
            actual_delay_ns = 10.372 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.48):
            word = 185
            actual_delay_ns = 10.409 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.522):
            word = 186
            actual_delay_ns = 10.48 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.587):
            word = 187
            actual_delay_ns = 10.522 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.629):
            word = 188
            actual_delay_ns = 10.587 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.703):
            word = 189
            actual_delay_ns = 10.629 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.74):
            word = 190
            actual_delay_ns = 10.703 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.836):
            word = 191
            actual_delay_ns = 10.74 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.868):
            word = 192
            actual_delay_ns = 10.836 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.933):
            word = 193
            actual_delay_ns = 10.868 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 10.973):
            word = 194
            actual_delay_ns = 10.933 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.039):
            word = 195
            actual_delay_ns = 10.973 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.078):
            word = 196
            actual_delay_ns = 11.039 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.153):
            word = 197
            actual_delay_ns = 11.078 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.192):
            word = 198
            actual_delay_ns = 11.153 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.249):
            word = 199
            actual_delay_ns = 11.192 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.311):
            word = 200
            actual_delay_ns = 11.249 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.379):
            word = 201
            actual_delay_ns = 11.311 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.417):
            word = 202
            actual_delay_ns = 11.379 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.488):
            word = 203
            actual_delay_ns = 11.417 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.535):
            word = 204
            actual_delay_ns = 11.488 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.605):
            word = 205
            actual_delay_ns = 11.535 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.639):
            word = 206
            actual_delay_ns = 11.605 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.771):
            word = 207
            actual_delay_ns = 11.639 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.811):
            word = 208
            actual_delay_ns = 11.771 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.877):
            word = 209
            actual_delay_ns = 11.811 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.906):
            word = 210
            actual_delay_ns = 11.877 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 11.979):
            word = 211
            actual_delay_ns = 11.906 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.018):
            word = 212
            actual_delay_ns = 11.979 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.085):
            word = 213
            actual_delay_ns = 12.018 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.123):
            word = 214
            actual_delay_ns = 12.085 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.19):
            word = 215
            actual_delay_ns = 12.123 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.228):
            word = 216
            actual_delay_ns = 12.19 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.31):
            word = 217
            actual_delay_ns = 12.228 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.338):
            word = 218
            actual_delay_ns = 12.31 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.407):
            word = 219
            actual_delay_ns = 12.338 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.447):
            word = 220
            actual_delay_ns = 12.407 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.506):
            word = 221
            actual_delay_ns = 12.447 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.546):
            word = 222
            actual_delay_ns = 12.506 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.668):
            word = 223
            actual_delay_ns = 12.546 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.702):
            word = 224
            actual_delay_ns = 12.668 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.774):
            word = 225
            actual_delay_ns = 12.702 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.808):
            word = 226
            actual_delay_ns = 12.774 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.876):
            word = 227
            actual_delay_ns = 12.808 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.913):
            word = 228
            actual_delay_ns = 12.876 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 12.985):
            word = 229
            actual_delay_ns = 12.913 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.02):
            word = 230
            actual_delay_ns = 12.985 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.084):
            word = 231
            actual_delay_ns = 13.02 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.116):
            word = 232
            actual_delay_ns = 13.084 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.193):
            word = 233
            actual_delay_ns = 13.116 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.232):
            word = 234
            actual_delay_ns = 13.193 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.302):
            word = 235
            actual_delay_ns = 13.232 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.338):
            word = 236
            actual_delay_ns = 13.302 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.408):
            word = 237
            actual_delay_ns = 13.338 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.45):
            word = 238
            actual_delay_ns = 13.408 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.579):
            word = 239
            actual_delay_ns = 13.45 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.607):
            word = 240
            actual_delay_ns = 13.579 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.68):
            word = 241
            actual_delay_ns = 13.607 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.72):
            word = 242
            actual_delay_ns = 13.68 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.796):
            word = 243
            actual_delay_ns = 13.72 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.821):
            word = 244
            actual_delay_ns = 13.796 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.901):
            word = 245
            actual_delay_ns = 13.821 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.928):
            word = 246
            actual_delay_ns = 13.901 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 13.994):
            word = 247
            actual_delay_ns = 13.928 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.025):
            word = 248
            actual_delay_ns = 13.994 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.106):
            word = 249
            actual_delay_ns = 14.025 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.141):
            word = 250
            actual_delay_ns = 14.106 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.213):
            word = 251
            actual_delay_ns = 14.141 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.248):
            word = 252
            actual_delay_ns = 14.213 + self.__base_delay_ns
            
        elif (adjusted_delay_ns <= 14.322):
            word = 253
            actual_delay_ns = 14.248 + self.__base_delay_ns
            
        else:
            word = 254
            actual_delay_ns = 14.322 + self.__base_delay_ns
            raise DelayLineException("Delay value is too large")


        # Calculate coarse and fine words
        coarse =    (word & 0b11110000) >> 4
        fine =      (word & 0b00001110) >> 1
        finest =    (word & 0b00000001)
        
        # Add back to actual_delay_ns
        actual_delay_ns = actual_delay_ns + self.__clk_positive_time_ns
        
        # Return 
        return coarse, fine, finest, actual_delay_ns
    
    
    
    
    
    
class DelayLineException(Exception):
    pass
    


# Runnable
if __name__ == "__main__":
    
    # Instantiate
    d = DelayLine()
    
    # Specify clock for delay line
    d.specify_clock(20, 0.5)
    
    # Find requested delay
    clk_flip, coarse, fine, finest, actual_delay = d.get_setting(20)
    
    
        
    