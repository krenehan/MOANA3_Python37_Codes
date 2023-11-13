# import the PYVISA module
import pyvisa
import time
from numpy import average
from decimal import Decimal

class KeysightE36312A:
    def __init__(self, wait = 0.5): #gpib_address = 5, wait = 0.5):
        self.rm = pyvisa.ResourceManager()
        self.rm.list_resources()
        # self.gpib = self.rm.open_resource("GPIB::%d" % (gpib_address))
        self.myinst = self.rm.open_resource('USB0::0x2A8D::0x1102::MY59182248::0::INSTR')

        self.wait = wait
        
        # Channels
        self.CH1_OUTPUT = 1
        self.CH2_OUTPUT = 2
        self.CH3_OUTPUT = 3

        # Output Voltage (V)
        self.OUTPUT_VOLTAGE_CH1_MAX = 6
        self.OUTPUT_CURRENT_CH_MAX = 25        
        
        # Output Current (A)
        self.OUTPUT_CURRENT_CH1_MAX = 5
        self.OUTPUT_CURRENT_CH_MAX = 1
        
        
    def Close(self):
        print ("Closing Keysight E36312A")
        self.rm.close()
        
    def ClearInstrument(self):
        self.myinst.write("CL")
        time.sleep(self.wait)    
        
    def ChannelSelect(self, channel):
        if (channel > self.CH3_OUTPUT) or (channel < self.CH1_OUTPUT):
            print("Not an output channel")      
        else:
            self.myinst.write(":INSTrument:NSELect" + " " + str(channel))
                              
    def ChannelEnable(self, ch_enable):
        if (ch_enable):
            self.myinst.write(":OUTPut:STATe 1")        
        else:
            self.myinst.write(":OUTPut:STATe 0")    
    
    def SetOPCurrent(self, current, channel):
        if (channel > self.CH3_OUTPUT) or (channel < self.CH1_OUTPUT):
            print("Not an output channel")
        elif (channel == 1) and (current > self.OUTPUT_CURRENT_CH1_MAX): 
            print("The maximun current cannot exceed 5A for channel 1")
        elif (channel == 2) and (current > self.OUTPUT_CURRENT_CH_MAX):
            print("The maximun current cannot exceed 1A for this channel") 
        elif (channel == 3) and (current > self.OUTPUT_CURRENT_CH_MAX):
            print("The maximun current cannot exceed 1A for this channel")     
        else:
            self.myinst.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % current )
        time.sleep(self.wait)
            
    def SetOPvoltage(self, voltage,channel):
        if (channel > self.CH3_OUTPUT) or (channel < self.CH1_OUTPUT):
            print("Not an output channel")  
        else:
            self.myinst.write(':SOURce:VOLTage:PROTection:LEVel:AMPLitude' + " " + str(voltage))
        time.sleep(self.wait)    
        
    def Setvoltage(self, voltage,channel):
        if (channel > self.CH3_OUTPUT) or (channel < self.CH1_OUTPUT):
            print("Not an output channel")
        elif (channel == 1) and (voltage > self.OUTPUT_VOLTAGE_CH1_MAX): 
            print("The maximun current cannot exceed 5A for channel 1")
        elif (channel == 2) and (voltage > self.OUTPUT_VOLTAGE_CH_MAX):
            print("The maximun current cannot exceed 1A for this channel") 
        elif (channel == 3) and (voltage > self.OUTPUT_VOLTAGE_CH_MAX):
            print("The maximun current cannot exceed 1A for this channel")   
        else:
            self.myinst.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % voltage)
        time.sleep(self.wait)     
        
        
    # def PrintError(self, str_byte):
    #     byte = int(str_byte)
    #     if (byte & (1 << self.UNRECOGNIZED_COMMAND_ERROR)):
    #         print "Unrecognized command"
    #     if (byte & (1 << self.WRONG_NUMBER_OF_PARAMETERS_ERROR)):
    #         print "Wrong number of parameters"
    #     if (byte & (1 << self.VALUE_OUT_OF_RANGE_ERROR)):
    #         print "Value out of range"
    #     if (byte & (1 << self.WRONG_MODE_ERROR)):
    #         print "Wrong mode for this command"
    #     if (byte & (1 << self.DELAY_LINKAGE_ERROR)):
    #         print "Delay linkage error"
    #     if (byte & (1 << self.DELAY_RANGE_ERROR)):
    #         print "Delay range error"
    #     if (byte & (1 << self.DATA_CORRUPTED_ERROR)):
    #         print "Data corrupted"
     

# if __name__=='__main__':s
#     s = KeysightE36312A(gpib_address=5, wait=0.5)
    #for channel in range(self.T0_OUTPUT,self.CD_OUTPUT):
    #    time.sleep(1)
    #    s.SetOutputMode(channel)
    #    s.SetOutputAmplitude(channel, 1.8)
    #    s.SetOutputOffset(channel, 0.0)

