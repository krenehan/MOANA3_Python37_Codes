from includes import *
from decimal import Decimal
import random
import numpy

# Extra test comment
# =============================================================================
# Setup
# =============================================================================

# Verbose
verbose = False
continuous_mode = True

# Set chip number
number_of_chips = 2

# Set row and cell
row         = ['chip_row_'+ str(i) for i in range(number_of_chips)]
cell        = 'multicell_0'

# Conditions to print in log file name
conditions = 'test_conditions_here'
date_time=str(datetime.datetime.now())
print(conditions)


# =============================================================================
# Chip Operation Switches
# =============================================================================
# TDC Resolution - True sets TDC to high resolution mode (70ps), False sets TDC to low resolution mode (150ps)
TDCDCBoost = True

# Start/Stop Source - True sets Start/Stop to come from StartExt and StopExt SMAs, False sets Start/Stop to come from SPADs
ExternalStart    = False
ExternalStop     = False

# VCSEL Enable Source - True causes VCSEL to be enabled by setting VCSELEnableExt scan chain bit, False causes VCSEL to be enabled by SEnable signal
VCSELEnableThroughScan = True
VCSELEnableExt = True

# Pattern Reset Sources - Don't touch these :D
PatternResetWithExternalSignal = False # If True, reset pattern through external signal selected below
PatternResetWithTriggerExt = False # If True use TriggerExt; if False use SUpdate

# Waiting time (between scans)
config_wait = 0.0
read_wait   = 0.1
equip_wait  = 0.3
ldo_wait = 0.5


# =============================================================================
# Equipment Setup
# =============================================================================
func_gen        = None
supply_main     = None
supplt_aux      = None


# =============================================================================
# Platform Setup - Initialize FPGA and chip
# =============================================================================
refclk_freq = 50e6
dut = test_platform.TestPlatform("moana3")
dut.init_fpga(bitfile_path = paths.bitfile_path, refclk_freq=50e6)

try:
    # =============================================================================
    # Frame parameters
    # =============================================================================
    meas_per_patt                   = 50000
    patt_per_frame                  = 1
    number_of_frames                = 100
    period                          = round(1/refclk_freq*1e9, 1)
    pad_captured_mask               = 0b11    # Keep track of passes and failures
    passed                          = 0
    failed                          = 0
    
    
    # =============================================================================
    # Power Setup - Initialize power supplies
    # =============================================================================
    time.sleep(ldo_wait)
    
    
    # =============================================================================
    # Begin Experiment
    # =============================================================================
    # Issue scan reset and chip reset
    dut.pulse_signal('scan_reset')
    dut.pulse_signal('cell_reset')
    
    # Configuring Digital Core
    scan_bits = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
    
    for i in range(number_of_chips):
        
        # Configure TDC
        scan_bits[i].TDCStartSelect        = '0'*8 if ExternalStart else '1'*8
        scan_bits[i].TDCStopSelect         = '0'*8 if ExternalStop else '1'*8
        scan_bits[i].TDCDisable            = '11111111'
        scan_bits[i].TDCDCBoost            = '0'*8 if TDCDCBoost else '1'*8
        
        
        # Configure Pattern Counter
        scan_bits[i].MeasPerPatt           = np.binary_repr(meas_per_patt, 24)
        scan_bits[i].MeasCountEnable       = '1'
        
        # Configuring Delay Lines
        scan_bits[i].AQCDLLCoarseWord      = np.binary_repr(0, 4)
        scan_bits[i].AQCDLLFineWord        = np.binary_repr(0, 3)
        scan_bits[i].AQCDLLFinestWord      = np.binary_repr(0, 1)
        scan_bits[i].DriverDLLWord         = np.binary_repr(1, 5)
        scan_bits[i].ClkFlip               = '0'
        scan_bits[i].ClkBypass             = '1'
        
        # Configure pattern reset signal
        scan_bits[i].PattResetControlledByTriggerExt       = '1' if PatternResetWithTriggerExt else '0'
        scan_bits[i].PattResetExtEnable    = '1' if PatternResetWithExternalSignal else '0'
        
        # Configure VCSELs
        scan_bits[i].VCSELEnableWithScan        = '1' if VCSELEnableExt else '0'
        scan_bits[i].VCSELEnableControlledByScan        = '1' if VCSELEnableThroughScan else '0'
        scan_bits[i].VCSELWave1Enable         = '1'
        scan_bits[i].VCSELWave2Enable         = '1'
        
        # Configure TxData
        scan_bits[i].TestPattEnable        = '1'
        scan_bits[i].TestDataIn            = np.binary_repr(0, 10)
        scan_bits[i].TxDataExtRequestEnable = '0'
        
        # Configure subtractor
        scan_bits[i].TimeOffsetWord        = np.binary_repr(0, 10)
        scan_bits[i].SubtractorBypass      = '1'
        
        scan_bits[i].DynamicConfigEnable = '0'
        
        # Configure SPADs
        scan_bits[i].SPADEnable            = '0'*64
    
    # Make scan bits for the fpga
    for i in range(number_of_chips):
        dut.commit_scan_chain(row[i])
        time.sleep(config_wait)

    # Read out scan chain
    for i in range(number_of_chips):
        dut.update_scan_chain(row[i], read_wait) 
    scan_bits = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
    
    # Receive array
    packet = DataPacket.DataPacket(number_of_chips, number_of_frames, patt_per_frame, meas_per_patt, period, compute_mean=False)
    
    # Flag for setting fsm bypass
    fsm_bypass_set = False
    
    # Data packets for chips, must be constant when running continuously
    DataIn = (np.random.randint(0, 1023), np.random.randint(0, 1023))
    
    # Run capture and check process
    for c in range(10000):
        
        for i in range(number_of_chips):
            
            print("------------ Capture " + str(c) + ": Chip " + str(i) + " Data " + np.binary_repr(DataIn[i], 10) + " ------------")
            
            # Set Test Data In
            scan_bits[i].TestDataIn            = np.binary_repr(DataIn[i], 10)
            
            # Make scan bits for the fpga
            dut.commit_scan_chain(row[i])
            time.sleep(config_wait)
        
        # Update FSM settings
        dut.FrameController.send_frame_data( number_of_chips, \
                                            number_of_frames,   \
                                            patt_per_frame,     \
                                            meas_per_patt, \
                                            pad_captured_mask)
        # Capture
        if continuous_mode:
            
            if fsm_bypass_set == False:
                dut.check_ram_trigger()
                dut.FrameController.set_fsm_bypass()
                fsm_bypass_set = True
            
            # Wait for ram trigger
            while dut.check_ram_trigger() == False:
                pass
            
        else:
            
            # Run capture
            dut.FrameController.run_capture()
    
        # Read the FIFOs
        dut.read_master_fifo_data(packet)
        
        # Work directly with receive array, reshape to correct size
        receive_array = np.reshape(packet.receive_array, (number_of_frames, patt_per_frame, number_of_chips, 150))
        
        # Transpose so that chip axis comes first
        receive_array = np.transpose(receive_array, axes=(2,0,1,3))
        
        # Flip along chip axis (would normally be every axis, but data is all the same past chip axis)
        receive_array = np.flip(receive_array, axis=(0,))
        
        # Flatten array beyond chip axis
        receive_array = np.reshape(receive_array, (number_of_chips, number_of_frames*patt_per_frame*150))

        # Figure out if the test was passed
        test_passed = [True for chip in range(number_of_chips)]
        for chip in range(number_of_chips):
            
            # Unpack data into bits
            l = []
            for i in range(len(receive_array[chip])):
                l.append(np.binary_repr(receive_array[chip][i], 20))
            data = ''.join(l)
            
            # Check 
            for frame in range(number_of_frames):
                bits_in_frame = patt_per_frame * 3000
                for j in range(300):
                    packet_data = data[frame*bits_in_frame+10*j:frame*bits_in_frame+10*(j+1)]
                    if verbose:
                        print("Packet data is " + str(int(packet_data, base=2)) + " and should be " + str(DataIn[chip]))
                        print("Packet data is " + packet_data + " and should be " + str(np.binary_repr(DataIn[chip], 10)))
                    if (int(packet_data, base = 2) != DataIn[chip]):
                        test_passed[chip] = False
                        break
                if test_passed[chip] == False:
                    break
                        
        # Print passing chips
        print("Chips (", end='')
        for i in range(number_of_chips):
            if test_passed[i]:
                passed = passed + 1
                print(str(i) + ", ", end='')        
        print(") passed")
              
        # Print failing chips
        print("Chips (", end='')
        for i in range(number_of_chips):
            if not test_passed[i]:
                failed = failed + 1
                print(str(i) + ", ", end='')        
        print(") failed")
            

finally:
    print("Passed = " + str(passed))
    print("Failed = " + str(failed))
    print("Closing FPGA")
    dut.fpga_interface.xem.Close()
    
