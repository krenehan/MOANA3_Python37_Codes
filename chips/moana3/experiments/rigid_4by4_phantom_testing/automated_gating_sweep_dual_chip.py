from includes import *
from KeysightE36312A import * 
import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np 

# for vs in [3,4]:
#     vcsel_setting = [0,]
#     for sv in vcsel_setting:
#         if vs == 3:
#             vcsel_setting = 0.4
#         else:
#             vcsel_setting = [0.5, 0.8]
for av in range(16):    
        
    # =============================================================================
    # Top-level parameters
    # =============================================================================

    
        # Number of captures per time gating setting
        number_of_captures = 1000
        
        # VCSEL bias setting
        vcsel_bias                          = 0.4 #sv 0.4,0.5,0.8
        active_vcsel                        = av
        vcsel_setting                       = 3 #vs 
        ir_vcsel                            = False
        
        # Phantom setting
        
        thickness                           = 6 #0.4,0.5,0.6
        size                                = 3 #2,3,4,5,9
        location                            = "3c3b" #tr,tl,b 
        number                              = 13
        
        #Power Supply setting 
        
        channel                             = 1
        power_enable                        = True 
        OC_current                          = 0.050
        OV_voltage                          = 4  
        voltage                             = 0.4 #sv
        
        # Test conditions to propagate to log file
        
        conditions = "thickness" + str(thickness) + "mm" + "_" + \
                     "size" + str(size).replace(".","p") + "mm" + "_" + \
                     "location" + str(location) + "_" + \
                     "emitter" + str(active_vcsel) + "_" + \
                     "setting" + str(vcsel_setting) + "_" + \
                    "bias" + str(vcsel_bias).replace(".", "p") + "V"
        if ir_vcsel:
            conditions = conditions + "_ir"
            
        print("================Conditions======================")
        print("================================================")
        print(conditions)
        print("================================================")
        print("================================================")
                    
        
        
        # =============================================================================
        # Test settings
        # Integration time = meas_per_patt * 1/clk_freq * patt_per_frame * number_of_frames
        # =============================================================================
        number_of_chips = 16
        meas_per_patt                       = 100000
        patt_per_frame                      = 1
        number_of_frames                    = 1
        clk_freq                            = 50e6
        period                              = 1/clk_freq
        tx_refclk_freq                      = 12.5e6
        pad_captured_mask                   = 0b1111111111111111
        clk_flip                            = True
        spad_voltage                        = 25.0
        vrst_voltage                        = 3.3
        time_gate_list                      = [0, ]
        subtractor_value                    = 145
        
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
        # Create an emitter pattern
        # =============================================================================
        emitter_pattern =  np.zeros((16, number_of_chips), dtype=bool)
        ir_emitters = np.zeros((number_of_chips), dtype=bool)
        emitter_pattern[0][active_vcsel] = True
        if ir_vcsel:
            ir_emitters[active_vcsel] = True
        
        
        # =============================================================================
        # Top-level options
        # =============================================================================
        # Enabling this will export data to log file 
        logging = True
        
        # Enabling this will show the plots as data is collected
        plotting = False 
        
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
        log_plots = True
        
        # Enabling this shows information about chip settings associated with the plotted data
        show_plot_info = False
        
        # Enabling this fixes the y-axis at a max value
        fix_y_max = False
        y_max_value = 300000
        
            
        # =============================================================================
        # Main gating sweep loop
        # =============================================================================
        for time_gate_value in time_gate_list:
            
            # Waiting times
            config_wait  = 0.3
            ldo_wait = 0.5
            
            
            # =============================================================================
            # Logging Setup
            # =============================================================================
            if logging:
                
                # Create the results directory
                results_dir = '../../data/test_run_2/data/'
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
                
                # Save emitter pattern
                np.save(os.path.join(experiment_directory, "emitter_pattern.npy"), emitter_pattern, fix_imports=False)
                
                # Save ir emitters
                np.save(os.path.join(experiment_directory, "ir_emitters.npy"), ir_emitters, fix_imports=False)
                
                # File header
                s = \
                    "Conditions: " + str(conditions) + "\n" \
                    "Number of Chips: " + str(number_of_chips) + "\n" \
                    "Pad Captured Mask: " + str(pad_captured_mask) + "\n" \
                    "Number of Captures: " + str(number_of_captures) + "\n" \
                    "Clock Frequency: " + str(clk_freq) + "\n" \
                    "Period: " + str(period) + "\n" \
                    "Delay: " + str(0) + "\n" \
                    "VCSEL Setting: " + str(vcsel_setting) + "\n" \
                    "Time Gating Setting: " + str(0) + "\n" \
                    "Measurements per Pattern: " + str(meas_per_patt) + "\n" \
                    "Patterns per Frame: " + str(patt_per_frame) + "\n" \
                    "Number of Frames: " + str(number_of_frames) + "\n" \
                    "VCSEL Bias: " + str(vcsel_bias) + "\n" \
                    "Laser Wavelength: " + "" + "\n" \
                    "Laser Power: " + "" + "\n" \
                    "Laser Bandwidth: " + "" + "\n" \
                    "Fiber Type: " + "" + "\n" \
                    "Other Equipment: " + "" + "\n" \
                    "Participant Name: " + "" + "\n" \
                    "Test Type: " + "IRF" + "\n" \
                    "Test Geometry: " + "" + "\n" \
                    "Patch Location: " + "" + "\n" \
                    "Phantom Number: " + str(number) + "\n" \
                    "Solution Number: " + "" + "\n" \
                    "ROI Size: " + str(size) + "\n" \
                    "ROI Location: " + str(location) + "\n" \
                    "ROI ua: " + str(0.934) + "\n" \
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
            # Equipment Setup
            # =============================================================================
            func_gen        = None
            supply_main     = None
            supplt_aux      = None
            time.sleep(config_wait)
            
            
            # =============================================================================
            # Test settings that are dynamically updated or stay constant
            # =============================================================================
            period                              = round(1/clk_freq*1e9, 1)
            number_of_bins                      = 150
            bin_size                            = 12
            requested_delay                     = period + time_gate_value -1 
            duty_cycle                          = 0.5            
            
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
            
            # # Setup the delay line
            # dut.DelayLine.set_clk_flip(clk_flip)
            dut.DelayLine.specify_clock(period,duty_cycle) 
            clk_flip, coarse, fine, finest, actual_delay_ns = dut.DelayLine.get_setting(requested_delay)
            
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
                    if True :
                        scan_bits[i].MeasCountEnable       = '1'
                    else:
                        scan_bits[i].MeasCountEnable       = '0'
                    
                    
                    # Configuring Delay Lines
                    # dword = 140
        
                    scan_bits[i].AQCDLLCoarseWord      = np.binary_repr(coarse, 4)
                    scan_bits[i].AQCDLLFineWord        = np.binary_repr(fine, 3)
                    scan_bits[i].AQCDLLFinestWord      = np.binary_repr(finest, 1)
                    scan_bits[i].DriverDLLWord         = np.binary_repr(vcsel_setting, 5)
                    scan_bits[i].ClkFlip               = np.binary_repr(clk_flip,1)
                    scan_bits[i].ClkBypass             = '0'
                    
                    # Configure pattern reset signal
                    scan_bits[i].PattResetControlledByTriggerExt       = '0' 
                    scan_bits[i].PattResetExtEnable    = '0'
                        
                    # Configure VCSELs
                    scan_bits[i].VCSELEnableWithScan        = '1'     
                    scan_bits[i].VCSELEnableControlledByScan        = '1'
                    
                    # VCSEL selection
                    if i == active_vcsel:
                        scan_bits[i].VCSELWave1Enable         = '0' if ir_vcsel else '1'
                        scan_bits[i].VCSELWave2Enable         = '1' if ir_vcsel else '0'
                    else:
                        scan_bits[i].VCSELWave1Enable         = '0'
                        scan_bits[i].VCSELWave2Enable         = '0'
                    
                    # Configure TxData
                    scan_bits[i].TestPattEnable        = '0'
                    scan_bits[i].TestDataIn            = np.binary_repr(4, 10)
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
                dut.FrameController.send_frame_data( np.zeros((patt_per_frame, number_of_chips), dtype=bool),      \
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
                for c in range(number_of_captures):
                    
                    # Status
                    if (c % 50) == 0:
                        print("Capture " + str(c) + " of " + str(number_of_captures))
                    
                    # Run capture
                    dut.FrameController.run_capture()
                    
                    # Read the data
                    dut.read_master_fifo_data(packet)
                    
                    # Save
                    if(logging):
                        np.save(os.path.join(experiment_directory, "capture_" + str(c) + ".npy"), packet.data)
                    
         
                    # Update the plot
                    if plotting:
                        data_plotter.update_plot() 
            
            # =============================================================================
            # Disable supplies, close plots, log files, and FPGA on exit
            # =============================================================================
            finally:
                # dut.disable_hvdd_ldo_supply()
                dut.disable_cath_sm_supply()
                # key.ChannelEnable(False)
                print("Closing FPGA")
                dut.fpga_interface.xem.Close()
                if data_plotter_created:
                    data_plotter.close()
    