from includes import *
from decimal import Decimal
import random
import numpy


# =============================================================================
# Setup
# =============================================================================
# Set chip number (only 2 chips supported in separate pipe readout mode)
number_of_chips = 2

if number_of_chips > 2:
    print("--------- Only 2 chips supported for datatx test ---------")
    raise Exception

# Set row and cell
row         = ['chip_row_'+ str(i) for i in range(number_of_chips)]
cell        = 'multicell_0'

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
results_dir = '../../data/DataTx_tests/'
if Logging:
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

# Create the log file name
log_file_name = "%s_%s-%s-%s.csv" % (conditions, date_time[0:10], date_time[11:13], date_time[14:16])

# Log file header
if Logging:
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
dut = test_platform.TestPlatform("moana2")
dut.init_fpga(bitfile_path = paths.bitfile_path, refclk_freq = 50e6, tx_refclk_freq = 50e6/4, init_pll = True)

try:
    # =============================================================================
    # Frame parameters
    # =============================================================================
    meas_per_patt                   = 20000
    patt_per_frame                  = 2
    number_of_frames                = 2
    
    
    # =============================================================================
    # Power Setup - Initialize power supplies
    # =============================================================================
    # Enable power level shifter
    dut.enable_power_level_shifter()
    
    dut.enable_vdd_sm_supply()
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
        # Configuring TDC
        scan_bits[i].TDCStartSelect        = '11111110' if ExternalStart else '1'*8
        scan_bits[i].TDCStopSelect         = '0'*8 if ExternalStop else '1'*8
        scan_bits[i].TDCDisable            = '0'*8
        scan_bits[i].TDCDCBoost            = '0' if TDCDCBoost else '1'
        
        
        # Configure Pattern Counter
        scan_bits[i].MeasPerPatt           = np.binary_repr(meas_per_patt, 15)
        scan_bits[i].MeasCountEnable       = '1'
        
        # Configuring Delay Lines
        word = 47
        coarse = (word & 0b1111000) >> 3
        fine = word & 0b111
        scan_bits[i].AQCDLLCoarseWord      = np.binary_repr(coarse, 4)
        scan_bits[i].AQCDLLFineWord        = np.binary_repr(fine, 3)
        scan_bits[i].DriverDLLWord         = np.binary_repr(1 << 3, 4)
        scan_bits[i].ClkFlip               = '1'
        scan_bits[i].ClkBypass             = '0'
        
        # Configure pattern reset signal
        scan_bits[i].PattResetExtSel       = '1' if PatternResetWithTriggerExt else '0'
        scan_bits[i].PattResetExtEnable    = '1' if PatternResetWithExternalSignal else '0'
        
        # Configure VCSELs
        scan_bits[i].VCSELEnableExt        = '1' if VCSELEnableExt else '0'
        scan_bits[i].VCSELEnableSel        = '1' if VCSELEnableThroughScan else '0'
        scan_bits[i].VCSELWave1Sel         = '1'
        scan_bits[i].VCSELWave2Sel         = '1'
        
        # Configure TxData
        scan_bits[i].TestPattEnable        = '1'
        scan_bits[i].TestDataIn            = np.binary_repr(0, 10)
        scan_bits[i].TxDataExtRequestEnable = '0'
        
        # Configure subtractor
        scan_bits[i].TimeOffsetWord        = np.binary_repr(0, 7)
        scan_bits[i].TimeOffsetWordLSBs    = np.binary_repr(0, 24)
        scan_bits[i].SubtractorBypass      = '1'
        
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
        
    # Test pattern in, test pattern out loop
    for DataIn in range(0, 1023, 8):
        
        # Console header
        print("------------ Test Pattern Data: {} ------------".format(DataIn))
        
        for i in range(number_of_chips):
            
            # Set Test Data In
            scan_bits[i].TestDataIn            = np.binary_repr(DataIn, 10)
            
            # Make scan bits for the fpga
            dut.commit_scan_chain(row[i])
            time.sleep(config_wait)
        
        # Update FSM settings
        pattern_pipe = [ [0]* number_of_chips]
        dut.FrameController.send_frame_data( pattern_pipe,      \
                                            number_of_chips, \
                                            number_of_frames,   \
                                            patt_per_frame,     \
                                            meas_per_patt       )
        
        # Run capture
        dut.FrameController.run_capture()
        
        # Check FIFO Status
        # dut.check_fifo_status(first_target=2, second_target=3, verbose=True)
    
        # Read the FIFOs
        data = [dut.read_fifo_data(i, number_of_frames, patt_per_frame) for i in range(number_of_chips)]
     
        # Figure out if the test was passed
        test_passed = [True for i in range(number_of_chips)]
        for i in range(number_of_chips):
            for frame in range(1, number_of_frames):
                for packet in range(180):
                    packet_data = data[i][frame*228*8+24+10*packet:frame*228*8+24+10*(packet+1)]
                    if (int(packet_data, base = 2) != DataIn):
                        test_passed[i] = False
                        break
                if test_passed[i] == False:
                    break
        
        # Print results
        for i in range(number_of_chips):
            if (test_passed[i]):
                print("Chip {} passed with test data {}".format(i, DataIn))
            else:
                print("Chip {} failed with test data {}".format(i, DataIn))
            
        # Log results
        if Logging:
            log_file.write(str(int(DataIn)), + ',')
            for i in range(number_of_chips):
                log_file.write(str(test_passed[i]))
                if i != number_of_chips-1:
                    log_file.write(',')
            log_file.write('\n')
            

finally:
    print("Closing FPGA")
    # dut.disable_vdd_sm_supply()
    dut.fpga_interface.xem.Close()
    if Logging:
        print("Closing log file")
        log_file.close()
    
