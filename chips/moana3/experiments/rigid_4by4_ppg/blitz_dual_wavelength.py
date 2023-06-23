from includes import *
import matplotlib.pyplot as plt
from KeysightE36312A import * 
from copy import deepcopy

# for vs in [4]:
#     sv = 0.8
# for sv in np.arange (4,12,4,dtype = int)/10:
# =============================================================================
# Top-level parameters
# =============================================================================

# Number of captures per time gating setting
number_of_captures = 108

# Number of chips
number_of_chips = 16

# VCSEL bias setting
clk_freq                            = 50e6
nir_vcsel_bias                      = 0.8#sv
nir_vcsel_setting                   = 4#vs
ir_vcsel_bias                      = 1.0#sv
ir_vcsel_setting                   = 3#vs


# List of time gating values to iterate through
time_gate_list = [0.0, ]

#Power Supply setting 

# channel                             = 1
# power_enable                        = True 
# OC_current                          = 0.050
# OV_voltage                          = 4  
# voltage                             = vcsel_bias

# Test conditions to propagate to log file
conditions = "nirsetting" + str(nir_vcsel_setting) + "_" + \
             str(nir_vcsel_bias).replace(".", "p") + "V" + \
             "irsetting" + str(ir_vcsel_setting) + "_" + \
             str(ir_vcsel_bias).replace(".", "p") + "V"


print("================Conditions======================")
print("================================================")
print(conditions)
print("================================================")
print("================================================")

dynamic_mode = True

# =============================================================================
# Test settings
# Integration time = meas_per_patt * 1/clk_freq * patt_per_frame * number_of_frames
# =============================================================================
meas_per_patt                       = 312500
patt_per_frame                      = 32 
number_of_frames                    = 25
tx_refclk_freq                      = 12.5e6
pad_captured_mask                   = 0b1111111101111111
subtractor_offset                   = 0

# Report integration time
integration_time = round(meas_per_patt * 1/clk_freq * patt_per_frame * number_of_frames * 1000, 1)
print("Integration time is " + str(integration_time) + " ms")

# =============================================================================
# Set the power supply setting 
# =============================================================================

# key = KeysightE36312A(0.5) 
# key.ChannelSelect(channel)
# key.SetOPCurrent(OC_current, channel)
# key.SetOPvoltage(OV_voltage, channel)
# key.ChannelEnable(power_enable)
# key.Setvoltage(voltage, channel)

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
y_max_value = 600000

    
# =============================================================================
# Main gating sweep loop
# =============================================================================
for time_gate_value in time_gate_list:
    
    # Print conditions and time gate value
    nir_vcsel_condition = "nir vcsel" + str(round(nir_vcsel_bias, 2)).replace('.', 'p')
    ir_vcsel_condition = "ir vcsel" + str(round(ir_vcsel_bias, 2)).replace('.', 'p')
    clk_condition = "clk" + str(int(clk_freq / 1e6)) + "MHz"
    time_gate_condition = str(time_gate_value) + "ns"
    full_conditions = conditions + "_" + nir_vcsel_condition + "_" + ir_vcsel_condition + "_" + clk_condition + "_" + time_gate_condition
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
    subtractor_value                    = int(round((1/clk_freq) * 0.5 / 65e-12, 0)) + subtractor_offset
    period                              = round(1/clk_freq*1e9, 1)
    number_of_bins                      = 150
    bin_size                            = 12
    requested_delay                     = period + time_gate_value - 2
    duty_cycle                          = 0.5 
    spad_voltage                        = 24.7
    vrst_voltage                        = 3.3
    
    # =============================================================================
    # Logging Setup
    # =============================================================================
    if logging:
        
        # Create the results directory
        results_dir = '../../data/blitz_rigid4by4_dual_testing/data/'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
                        
        # Get the date and time for logging directory creation
        date_time=str(datetime.datetime.now())
        
        # Build the experiment directory name (conditions_year-month-day_hour-minute-second)
        experiment_directory_name = \
                        conditions + "_" + \
                        date_time[0:10] + "_" + \
                        date_time[11:13]+ "-" + \
                        date_time[14:16]+ "-" + \
                        date_time[17:19]
        
        # Create directory
        experiment_directory = os.path.join(results_dir, experiment_directory_name)
        os.mkdir(experiment_directory)
        
        # Check that logging directory was created
        if not os.path.exists(experiment_directory):
            raise Exception("Experiment directory " + experiment_directory + " was not created successfully")
            
        # Save a yeild file
        s = "detectors=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\nsources=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15"
        y_file = open(os.path.join(experiment_directory, "yield.txt"), 'w')
        y_file.write(str(s))
        y_file.close()
        
     
        
        # File header
        s = \
            "Conditions: " + str(conditions) + "\n" \
            "Number of Chips: " + str(number_of_chips) + "\n" \
            "Pad Captured Mask: " + str(pad_captured_mask) + "\n" \
            "Number of Captures: " + str(number_of_captures) + "\n" \
            "Clock Frequency: " + str(clk_freq) + "\n" \
            "Period: " + str(period) + "\n" \
            "Delay: " + str(0) + "\n" \
            "NIR VCSEL Setting: " + str(nir_vcsel_setting) + "\n" \
            "IR VCSEL Setting: " + str(ir_vcsel_setting) + "\n" \
            "Time Gating Setting: " + str(0) + "\n" \
            "Measurements per Pattern: " + str(meas_per_patt) + "\n" \
            "Patterns per Frame: " + str(patt_per_frame) + "\n" \
            "Number of Frames: " + str(number_of_frames) + "\n" \
            "NIR VCSEL Bias: " + str(nir_vcsel_bias) + "\n" \
            "IR VCSEL Bias: " + str(ir_vcsel_bias) + "\n" \
            "Laser Wavelength: " + "" + "\n" \
            "Laser Power: " + "" + "\n" \
            "Laser Bandwidth: " + "" + "\n" \
            "Fiber Type: " + "" + "\n" \
            "Other Equipment: " + "" + "\n" \
            "Participant Name: " + "" + "\n" \
            "Test Type: " + "IRF" + "\n" \
            "Test Geometry: " + "" + "\n" \
            "Patch Location: " + "" + "\n" \
            "Phantom Number: " + "" + "\n" \
            "Solution Number: " + "" + "\n" \
            "ROI Size: " + "" + "\n" \
            "ROI ua: " + "" + "\n" \
            "SPAD Voltage: " + str(spad_voltage) + "\n" \
            "VRST Voltage: " + str(vrst_voltage) + "\n" \
            "Subtractor Offset: " + str(0) + "\n" \
            "Base Subtractor Value: " + str(subtractor_value) + "\n" \
            "Subtractor Value: " + str(subtractor_value) + "\n" \
            "Logging: " + str(logging) + "\n" + \
            "Logging Directory: " + str(experiment_directory) + "\n"
                
        # Save test setup
        ts_file = open(os.path.join(experiment_directory, "test_setup.txt"), 'w')
        ts_file.write(str(s))
        ts_file.close()
    
    
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
        data_plotter = MultipleDataPlotter.MultipleDataPlotter( packet, time_limits=[0,period*3/4])
        data_plotter_created = True
        
        # Setup
        data_plotter.set_subtractor_value(subtractor_value)        
        
        # Plot options
        data_plotter.set_vcsel_setting(nir_vcsel_setting)
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
    dut.fpga_interface.xem.ResetFPGA()
    # Print the serial number of the device
    serial_number = dut.fpga_interface.xem.GetSerialNumber()
    print("Serial Number: " + serial_number)

    # # Setup the delay line
    dut.DelayLine.specify_clock(period,duty_cycle) 
    clk_flip, coarse, fine, finest, actual_delay_ns = dut.DelayLine.get_setting(requested_delay)

    # Set up VCSEL biases 
    dut.update_vcsel_data_bits(nir_vcsel_bias, ir_vcsel_bias)
    dut.vcsel_enable_trigger()
    
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
        dut.enable_vcsel_cath_sm_supply()
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
            if True :
                scan_bits[i].TDCStartSelect        = '0'*8 if external_start else '1'*8
                scan_bits[i].TDCStopSelect         = '0'*8 if external_stop else '1'*8
                scan_bits[i].TDCDisable            = '0'*8
                scan_bits[i].TDCDCBoost            = '0'*8 
            else:
                scan_bits[i].TDCStartSelect        = '0'*8
                scan_bits[i].TDCStopSelect         = '0'*8
                scan_bits[i].TDCDisable            = '1'*8
                scan_bits[i].TDCDCBoost            = '1'*8 
            
            
            # Configure Pattern Counter
            scan_bits[i].MeasPerPatt           = np.binary_repr(meas_per_patt, 24)
            if True :
                scan_bits[i].MeasCountEnable       = '1'
            else:
                scan_bits[i].MeasCountEnable       = '0'
            
            
            # Configuring Delay Lines
            # dword = 140

            scan_bits[i].AQCDLLCoarseWord      = np.binary_repr(coarse, 4)
            scan_bits[i].AQCDLLFineWord        = np.binary_repr(fine, 3)
            scan_bits[i].AQCDLLFinestWord      = np.binary_repr(finest, 1)
            scan_bits[i].DriverDLLWord         = np.binary_repr(0, 5)
            scan_bits[i].ClkFlip               = np.binary_repr(clk_flip,1)
            scan_bits[i].ClkBypass             = '0'
            
            # Configure pattern reset signal
            scan_bits[i].PattResetControlledByTriggerExt       = '0' 
            scan_bits[i].PattResetExtEnable    = '0'
                
            # Configure VCSELs
            scan_bits[i].VCSELWave1Enable         = '0'    
            scan_bits[i].VCSELEnableWithScan        = '0'     
            scan_bits[i].VCSELEnableControlledByScan        = '0' 
            scan_bits[i].VCSELWave2Enable         = '0'
            
            
            # Configure TxData
            scan_bits[i].TestPattEnable        = '0'
            scan_bits[i].TestDataIn            = np.binary_repr(4, 10)
            scan_bits[i].TxDataExtRequestEnable = '0'
            
            # Configure subtractor
            scan_bits[i].TimeOffsetWord        = np.binary_repr(subtractor_value, 10)
            scan_bits[i].SubtractorBypass      = '0'
            
            # Dynamic operation
            scan_bits[i].DynamicConfigEnable = '1' if dynamic_mode else '0'
            
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
        dut.FrameController.send_frame_data( number_of_chips, \
                                            number_of_frames,   \
                                            patt_per_frame,     \
                                            meas_per_patt,
                                            pad_captured_mask )
            
        # =============================================================================
        # Create an emitter pattern
        # =============================================================================
        # nir_enabled = '1' if (w == 'nir') else '0'
        # ir_enabled =  '1' if (w == 'ir') else '0'
        if dynamic_mode:
            dynamic_packet = DynamicPacket.DynamicPacket(number_of_chips, patt_per_frame)
            
            # These settings are maintained through all patterns
            dynamic_packet.fill(field_dict={    'nir_vcsel_enable': '0', \
                                                'ir_vcsel_enable': '0', \
                                                'driver_dll_word': np.binary_repr(0, 5), \
                                                'clk_flip': np.binary_repr(clk_flip,1), \
                                                'aqc_dll_coarse_word': np.binary_repr(coarse, 4), \
                                                'aqc_dll_fine_word': np.binary_repr(fine, 3), \
                                                'aqc_dll_finest_word': np.binary_repr(finest, 1), \
                                                })
                
            # # Sweep emitter
            for p in range(patt_per_frame):
                if p < 16:
                    c = p
                    dynamic_packet.fill(pattern_list=[p], chip_list=[c], field_dict={'vcsel_enable': '1', 'nir_vcsel_enable': '1'})
                    dynamic_packet.fill(pattern_list=[p], field_dict={'driver_dll_word': np.binary_repr(nir_vcsel_setting, 5)})
                else:
                    c = p-16
                    dynamic_packet.fill(pattern_list=[p], chip_list=[c], field_dict={'vcsel_enable': '1', 'ir_vcsel_enable': '1'})
                    dynamic_packet.fill(pattern_list=[p], field_dict={'driver_dll_word': np.binary_repr(ir_vcsel_setting, 5)})
            
            # Show results
            s = dynamic_packet.write()
            
            # Activate dynamic mode
            dut.activate_dynamic_mode(dynamic_packet)
            
            # Save dynamic packet
            if logging:
                ts_file = open(os.path.join(experiment_directory, "dynamic_packet.txt"), 'w')
                ts_file.write(str(s))
                ts_file.close()


        # =============================================================================
        # Final chip reset before capture starts
        # =============================================================================
        dut.pulse_signal('cell_reset')
        dut.reset_fifos()
        time.sleep(config_wait)


        # =============================================================================
        # Image capture loop
        # =============================================================================
        print("Blitzing histograms")
        
        # Initialize capture count
        c = 0

        # Start blitz
        dut.FrameController.begin_blitz()
        
        
        # Begin blitz
        while True:
            
            if dut.check_ram_trigger():
            
                
                # Read data
                dut.read_master_fifo_data(packet)
            
                # Save
                if logging:
                    np.save(os.path.join(experiment_directory, "capture_" + str(c) + ".npy"), packet.data)
                
                # Update the plot
                if plotting:
                    data_plotter.update_plot(pattern_to_plot=0)
                    
                # Increment capture count
                c = c + 1
                    
                # Check
                if c == number_of_captures:
                    break
    
    # =============================================================================
    # Disable supplies, close plots, log files, and FPGA on exit
    # =============================================================================
    finally:
        # End blitz
        dut.FrameController.end_blitz()
        print("Finished blitzing histograms")
        
        # # Read out results
        # for i in range(number_of_chips):
        #     dut.update_scan_chain(row[i], config_wait)
        # scan_bits_received = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
        
        
        dut.disable_hvdd_ldo_supply()
        dut.disable_vcsel_cath_sm_supply()
        dut.disable_cath_sm_supply()
        # key.ChannelEnable(False)
        print("Closing FPGA")
        dut.fpga_interface.xem.Close()
        if data_plotter_created:
            data_plotter.close()
