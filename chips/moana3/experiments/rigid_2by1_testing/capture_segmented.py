from includes import *
import matplotlib.pyplot as plt
from copy import deepcopy


# =============================================================================
# Top-level parameters
# =============================================================================

# Verbose
verbose = False

# Number of captures per time gating setting
captures = 1000

# Number of chips
number_of_chips = 2

# VCSEL bias setting
clk_freq                            = 50e6
vcsel_bias                          = 1.4
vcsel_setting                       = 2

# List of time gating values to iterate through
time_gate_list = [0, ]


# =============================================================================
# Test settings
# Integration time = meas_per_patt * 1/clk_freq * patt_per_frame * number_of_frames
# =============================================================================
meas_per_patt                       = 50000
patt_per_frame                      = 1
number_of_frames                    = 50
spad_voltage                        = 24.7
vrst_voltage                        = 3.3
pad_captured_mask                   = 0b11

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

# Enabling this will show the plots as data is collected
plotting = True

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
fast_mode = True

# Raw plotting shows bins instead of time on the x-axis
raw_plotting = True

# Enabling this shows the peak counts in the displayed histogram
show_peak = False

# Enabling this plots count data in log scale
log_plots = False

# Enabling this shows information about chip settings associated with the plotted data
show_plot_info = False

# Enabling this fixes the y-axis at a max value
fix_y_max = True
y_max_value = 5000

    
# =============================================================================
# Main gating sweep loop
# =============================================================================
for time_gate_value in time_gate_list:
    
    # Print conditions and time gate value
    vcsel_condition = "vcsel" + str(round(vcsel_bias, 2)).replace('.', 'p')
    clk_condition = "clk" + str(int(clk_freq / 1e6)) + "MHz"
    time_gate_condition = str(time_gate_value) + "ns"
    full_conditions = vcsel_condition + "_" + clk_condition + "_" + time_gate_condition
    print("Conditions: " + full_conditions)
    
    # Waiting times
    config_wait  = 0.3
    ldo_wait = 0.5
    
    
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
    subtractor_value                    = int(round((1/clk_freq) * 0.5 / 65e-12, 0))
    period                              = round(1/clk_freq*1e9, 1)
    number_of_bins                      = 150
    bin_size                            = 12
    requested_delay                     = period + time_gate_value - 2
    
    
    # =============================================================================
    # Initialize the data packet
    # =============================================================================
    packet = DataPacket.DataPacket(number_of_chips, number_of_frames, patt_per_frame, meas_per_patt, period, compute_mean=False)

    
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
    dut.init_fpga(bitfile_path = paths.bitfile_path, refclk_freq=clk_freq)

    # Print the serial number of the device
    serial_number = dut.fpga_interface.xem.GetSerialNumber()
    print("Serial Number: " + serial_number)

    # Setup the delay line
    dut.DelayLine.specify_clock(period, 0.5) 
    clk_flip, coarse, fine, finest, actual_delay_ns = dut.DelayLine.get_setting(requested_delay)
    
    if plotting:
        
        # Propagate settings to MultipleDataPlotter
        data_plotter.set_coarse_fine([coarse]*number_of_chips, [fine]*number_of_chips)
        data_plotter.set_gate_delay([requested_delay]*number_of_chips)
    
    
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
        dut.enable_hvdd_ldo_supply()
        dut.enable_cath_sm_supply()
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
            scan_bits[i].TDCStartSelect        = '0'*8 if external_start else '1'*8
            scan_bits[i].TDCStopSelect         = '0'*8 if external_stop else '1'*8
            scan_bits[i].TDCDisable            = '0'*8
            scan_bits[i].TDCDCBoost            = '0'*8
            
            
            # Configure Pattern Counter
            scan_bits[i].MeasPerPatt           = np.binary_repr(meas_per_patt, 24)
            scan_bits[i].MeasCountEnable       = '1'
            
            
            # Configuring Delay Lines
            scan_bits[i].AQCDLLCoarseWord      = np.binary_repr(coarse, 4)
            scan_bits[i].AQCDLLFineWord        = np.binary_repr(fine, 3)
            scan_bits[i].AQCDLLFinestWord      = np.binary_repr(finest, 1)
            scan_bits[i].DriverDLLWord         = np.binary_repr(4, 5)
                
            scan_bits[i].ClkFlip               = np.binary_repr(clk_flip, 1)
            scan_bits[i].ClkBypass             = '0'
            
            # Configure pattern reset signal
            scan_bits[i].PattResetControlledByTriggerExt       = '0' 
            scan_bits[i].PattResetExtEnable    = '0'
                
            # Configure VCSELs
            scan_bits[i].VCSELWave1Enable         = '1'
            scan_bits[i].VCSELEnableWithScan        = '0'     
            scan_bits[i].VCSELEnableControlledByScan        = '1' 
            scan_bits[i].VCSELWave2Enable         = '0'
            
            # Configure TxData
            scan_bits[i].TestPattEnable        = '0'
            if i == 0:
                scan_bits[i].TestDataIn            = np.binary_repr(10, 10)
            else:
                scan_bits[i].TestDataIn            = np.binary_repr(2**9-1, 10)
            scan_bits[i].TxDataExtRequestEnable = '0'
            
            # Configure subtractor
            scan_bits[i].TimeOffsetWord        = np.binary_repr(subtractor_value, 10)         

            scan_bits[i].SubtractorBypass      = '0'
            
            scan_bits[i].DynamicConfigEnable = '0'
            
            # Configure SPADs
            scan_bits[i].SPADEnable            = '1'*64
        
        # Make scan bits for the fpga
        for i in range(number_of_chips):
            dut.commit_scan_chain(row[i])
            time.sleep(config_wait)
            
        # Read out results
        for i in range(number_of_chips):
            dut.update_scan_chain(row[i], config_wait)
        scan_bits_received = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
        

        # =============================================================================
        # Send information to frame controller prior to capture
        # =============================================================================
        # Update FSM settings
        dut.FrameController.send_frame_data( pattern_pipe,      \
                                            number_of_chips, \
                                            number_of_frames,   \
                                            patt_per_frame,     \
                                            meas_per_patt, \
                                            pad_captured_mask)

        
        # =============================================================================
        # Final chip reset before capture starts
        # =============================================================================
        dut.pulse_signal('cell_reset')
        time.sleep(config_wait)


        # =============================================================================
        # Image capture loop
        # =============================================================================
        for i in range(captures):
            
            # Run capture
            dut.FrameController.run_capture()
            
            # Check counts after capture
            if verbose:
                print("Packets after to capture " + str(i) + ":")
                dut.check_fifo_data_counts()
                
            dut.read_master_fifo_data(packet)
            
            # Check counts before capture
            if verbose:
                print("Packets after read " + str(i) + ":")
                dut.check_fifo_data_counts() 

 
            # Update the plot
            if plotting:
                data_plotter.update_plot() 
                
    
    # =============================================================================
    # Disable supplies, close plots, log files, and FPGA on exit
    # =============================================================================
    finally:
        dut.disable_hvdd_ldo_supply()
        dut.disable_cath_sm_supply()
        print("Closing FPGA")
        dut.fpga_interface.xem.Close()
        if data_plotter_created:
            data_plotter.close()
