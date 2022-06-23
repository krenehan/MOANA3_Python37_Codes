from includes import *
from decimal import Decimal
import random
import numpy
import matplotlib.pyplot as plt

legend = []
for dword in range(0, 16):
# if True:
    # =============================================================================
    # Setup
    # =============================================================================
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
    ExternalStart    = True
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
        meas_per_patt                   = 100000 # 16777215 is max
        patt_per_frame                  = 1
        number_of_frames                = 1
        period                          = round(1/refclk_freq*1e9, 1)
        
        
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
            scan_bits[i].TDCStartSelect        = '01111111' if ExternalStart else '1'*8
            scan_bits[i].TDCStopSelect         = '0'*8 if ExternalStop else '10000000'
            scan_bits[i].TDCDisable            = '01111111'
            scan_bits[i].TDCDCBoost            = '01111111' if TDCDCBoost else '1'*8
            
            
            # Configure Pattern Counter
            scan_bits[i].MeasPerPatt           = np.binary_repr(meas_per_patt, 24)
            scan_bits[i].MeasCountEnable       = '1'
            
            # Configuring Delay Lines
            # dword = 3
            scan_bits[i].AQCDLLCoarseWord      = np.binary_repr( (dword&0b11110000) >> 4, 4)
            scan_bits[i].AQCDLLFineWord        = np.binary_repr((dword&0b1110) >> 1, 3)
            scan_bits[i].AQCDLLFinestWord      = np.binary_repr((dword&0b1), 1)
            scan_bits[i].DriverDLLWord         = np.binary_repr(5, 5)
            scan_bits[i].ClkFlip               = '0'
            scan_bits[i].ClkBypass             = '0'
            
            # Configure pattern reset signal
            scan_bits[i].PattResetControlledByTriggerExt       = '1' if PatternResetWithTriggerExt else '0'
            scan_bits[i].PattResetExtEnable    = '1' if PatternResetWithExternalSignal else '0'
            
            # Configure VCSELs
            scan_bits[i].VCSELEnableWithScan        = '1' if VCSELEnableExt else '0'
            scan_bits[i].VCSELEnableControlledByScan        = '1' if VCSELEnableThroughScan else '0'
            scan_bits[i].VCSELWave1Enable         = '1'
            scan_bits[i].VCSELWave2Enable         = '1'
            
            # Configure TxData
            scan_bits[i].TestPattEnable        = '0'
            scan_bits[i].TestDataIn            = np.binary_repr(0, 10)
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
    
        # Read out scan chain
        for i in range(number_of_chips):
            dut.update_scan_chain(row[i], read_wait) 
        scan_bits = [dut.chip_infrastructure.get_scan_chain(row[i]).get_scan_chain_segment(cell) for i in range(number_of_chips)]
        
        # Receive array
        packet = DataPacket.DataPacket(number_of_chips, number_of_frames, patt_per_frame, meas_per_patt, period, compute_mean=False)
            
        # Test pattern in, test pattern out loop
        for DataIn in (0b1111000011,):#range(1, 1023, 8):
            
            expected_packet = (DataIn << 10) + DataIn
            
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
                                                meas_per_patt       )
                
            # Run capture
            dut.FrameController.set_fsm_bypass()
            time.sleep(4*meas_per_patt*1/12e6)
            dut.FrameController.unset_fsm_bypass()
            # dut.FrameController.run_capture()
            
            # Read from pipe
            for chip in range(number_of_chips):
                packet.rbuf = bytearray(600*1*number_of_frames*patt_per_frame)
                if chip == 0:
                    dut.fpga_interface.xem.ReadFromPipeOut(0xA1, packet.rbuf)
                if chip == 1:
                    dut.fpga_interface.xem.ReadFromPipeOut(0xA2, packet.rbuf)
                
                # Raw string
                rs = dut.fpga_interface.decode_data_fifo_to_string(packet)
                
                # Isolate the packet from chip 0
                s = rs[0:32*150*patt_per_frame*number_of_frames]
                
                # Work through the packet
                print("------------------------- Chip " + str(chip) + " -------------------------")
                for p in range(len(s) // 32):
                    
                    # Grab the part of the string
                    ps = s[p*32:(p+1)*32]
                    print('Bin {0:03d}'.format(p) + ': ' + str(int(ps, base=2)))
            
                # Numpy datatype definition
                dt = np.dtype(np.uint32)
                dt = dt.newbyteorder('>')
                
                # Read from buffer
                packet_data = np.frombuffer(packet.rbuf, dtype=dt).astype(int)
                
                if chip == 1:
                    # plt.figure()
                    x = np.argmax(packet_data)
                    plt.plot(np.linspace(0, x-1, num=x)*60, packet_data[0:x])
                    legend.append(str(dword))
                
            
    
    
    finally:
        plt.legend(legend)
        print("Closing FPGA")
        dut.fpga_interface.xem.Close()
    
