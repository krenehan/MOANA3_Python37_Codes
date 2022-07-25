from includes import *
import matplotlib.pyplot as plt
from copy import deepcopy


# =============================================================================
# Top-level parameters
# =============================================================================

# Number of captures per time gating setting
captures = 1

# Number of chips
number_of_chips = 16

# VCSEL bias setting
clk_freq                            = 50e6
vcsel_bias                          = 1.4
vcsel_setting                       = 2

# List of time gating values to iterate through
time_gate_list = [0, ]


# Test conditions to propagate to log file
conditions = 'dummy'

# Use to keep track of time
time_init = 0.0
time_recorded = False


# =============================================================================
# Test settings
# Integration time = meas_per_patt * 1/clk_freq * patt_per_frame * number_of_frames
# =============================================================================
meas_per_patt                       = 50000
patt_per_frame                      = 1
number_of_frames                    = 1
tx_refclk_freq                      = 12.5e6
pad_captured_mask                   = 0b1
clk_flip                            = True
spad_voltage                        = 27.7
vrst_voltage                        = 3.3

# Report integration time
integration_time = round(meas_per_patt * 1/clk_freq * patt_per_frame * number_of_frames * 1000, 1)
print("Integration time is " + str(integration_time) + " ms")


# =============================================================================
# Create an emitter pattern
# =============================================================================
pattern_pipe =  np.zeros((patt_per_frame, number_of_chips), dtype=bool)
# pattern_pipe[0][0] = True


# =============================================================================
# Top-level options
# =============================================================================
# Enabling this will export data to log file 
logging = False

# Enabling this will show the plots as data is collected
plotting = True

# Enabling this will show the scan settings so that they can be verified
print_scan_results = False

# These options control the clock level shifter. Leave these alone for the time being.
use_clock_level_shifter = True
clock_input_through_level_shifter = True
clock_output_through_level_shifter = False

# TDC source - should be left as False, False for normal operation
external_start    = False
external_stop     = False

# Enabling this will allow for VCSEL to be enabled through the scan chain
vcsel_enable_through_scan = False


# =============================================================================
# Plotting options
# =============================================================================
# Fast mode overrides all othe plot settings and optimizes processing for fast collection of data
fast_mode = False 

# Raw plotting shows bins instead of time on the x-axis
raw_plotting = True

# Enabling this shows the peak counts in the displayed histogram
show_peak = False

# Enabling this plots count data in log scale
log_plots = False

# Enabling this shows information about chip settings associated with the plotted data
show_plot_info = False

# Enabling this fixes the y-axis at a max value
fix_y_max = False
y_max_value = 500

    
# =============================================================================
# Main gating sweep loop
# =============================================================================
for time_gate_value in time_gate_list:
    
    # Print conditions and time gate value
    vcsel_condition = "vcsel" + str(round(vcsel_bias, 2)).replace('.', 'p')
    clk_condition = "clk" + str(int(clk_freq / 1e6)) + "MHz"
    time_gate_condition = str(time_gate_value) + "ns"
    full_conditions = conditions + "_" + vcsel_condition + "_" + clk_condition + "_" + time_gate_condition
    print("Conditions: " + full_conditions)
    
    # Waiting times
    config_wait  = 0.3
    ldo_wait = 0.5
    
    
    # =============================================================================
    # Logging Setup
    # =============================================================================
    if logging:
        # Grab the current date and time
        date_time=str(datetime.datetime.now())
        
        # Create the results directory
        results_dir = '../../data/flex_pulseox/'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # Create log_file_name
        log_file_name = "%s_%s-%s-%s.csv" % (full_conditions, date_time[0:10], date_time[11:13], date_time[14:16])
        
        # File header
        header =       'Time (s)' + ','+ 'Delay'+','
        for i in range(number_of_chips):
            header = header + 'FIFO ' + str(i) + ' Data' + ','
        header = header + \
                               'Clock Frequency'            + ',' + \
                               'Number of Frames'           + ',' + \
                               'Patterns per Frame'         + ',' + \
                               'Measurements per Pattern'   + ',' + \
                               'Subtractor Value'           + ',' + \
                               'ClkFlip'                    + ',' + \
                               'Driver Setting'             + ',' + \
                               'SPAD Voltage'               + ',' + \
                               'VRST Voltage'               + ',' + \
                               'VCSEL Bias'                 + ',' + \
                               'Pattern Pipe'               + '\n'
        log_file = open(results_dir + log_file_name, 'w')
        log_file.write(header)
    
    
    # =============================================================================
    # Equipment Setup
    # =============================================================================
    func_gen        = None
    supply_main     = None
    supplt_aux      = None
    time.sleep(config_wait)
    
    
    # =============================================================================
    # Test settings that are dynamically updated or stay constant
    # =============================================================================
    subtractor_value                    = int(round((1/clk_freq) * 0.5 / 70e-12, 0)) -50
    period                              = round(1/clk_freq*1e9, 1)
    number_of_bins                      = 150
    bin_size                            = 12
    gating_delay                        = period + 150e-3 + time_gate_value -2
    
    
    # =============================================================================
    # Initialize the data packet
    # =============================================================================
    packet = DataPacket.DataPacket(number_of_chips, number_of_frames, patt_per_frame, meas_per_patt, period, compute_mean=True)

    
    # =============================================================================
    # Data Plotter Setup
    # =============================================================================
    data_plotter_created = False
    if plotting:
        
        # Instantiate the MultipleDataPlotter
        data_plotter = MultipleDataPlotter.MultipleDataPlotter( packet, time_limits=[0,period*3/4], number_of_chips_to_plot=None)
        data_plotter_created = True
        
        # Setup
        data_plotter.set_subtractor_value(subtractor_value)        
        
        # Plot options
        data_plotter.set_vcsel_setting(vcsel_setting)
        data_plotter.set_raw_plotting(raw_plotting)
        data_plotter.set_show_peak(show_peak)
        data_plotter.set_plot_logarithmic(log_plots)
        data_plotter.set_show_plot_info(show_plot_info)
        data_plotter.set_fix_y_max(fix_y_max, y_max_value)
        data_plotter.set_fast_mode(fast_mode, 0.001)
    
    
    # =============================================================================
    # Test Platform setup
    # =============================================================================
    # Instantiate test platform
    dut = test_platform.TestPlatform("moana3")
    
    # Program the FPGA
    dut.init_fpga(bitfile_path = paths.bitfile_path)
    dut.fpga_interface.xem.ResetFPGA()
    # Print the serial number of the device
    serial_number = dut.fpga_interface.xem.GetSerialNumber()
    print("Serial Number: " + serial_number)

    # Setup the delay line
    dut.DelayLine.set_clk_flip(clk_flip)
    bypass, coarse, fine = dut.DelayLine.set_delay_line(gating_delay)
    time_gating_delay = dut.DelayLine.get_delay(coarse, fine)
    
    if plotting:
        
        # Propagate settings to MultipleDataPlotter
        data_plotter.set_coarse_fine([coarse]*number_of_chips, [fine]*number_of_chips)
        data_plotter.set_gate_delay([time_gating_delay]*number_of_chips)
    
    
    # =============================================================================
    # Begin scan and capture
    # =============================================================================
    try:

        # =============================================================================
        # Configure level shifter
        # =============================================================================
        if use_clock_level_shifter:
            dut.enable_clock_level_shifter()
            if clock_input_through_level_shifter:
                dut.set_clock_level_shifter_for_clock_input()
            elif clock_output_through_level_shifter:
                dut.set_clock_level_shifter_for_clock_output()
            else:
                dut.disable_clock_level_shifter()
        else:
            dut.disable_clock_level_shifter()


        # =============================================================================
        # Power-up chip and reset
        # =============================================================================
        print("Powering on...")
        # dut.enable_vdd_sm_supply()
        # dut.enable_hvdd_ldo_supply()
        time.sleep(ldo_wait)
        
        # Issue scan reset
        dut.pulse_signal('scan_reset')
        dut.pulse_signal('cell_reset')
        
        
        # =============================================================================
        # Scan chain configuration
        # =============================================================================
        print("Configuring scan chains...")
     
        
        # Create scan bits
        row         = ['chip_row_'+ str(i) for i in range(number_of_chips)]
        cell        = 'multicell_0'
        scan_bits = [ dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
        
        for i in range(number_of_chips):
            
            # Configure TDC
            scan_bits[i].TDCStartSelect        = '01111111' 
            scan_bits[i].TDCStopSelect         = '0'*8 
            scan_bits[i].TDCDisable            = '01111111'
            scan_bits[i].TDCDCBoost            = '01111111' 
            
            
            # Configure Pattern Counter
            scan_bits[i].MeasPerPatt           = np.binary_repr(meas_per_patt, 24)
            scan_bits[i].MeasCountEnable       = '1'
            
            # Configuring Delay Lines
            dword = 3
            scan_bits[i].AQCDLLCoarseWord      = np.binary_repr( (dword&0b11110000) >> 4, 4)
            scan_bits[i].AQCDLLFineWord        = np.binary_repr((dword&0b1110) >> 1, 3)
            scan_bits[i].AQCDLLFinestWord      = np.binary_repr((dword&0b1), 1)
            scan_bits[i].DriverDLLWord         = np.binary_repr(5, 5)
            scan_bits[i].ClkFlip               = '0'
            scan_bits[i].ClkBypass             = '0'
            
            # Configure pattern reset signal
            scan_bits[i].PattResetControlledByTriggerExt       = '0' 
            scan_bits[i].PattResetExtEnable    = '0'
            
            # Configure VCSELs
            scan_bits[i].VCSELEnableWithScan        = '1' 
            scan_bits[i].VCSELEnableControlledByScan        = '1' 
            scan_bits[i].VCSELWave1Enable         = '1'
            scan_bits[i].VCSELWave2Enable         = '1'
            
            # Configure TxData
            scan_bits[i].TestPattEnable        = '1'
            scan_bits[i].TestDataIn            = np.binary_repr(2, 10)
            scan_bits[i].TxDataExtRequestEnable = '0'
            
            # Configure subtractor
            scan_bits[i].TimeOffsetWord        = np.binary_repr(354, 10)
            scan_bits[i].SubtractorBypass      = '0'
            
            scan_bits[i].DynamicConfigEnable = '0'
            
            # Configure SPADs
            scan_bits[i].SPADEnable            = '0'*64
        
        
        # Make scan bits for the fpga
        for i in range(number_of_chips):
            dut.commit_scan_chain(row[i])
            time.sleep(config_wait)
            
        # Read out results
        for i in range(number_of_chips):
            dut.update_scan_chain(row[i], config_wait)
        scan_bits_received = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
        
        # Print results of scan out if requested
        if print_scan_results:
            for i in range(number_of_chips):
                print( "-------- Chip %d --------" % i)
                print( "Measurements per Pattern : %d" % int(scan_bits_received[i].MeasPerPatt, base=2))
                print( "Measurement Counter Enable: %d" % int(scan_bits_received[i].MeasCountEnable, base=2))
                print( "Test Pattern Enable: %d" % int(scan_bits_received[i].TestPattEnable, base=2))
                print( "Test Data In: %d" % int(scan_bits_received[i].TestDataIn, base=2))
                print( "TxData External Request Enable: %d" % int(scan_bits_received[i].TxDataExtRequestEnable, base=2))
                print( "Time Offset Word: %d" % int(scan_bits_received[i].TimeOffsetWord, base=2))
                print( "Time Offset Word LSBs: %d" % int(scan_bits_received[i].TimeOffsetWordLSBs, base=2))
                print( "Subtractor Bypass: %d" % int(scan_bits_received[i].SubtractorBypass, base=2))
                print( "Clock Flip: %d" % int(scan_bits_received[i].ClkFlip, base=2))
                print( "Clock Bypass: %d" % int(scan_bits_received[i].ClkBypass, base=2))
                print( "VCSEL Enable Select: %d" % int(scan_bits_received[i].VCSELEnableSel, base=2))
                print( "VCSEL Enable Ext: %d" % int(scan_bits_received[i].VCSELEnableExt, base=2))
                print( "VCSEL Wavelength 1: %d" % int(scan_bits_received[i].VCSELWave1Sel, base=2))
                print( "VCSEL Wavelength 2: %d" % int(scan_bits_received[i].VCSELWave2Sel, base=2))
                print( "TDC Disabled: %d" % int(scan_bits_received[i].TDCDisable, base=2))
                print( "TDC Status : %d" % int(scan_bits_received[i].TDCStatus, base=2))
                print( "TDC Fine Raw : %s" % scan_bits_received[i].TDCFineOutRaw)
                print( "TDC Coarse Raw : %d" % int(scan_bits_received[i].TDCCoarseOut, base=2))
        
        print("Done configuring")

        # =============================================================================
        # Send information to frame controller prior to capture
        # =============================================================================
        # Update FSM settings
        dut.FrameController.send_frame_data( pattern_pipe,      \
                                            number_of_chips, \
                                            number_of_frames,   \
                                            patt_per_frame,     \
                                            meas_per_patt,
                                            pad_captured_mask )

        
        # =============================================================================
        # Final chip reset before capture starts
        # =============================================================================
        dut.pulse_signal('cell_reset')
        dut.reset_fifos()
        time.sleep(config_wait)


        # =============================================================================
        # Image capture loop
        # =============================================================================
        for i in range(captures):
            
            if not time_recorded:
                time_init = time.time()
                timestamp = 0.0
                time_recorded = True
            else:
                timestamp = time.time() - time_init                
            
            # Run capture
            dut.check_fifo_data_counts()
            dut.FrameController.run_capture()
            
            
            # Run capture
            # dut.FrameController.set_fsm_bypass()
            # time.sleep(4*meas_per_patt*1/12e6)
            # dut.FrameController.unset_fsm_bypass()
            
            dut.check_fifo_data_counts()

            
            # Read the data
            dut.read_master_fifo_data(packet)

 
            # Update the plot
            if plotting:
                data_plotter.update_plot() 
                
            # Write to log file
            if logging:
                log_data = str(timestamp) + ',' + str(time_gating_delay) + ','
                for chip in range(number_of_chips):
                    log_data = log_data + data[chip] + ','
                log_data = log_data +  \
                                       str(clk_freq)                + ',' + \
                                       str(number_of_frames)        + ',' + \
                                       str(patt_per_frame)          + ',' + \
                                       str(meas_per_patt)           + ',' + \
                                       str(subtractor_value)        + ',' + \
                                       str(int(clk_flip))           + ',' + \
                                       str(vcsel_setting)           + ',' + \
                                       str(spad_voltage)            + ',' + \
                                       str(vrst_voltage)            + ',' + \
                                       str(vcsel_bias)              + ',' + \
                                       str(pipe_pattern)            + '\n'
                log_file.write(log_data)
            
            # # Uncomment for step-through debug process
            # print("Capture " + str(i))
            # dut.check_fifo_data_counts()
            # if i == 0:
            #     dut.read_master_fifo_data(packet)
            # if i % 10 == 0:
            #     input()

            
        # Print frame rate
        # print("Frame Rate is " + str(int(i/timestamp)) + " Hz")
    
    # =============================================================================
    # Disable supplies, close plots, log files, and FPGA on exit
    # =============================================================================
    finally:
        # dut.disable_hvdd_ldo_supply()
        print("Closing FPGA")
        dut.fpga_interface.xem.Close()
        if data_plotter_created:
            data_plotter.close()
        if logging:
            print("Closing log file")
            log_file.close()
