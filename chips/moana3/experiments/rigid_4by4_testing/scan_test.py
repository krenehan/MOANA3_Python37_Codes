# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:01:11 2020

The purpose of this script is to verify that the scan chains on both chips are working correctly. 
A sequence of bits are scanned in, then scanned back out. 
If the bits match, the scan chains are working. If they do not match, the scan chains are not working.

@author: Kevin Renehan
"""

# =============================================================================
# Includes
# =============================================================================
from includes import *


# =============================================================================
# Setup
# =============================================================================
# Set number of chips
number_of_chips = 16

# Set row and cell
row         = ['chip_row_'+ str(i) for i in range(number_of_chips)]
cell        = 'multicell_0'

# Number of times to scan data in and out
number_of_scans = 1

# Enable or disable logging to file
Logging = False

# Conditions to print in log file name
conditions = 'test_conditions_here'
date_time=str(datetime.datetime.now())
print(conditions)


# =============================================================================
# Logging Setup
# =============================================================================
# Create the results directory if it does not exist
results_dir = '../../data/scan_tests/'
if Logging:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

# Create the log file name
log_file_name = "%s_%s-%s-%s.txt" % (conditions, date_time[0:10], date_time[11:13], date_time[14:16])

# Open the log file
if Logging:
    log_file = open(results_dir + log_file_name, 'w')
    

# =============================================================================
# Chip Operation Switches
# =============================================================================
# TDC Resolution - True sets TDC to high resolution mode (70ps), False sets TDC to low resolution mode (150ps)
TDCDCBoost = True

# Start/Stop Source - True sets Start/Stop to come from StartExt and StopExt SMAs, False sets Start/Stop to come from SPADs
ExternalStart    = True
ExternalStop     = True

# VCSEL Enable Source - True causes VCSEL to be enabled by setting VCSELEnableExt scan chain bit, False causes VCSEL to be enabled by SEnable signal
VCSELEnableThroughScan = True
VCSELEnableExt = True

# Pattern Reset Sources - Don't touch these :D
PatternResetWithExternalSignal = False # If True, reset pattern through external signal selected below
PatternResetWithTriggerExt = False # If True use TriggerExt; if False use SUpdate


# =============================================================================
# Equipment Setup
# =============================================================================
# Waiting time (between scans)
config_wait = 0.0
read_wait   = 0.2
equip_wait  = 0.5
ldo_wait = 0.5

# Equipment
func_gen        = None
supply_main     = None
supply_aux      = None


try:
    # =============================================================================
    # Platform Setup
    # =============================================================================
    dut = test_platform.TestPlatform("moana3")
    dut.init_fpga(bitfile_path = paths.bitfile_path)
    
    # Print the serial number of the device
    serial_number = dut.fpga_interface.xem.GetSerialNumber()
    print("Serial Number: " + serial_number)
    
    
    # =============================================================================
    # Power Setup - Initialize power supplies
    # =============================================================================
    dut.enable_hvdd_ldo_supply()
    dut.enable_cath_sm_supply()
    time.sleep(ldo_wait)
    
    
    # =============================================================================
    # Begin Experiment
    # =============================================================================
    
    # Issue scan reset and chip reset
    dut.pulse_signal('scan_reset')
    dut.pulse_signal('cell_reset')
    
    # Get bits for scan rows and cells
    scan_bits = [ dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
    
    # Need to configure scan bits for each chip
    for i in range(number_of_chips):
        
        # Configure TDC
        scan_bits[i].TDCStartSelect        = '0'*8 if ExternalStart else '1'*8
        scan_bits[i].TDCStopSelect         = '0'*8 if ExternalStop else '1'*8
        scan_bits[i].TDCDisable            = '11111111'
        scan_bits[i].TDCDCBoost            = '0'*8 if TDCDCBoost else '1'*8
        
        # Configure Pattern Counter
        scan_bits[i].MeasPerPatt           = np.binary_repr(100000, 24)
        scan_bits[i].MeasCountEnable       = '1'
        
        # Configuring Delay Lines
        scan_bits[i].AQCDLLCoarseWord      = np.binary_repr(0, 4)
        scan_bits[i].AQCDLLFineWord        = np.binary_repr(0, 3)
        scan_bits[i].AQCDLLFinestWord      = np.binary_repr(0, 1)
        scan_bits[i].DriverDLLWord         = np.binary_repr(31,5)
        scan_bits[i].ClkFlip               = '0'
        scan_bits[i].ClkBypass             = '0'
        
        # Configure pattern reset signal
        scan_bits[i].PattResetControlledByTriggerExt       = '1' if PatternResetWithTriggerExt else '0'
        scan_bits[i].PattResetExtEnable    = '1' if PatternResetWithExternalSignal else '0'
        
        # Configure VCSELs
        scan_bits[i].VCSELEnableWithScan        = '1' if VCSELEnableExt else '0'
        scan_bits[i].VCSELEnableControlledByScan        = '1' if VCSELEnableThroughScan else '0'
        scan_bits[i].VCSELWave1Enable         = '1'
        scan_bits[i].VCSELWave2Enable         = '0'
        
        # Configure TxData
        scan_bits[i].TestPattEnable        = '0'
        scan_bits[i].TestDataIn            = np.binary_repr(500, 10)
        scan_bits[i].TxDataExtRequestEnable = '0'
        
        scan_bits[i].DynamicConfigEnable = '0'
        
        # Configure subtractor
        scan_bits[i].TimeOffsetWord        = np.binary_repr(12, 10)
        scan_bits[i].SubtractorBypass      = '1'
        
        # Configure SPADs
        scan_bits[i].SPADEnable            = np.binary_repr(0, 64)
        
    # Customization for individual chips can be done below
    # scan_bits[0].VCSELEnableExt = '1'
    
    # Make scan bits for the fpga
    for i in range(number_of_chips):
        dut.commit_scan_chain(row[i])
        time.sleep(config_wait)
    
    # Print scan parameters to log file
    if Logging:
        log_file.write("---------------- Scan Parameters ----------------")
        log_file.write("\n")
        log_file.write("Measurements per Pattern : %d" % int(scan_bits[0].MeasPerPatt, base=2))
        log_file.write("\n")
        log_file.write("Measurement Counter Enable: %d" % int(scan_bits[0].MeasCountEnable, base=2))
        log_file.write("\n")
        log_file.write("Test Pattern Enable: %d" % int(scan_bits[0].TestPattEnable, base=2))
        log_file.write("\n")
        log_file.write("Test Data In: %d" % int(scan_bits[0].TestDataIn, base=2))
        log_file.write("\n")
        log_file.write("TxData External Request Enable: %d" % int(scan_bits[0].TxDataExtRequestEnable, base=2))
        log_file.write("\n")
        log_file.write("Time Offset Word: %d" % int(scan_bits[0].TimeOffsetWord, base=2))
        log_file.write("\n")
        log_file.write("Time Offset Word LSBs: %d" % int(scan_bits[0].TimeOffsetWordLSBs, base=2))
        log_file.write("\n")
        log_file.write("Subtractor Bypass: %d" % int(scan_bits[0].SubtractorBypass, base=2))
        log_file.write("\n")
        log_file.write("Clock Flip: %d" % int(scan_bits[0].ClkFlip, base=2))
        log_file.write("\n")
        log_file.write("Clock Bypass: %d" % int(scan_bits[0].ClkBypass, base=2))
        log_file.write("\n")
        log_file.write("VCSEL Enable Select: %d" % int(scan_bits[0].VCSELEnableSel, base=2))
        log_file.write("\n")
        log_file.write("VCSEL Enable Ext: %d" % int(scan_bits[0].VCSELEnableExt, base=2))
        log_file.write("\n")
        log_file.write("TDC Disabled: %d" % int(scan_bits[0].TDCDisable, base=2))
        log_file.write("\n")
        log_file.write("TDC Status : %d" % int(scan_bits[0].TDCStatus, base=2))
        log_file.write("\n")
        log_file.write("TDC Fine Raw : %s" % scan_bits[0].TDCFineOutRaw)
        log_file.write("\n")
        log_file.write("TDC Coarse Raw : %d" % int(scan_bits[0].TDCCoarseOut, base=2))
        log_file.write("\n")
    
    # Scan in, scan out loop
    for loop in range(number_of_scans):
        print('---------------- Scan {} ----------------'.format(loop))
        
    
        # Read out results
        for i in range(number_of_chips):
            dut.commit_scan_chain(row[i])
            dut.update_scan_chain(row[i], read_wait)
        scan_bits_received = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
    
        # Print results
        for i in range(number_of_chips):
            print("-------- Chip %d --------" % (i+1))
            print("Measurements per Pattern : %d" % int(scan_bits_received[i].MeasPerPatt, base=2))
            print("Test Data In: %d" % int(scan_bits_received[i].TestDataIn, base=2))
            #print("Time Offset Word: %d" % int(scan_bits_received[i].TimeOffsetWord, base=2))
            #print("Time Offset Word LSBs: %d" % int(scan_bits_received[i].TimeOffsetWordLSBs, base=2))
            #print("TDC Disabled: %d" % int(scan_bits_received[i].TDCDisable, base=2))
            
            # Write to log file
            if Logging:
                log_file.write("---------------- Scan %d ----------------" % int(loop))
                log_file.write("\n")
                log_file.write("Measurements per Pattern : %d" % int(scan_bits_received[i].MeasPerPatt, base=2))
                log_file.write("\n")
                log_file.write("Measurement Counter Enable: %d" % int(scan_bits_received[i].MeasCountEnable, base=2))
                log_file.write("\n")
                log_file.write("Test Pattern Enable: %d" % int(scan_bits_received[i].TestPattEnable, base=2))
                log_file.write("\n")
                log_file.write("Test Data In: %d" % int(scan_bits_received[i].TestDataIn, base=2))
                log_file.write("\n")
                log_file.write("TxData External Request Enable: %d" % int(scan_bits_received[i].TxDataExtRequestEnable, base=2))
                log_file.write("\n")
                log_file.write("Time Offset Word: %d" % int(scan_bits_received[i].TimeOffsetWord, base=2))
                log_file.write("\n")
                log_file.write("Time Offset Word LSBs: %d" % int(scan_bits_received[i].TimeOffsetWordLSBs, base=2))
                log_file.write("\n")
                log_file.write("Subtractor Bypass: %d" % int(scan_bits_received[i].SubtractorBypass, base=2))
                log_file.write("\n")
                log_file.write("Clock Flip: %d" % int(scan_bits_received[i].ClkFlip, base=2))
                log_file.write("\n")
                log_file.write("Clock Bypass: %d" % int(scan_bits_received[i].ClkBypass, base=2))
                log_file.write("\n")
                log_file.write("VCSEL Enable Select: %d" % int(scan_bits_received[i].VCSELEnableSel, base=2))
                log_file.write("\n")
                log_file.write("VCSEL Enable Ext: %d" % int(scan_bits_received[i].VCSELEnableExt, base=2))
                log_file.write("\n")
                log_file.write("TDC Disabled: %d" % int(scan_bits_received[i].TDCDisable, base=2))
                log_file.write("\n")
                log_file.write("TDC Status : %d" % int(scan_bits_received[i].TDCStatus, base=2))
                log_file.write("\n")
                log_file.write("TDC Fine Raw : %s" % scan_bits_received[i].TDCFineOutRaw)
                log_file.write("\n")
                log_file.write("TDC Coarse Raw : %d" % int(scan_bits_received[i].TDCCoarseOut, base=2))
                log_file.write("\n")

finally:
    print("Experiment finished")
    # dut.disable_hvdd_ldo_supply()
    if Logging:
        print("Closing log file")
        log_file.close()
    print("Closing FPGA")
    dut.fpga_interface.xem.Close()
