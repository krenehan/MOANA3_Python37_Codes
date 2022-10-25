from includes import *
from decimal import Decimal
import random
import numpy
import time


# =============================================================================
# Setup
# =============================================================================
# Set chip number
number_of_chips = 16

# Set row and cell
row         = ['chip_row_'+ str(i) for i in range(number_of_chips)]
cell        = 'multicell_0'

# Enable or disable logging to file
logging = False

# Conditions to print in log file name
conditions = 'test_conditions_here'
date_time=str(datetime.datetime.now())
print(conditions)


# =============================================================================
# Logging Setup
# =============================================================================
# Create the results directory if it does not exist
results_dir = '../../data/DataTx_tests/'
if logging:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

# Create the log file name
log_file_name = "%s_%s-%s-%s.csv" % (conditions, date_time[0:10], date_time[11:13], date_time[14:16])

# Log file header
if logging:
    log_file = open(results_dir + log_file_name, 'w')
    log_file.write('Test Pattern'+',')
    for i in range(number_of_chips):
        log_file.write('Chip ' + str(i) + ' Passed')
        if i != number_of_chips-1:
            log_file.write(',')
    log_file.write('\n')

# =============================================================================
# Chip Operation Switches
# =============================================================================
# TDC Resolution - True sets TDC to high resolution mode (70ps), False sets TDC to low resolution mode (150ps)
TDCDCBoost = False

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
    meas_per_patt                   = 500000
    patt_per_frame                  = 1
    number_of_frames                = 1
    period                              = round(1/refclk_freq*1e9, 1)
    pad_captured_mask               = 0b1111111111111111

    
    
    # =============================================================================
    # Power-up chip and reset
    # =============================================================================
    print("Powering on...")
    time.sleep(ldo_wait)
    print("Power on done!")
    
    # Issue scan reset
    print("Resetting hardware...")
    dut.pulse_signal('scan_reset')
    dut.pulse_signal('cell_reset')
    print("Reset done!")
    
    # =============================================================================
    # Begin Experiment
    # =============================================================================
    # Issue scan reset and chip reset
    dut.pulse_signal('scan_reset')
    dut.pulse_signal('cell_reset')
    
    # Configuring Digital Core
    scan_bits = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
    
    for i in range(number_of_chips):
            
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
        
    # Test pattern in, test pattern out loop
    for DataIn in (682, 682, 682):#range(1, 1023, 8):
        
        # Console header
        print("------------ Test Pattern Data: " + np.binary_repr(DataIn, 10) + " ------------")
        
        for i in range(number_of_chips):
            
            # Set Test Data In
            scan_bits[i].TestDataIn            = np.binary_repr(DataIn, 10)
            
            # Make scan bits for the fpga
            dut.commit_scan_chain(row[i])
            time.sleep(config_wait)
        
        # Update FSM settings
        pattern_pipe = np.zeros((patt_per_frame, number_of_chips), dtype=int)
        dut.FrameController.send_frame_data( pattern_pipe,      \
                                            number_of_chips, \
                                            number_of_frames,   \
                                            patt_per_frame,     \
                                            meas_per_patt,
                                            pad_captured_mask)
        
        # Run capture
        # dut.FrameController.set_fsm_bypass()
        # time.sleep(4*meas_per_patt*1/12e6)
        # dut.FrameController.unset_fsm_bypass()
        dut.FrameController.run_capture()
    
        # Read the FIFOs
        dut.read_master_fifo_data(packet)
        
        # Work directly with receive array
        receive_array = np.flip(np.reshape(packet.receive_array, (number_of_chips, number_of_frames*patt_per_frame*150)), axis=0)

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
                    # print("Packet data is " + str(int(packet_data, base=2)) + " and should be " + str(DataIn))
                    # print("Packet data is " + packet_data + " and should be " + str(np.binary_repr(DataIn, 10)))
                    if (int(packet_data, base = 2) != DataIn):
                        test_passed[chip] = False
                        break
                if test_passed[chip] == False:
                    break
                        
        # Print passing chips
        print("Chips (", end='')
        for i in range(number_of_chips):
            if test_passed[i]:
                print(str(i) + ", ", end='')        
        print(") passed")
              
        # Print failing chips
        print("Chips (", end='')
        for i in range(number_of_chips):
            if not test_passed[i]:
                print(str(i) + ", ", end='')        
        print(") failed")
            
        # Log results
        if logging:
            log_file.write(str(int(DataIn)), + ',')
            for i in range(number_of_chips):
                log_file.write(str(test_passed[i]))
                if i != number_of_chips-1:
                    log_file.write(',')
            log_file.write('\n')

finally:

        print("Closing FPGA")
        dut.fpga_interface.xem.Close()
        if logging:
            print("Closing log file")
            log_file.close()
    
