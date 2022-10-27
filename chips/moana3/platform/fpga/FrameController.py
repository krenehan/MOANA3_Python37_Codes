# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:48:40 2020

API for communicating with the Frame Controller on the FPGA. 

@author: Kevin R.
"""

import time
import  __address__ as addr
from math import ceil


# ====================================================
# Custom exception
# ====================================================  
class FrameControllerError(Exception):
    pass


class FrameController:
    
    # Status bits
    __scan_done = False
    __frame_data_sent = False
    __fsm_bypass = False
    __frame_controller_reset = False
    __capture_start = False
    __capture_interrupt = False
    __data_stream = False
    __blitz_mode = False
    
    # Frame data settings
    __packets_per_transfer = 0
    __number_of_frames = 0
    __patterns_per_frame = 0
    __measurements_per_pattern = 0
    __pad_captured_mask = 0b0000000000000000
    
    # Capture wait time (s)
    __capture_wait_time = 0.0
    
    # Frame controller wire-in register
    __framectrl_reg    = 0x0000
    
    # To verify that frame data routine was called before running capture
    __ready_to_run_capture = False
    
    # Software In Frame Controller Signals
    __SIGNAL_SCAN_DONE =              0x0001
    __SIGNAL_FRAME_DATA_SENT =        0x0002
    __SIGNAL_CAPTURE_START =          0x0004
    __SIGNAL_CAPTURE_INTERRUPT =      0x0008
    __SIGNAL_FRAME_CONTROLLER_RESET = 0x0010
    __SIGNAL_FSM_BYPASS =             0x0020
    __SIGNAL_DATA_STREAM =            0x0040
    __SIGNAL_BLITZ_MODE =             0x0080
    
    # Software Out Frame Controller Signals
    __SIGNAL_CAPTURE_IDLE =           0x0020
    __SIGNAL_FRAME_DATA_RECEIVED =    0x0040
    __SIGNAL_CAPTURE_RUNNING =        0x0080
    __SIGNAL_CAPTURE_DONE =           0x0100
    
    # Frame controller states
    __STATE_IDLE =                    0x01
    __STATE_HANDSHAKE =               0x02
    __STATE_RUN_CAPTURE =             0x04
    __STATE_FINISH_DATATX =           0x08
    __STATE_FINISH_CAPTURE =          0x10
    __STATE_RESET =                   0x20
    __STATE_STREAM_RESUME =           0x40
    __STATE_BLITZ =                   0x80
    
    # Clock period (ns)
    period = 20.0
    txperiod = 40.0
    
    # Number of chips
    __number_of_chips =               0
    
    # 16-bit words per histogram
    __number_of_words_per_histogram =   300
    __data_stream_words_per_transfer =  0
    
    # To verify that stream configuration data was sent
    __data_stream_config_sent =              False
    
    # Size of backend FIFO
    __fifo_size = 0

    
    # ====================================================
    # Initialize the frame controller instance with object references
    # ====================================================
    def __init__(self, fpga_interface_object=None):
        
        # Initialize the FPGA interface object
        self.__fpga_interface = fpga_interface_object
        
        # Frame controller signals
        self.frame_controller_signal =                              {}
        self.frame_controller_signal['scan_done'] =                 self.__SIGNAL_SCAN_DONE
        self.frame_controller_signal['frame_data_sent'] =           self.__SIGNAL_FRAME_DATA_SENT
        self.frame_controller_signal['capture_start'] =             self.__SIGNAL_CAPTURE_START
        self.frame_controller_signal['capture_interrupt'] =         self.__SIGNAL_CAPTURE_INTERRUPT
        self.frame_controller_signal['frame_controller_reset'] =    self.__SIGNAL_FRAME_CONTROLLER_RESET
        self.frame_controller_signal['fsm_bypass'] =                self.__SIGNAL_FSM_BYPASS
        self.frame_controller_signal['data_stream'] =               self.__SIGNAL_DATA_STREAM
        self.frame_controller_signal['blitz_mode'] =                self.__SIGNAL_BLITZ_MODE
        
        
    # ====================================================
    # Run data stream routine
    # ====================================================
    def begin_blitz(self):
        ''' Begin the blitz routine '''
            
        # Check that stream configuration was sent
        if not self.__data_stream_config_sent:
            raise FrameControllerError("Must call send_data_stream_config before calling begin_blitz")
            
        # End scan process
        self.__set_scan_done()
        
        # Send frame data
        self.__run_send_frame_data()
        
        # Start stream process
        self.__set_blitz_mode()
        
        
    # ====================================================
    # Run data stream routine
    # ====================================================
    def begin_stream(self):
        ''' Begin the stream routine '''
            
        # Check that stream configuration was sent
        if not self.__data_stream_config_sent:
            raise FrameControllerError("Must call send_data_stream_config before calling run_stream")
            
        # End scan process
        self.__set_scan_done()
        
        # Send frame data
        self.__run_send_frame_data()
        
        # Start stream process
        self.__set_data_stream()
    
    
    # ====================================================
    # Check that the capture is complete
    # ====================================================
    def check_capture_done(self):
        out = self.__fpga_interface.wire_out(addr.ADDR_WIRE_OUT_SIGNAL)
        #print "WireOut: %s" % bin(out)
        if (out & self.__SIGNAL_CAPTURE_DONE):
            return True
        else:
            return False
        
    
    # ====================================================
    # Check that the FSM is not running the chip
    # ====================================================
    def check_capture_idle(self):
        out = self.__fpga_interface.wire_out(addr.ADDR_WIRE_OUT_SIGNAL)
        #print "WireOut: %s" % bin(out)
        if (out & self.__SIGNAL_CAPTURE_IDLE):
            return True
        else:
            return False
    
    
    # ====================================================
    # Check that the capture is running
    # ====================================================
    def check_capture_running(self):
        out = self.__fpga_interface.wire_out(addr.ADDR_WIRE_OUT_SIGNAL)
        #print "WireOut: %s" % bin(out)
        if (out & self.__SIGNAL_CAPTURE_RUNNING):
            return True
        else:
            return False
    
    
    # ====================================================
    # Check that the frame data has been received
    # ====================================================
    def check_frame_data_received(self):
        out = self.__fpga_interface.wire_out(addr.ADDR_WIRE_OUT_SIGNAL)
        #print "WireOut: %s" % bin(out)
        if (out & self.__SIGNAL_FRAME_DATA_RECEIVED):
            return True
        else:
            return False


    # ====================================================
    # Check state of frame controller
    # ====================================================
    def check_state(self):
        
        s = self.__fpga_interface.wire_out(addr.ADDR_WIRE_OUT_FC_STATE)
        if s == self.__STATE_IDLE:
            return "Frame controller state is IDLE"
        elif s == self.__STATE_HANDSHAKE:
            return "Frame controller state is HANDSHAKE"
        elif s == self.__STATE_RUN_CAPTURE:
            return "Frame controller state is RUN_CAPTURE"
        elif s == self.__STATE_FINISH_DATATX:
            return "Frame controller state is FINISH_DATATX"
        elif s == self.__STATE_FINISH_CAPTURE:
            return "Frame controller state is FINISH_CAPTURE"
        elif s == self.__STATE_RESET:
            return "Frame controller state is RESET"
        elif s == self.__STATE_STREAM_RESUME:
            return "Frame controller state is STREAM_RESUME"
        elif s == self.__STATE_BLITZ:
            return "Frame controller state is BLITZ"
        else:
            return "Frame controller state is unknown"
        
        
    # ====================================================
    # End data stream routine
    # ====================================================
    def end_blitz(self):
        ''' End the blitz routine '''
        
        # Start stream process
        self.__unset_blitz_mode()

        
        
    # ====================================================
    # End data stream routine
    # ====================================================
    def end_stream(self):
        ''' End the stream routine '''
        
        # Start stream process
        self.__unset_data_stream()
    
        
    # ====================================================
    # Report frame controller status
    # ====================================================
    def report_frame_controller_status(self):
        print( "Address: {}".format(addr.ADDR_WIRE_IN_FRAMECTRL))
        print( "Number of Frames: {}".format(self.__number_of_frames))
        print( "Patterns per Frame: {}".format(self.__patterns_per_frame))
        print( "Measurements per Pattern: {}".format(self.__measurements_per_pattern))
        print( "FSM Bypass: {}".format(self.__fsm_bypass))
        print( "Frame Controller Reset: {}".format(self.__frame_controller_reset))
        print( "Frame Controller Idle: {}".format(self.check_capture_idle()))
        print( "Scan Done: {}".format(self.__scan_done))
        print( "Frame Data Sent: {}".format(self.__frame_data_sent))
        print( "Frame Data Received: {}".format(self.check_frame_data_received()))
        print( "Capture Start: {}".format(self.__capture_start))
        print( "Capture Running: {}".format(self.check_capture_running()))
        print( "Capture Done: {}".format(self.check_capture_done()))
        print( "Capture Interrupt: {}".format(self.__capture_interrupt))
        
    
    # ====================================================
    # Reset the frame controller
    # ====================================================
    def reset(self):
        ''' Reset the frame controller '''
        
        # Reset register to 0
        self.__framectrl_reg = 0x00
        self.__scan_done = False
        self.__frame_data_sent = False
        self.__fsm_bypass = False
        self.__frame_controller_reset = False
        self.__capture_start = False
        self.__capture_interrupt = False
        self.__data_stream_config_sent = False
        self.__data_stream = False
        self.__pulse_frame_controller_reset()
    
    
    # ====================================================
    # Run capture routine
    # ====================================================
    def run_capture(self, number_of_captures=1):
        ''' Run the main capture routine '''
        
        # Check that frame data was specified beforehand
        if not self.__ready_to_run_capture:
            print("Must call send_frame_data before calling run_capture")
            raise FrameControllerError
        
        # Ensure that number of captures is an integer value
        __number_of_captures = int(number_of_captures)
        
        # Start the number of successful captures at 0
        __successful_captures = 0
        
        # Main run loop
        while __successful_captures < __number_of_captures:
        
            try:
                
                # End scan process
                self.__set_scan_done()
                
                # Send frame data
                self.__run_send_frame_data()
            
                # Start the capture
                self.__set_capture_start()
                
                # Wait a little
                time.sleep(self.__capture_wait_time)
                
                # Check that the capture process is done
                self.__run_capture_done()
                
                # Ensure that the frame controller is in idle state
                self.__run_capture_idle()
                
                # Add to successful captures
                __successful_captures = __successful_captures + 1
            
            except FrameControllerError as e:
                
                # Pulse the reset and try again
                print(str(e))
                print("Resetting frame controller and trying again")
                self.reset()
                self.__fpga_interface.reset_fifos()
                
        
    # ====================================================
    # Send configuration information to the frame controller
    # ====================================================
    def send_frame_data(self, number_of_chips, number_of_frames, patterns_per_frame, measurements_per_pattern, pad_captured_mask):
        ''' Send configuration data to the frame controller'''
        
        # Retain number of chips
        self.__number_of_chips = number_of_chips
        
        # Update the number of frames
        self.__update_number_of_frames(number_of_frames)
        
        # Update the patterns per frame
        self.__update_patterns_per_frame(patterns_per_frame)
        
        # Update the measurements per pattern
        self.__update_measurements_per_pattern(measurements_per_pattern)
        
        # Update the packets per transfer
        self.__update_packets_per_transfer(number_of_frames * patterns_per_frame)
        
        # Update the pad_captured mask
        self.__update_pad_captured_mask(pad_captured_mask)
        
        # Get the FIFO size
        self.__get_fifo_size()
        
        # Calculate the wait time
        self.__capture_wait_time = self.period * 1e-9 * measurements_per_pattern * patterns_per_frame * number_of_frames
        
        # Indicate the capture is ready to run
        self.__ready_to_run_capture = True
        
        # Send the datastream configuration
        self.__send_data_stream_config()
        
        # Check configuration settings before run
        self.__check_for_configuration_errors()
        
        
    # ====================================================
    # Set the fpga interface object
    # ====================================================
    def set_fpga_interface(self, fpga_interface_object):
        self.__fpga_interface = fpga_interface_object
        
    
    # ====================================================
    # Bypass the frame controller to run the clocks
    # ====================================================
    def set_fsm_bypass(self):
        self.__tiehi_signal('fsm_bypass')
        self.__fsm_bypass = True
    
    
    # ====================================================
    # Stop bypassing the frame controller to stop the clocks
    # ====================================================
    def unset_fsm_bypass(self):
        self.__tielo_signal('fsm_bypass')
        self.__fsm_bypass = False
        
        
    # ====================================================
    # Check for configuration erros in the test platform
    # ====================================================
    def __check_for_configuration_errors(self):
        
        # Check clock frequencies
        if self.period < 10:
            raise FrameControllerError("RefClk frequency must be less than or equal to 100 MHz for proper chip operation")
        if self.txperiod < 40:
            raise FrameControllerError("TxRefClk frequency must be less than or equal to 25 MHz for proper chip operation")
            
        # Check that measurements per pattern does not exceed 24 bits
        if self.__measurements_per_pattern > 2**24-1:
            raise FrameControllerError("Measurements per pattern cannot exceed " + str(2**24-1))
            
        # Check that number of words per transfer is divisible by 4 (because of 32->128 FIFO)
        if ( (self.__number_of_words_per_transfer * self.__number_of_chips) % 4):
            raise FrameControllerError("The total number of 32b bin values (chips*frames*patterns*bins) transferred from the FPGA to the PC must be divisible by 4")
            
        # Ensure that number of words per transfer is not too large
        if (self.__number_of_words_per_transfer > 2**16-1):
            raise FrameControllerError("Number of words per transfer is greater than 2^16-1")
        
    
    # ====================================================
    # Get the frame controller signal
    # ====================================================
    def __get_frame_controller_signal(self, signal_name):
        return(self.frame_controller_signal[signal_name])
        
        
    # ====================================================
    # Pulse the capture interrupt bit
    # ====================================================
    def __pulse_capture_interrupt(self):
        self.__set_capture_interrupt()
        time.sleep(0.1)
        self.__unset_capture_interrupt()
    
    
    # ====================================================
    # Pulse the frame controller reset bit
    # ====================================================
    def __pulse_frame_controller_reset(self):
        self.__set_frame_controller_reset()
        time.sleep(0.1)
        self.__unset_frame_controller_reset()
                
                
    # ====================================================
    # Check that the capture is done
    # ====================================================
    def __run_capture_done(self):
        
        # Verify that capture is done
        # for tries in range(0, 2000):
        while True:
            
            # If capture is done, unset relevant bits and end loop
            if self.check_capture_done():
                self.__unset_capture_start()
                self.__unset_frame_data_sent()
                self.__unset_scan_done()
                # print("Check capture done true-> " + self.check_state())
                return 0
            
            # If the capture is still running, wait for it to finish
            elif self.check_capture_running():
                time.sleep(0.001)
                # print("Check capture done false-> " + self.check_state())
                
            # If the capture isn't running, end the process
            else:
                time.sleep(0.001)
                # raise FrameControllerError("Capture did not start")
        
        # If we try 2000 times and still haven't gotten a capture, we quit
        raise FrameControllerError("Capture did not finish")
                
                
    # ====================================================
    # Check that the FSM is idle during capture
    # ====================================================
    def __run_capture_idle(self):
        
        # # Check that capture is idle
        # if (not self.check_capture_idle()):
        #     raise FrameControllerError("Frame controller not idle")
        
        while True:
            if self.check_capture_idle():
                break
    
    
    # ====================================================
    # Send the frame data
    # ====================================================
    def __run_send_frame_data(self):
        
        # Send frame data and verify that it is received
        while True:
            
            # Frame data sent
            self.__set_frame_data_sent()
            
            # Check that frame data was received
            if (self.check_frame_data_received()):
                self.__unset_frame_data_sent()
                break
            else:
                pass
                # raise FrameControllerError("Frame data not received")
        
        
    # ====================================================
    # Set the blitz_mode bit
    # ====================================================
    def __set_blitz_mode(self):
        self.__tiehi_signal('blitz_mode')
        self.__blitz_mode = True
        
    
    # ====================================================
    # Send the number of words per transfer
    # ====================================================
    def __send_data_stream_config(self):
        ''' Send number of 16-bit words per transfer (per chip) to the frame controller, return read buffer '''
        
        # Check that frame data was specified beforehand
        if not self.__ready_to_run_capture:
            raise FrameControllerError("Must call send_frame_data before calling send_data_stream_config")
        
        # Calculate number of 16-bit words in a single transfer for a single chip
        self.__number_of_words_per_transfer = self.__number_of_words_per_histogram
        
        # Check that number of words per transfer is divisible by 2
        if (self.__number_of_words_per_transfer % 2):
            raise FrameControllerError("Number of words per transfer is not divisible by 2")
            
        # Divide by 2
        self.__number_of_words_per_transfer = self.__number_of_words_per_transfer // 2
            
        # Send to frame controller
        self.__update_data_stream_words_per_transfer(self.__number_of_words_per_transfer) # (Added divide by 2 for RAM controller)
        
        # Indicate that data stream config was sent
        self.__data_stream_config_sent = True
    
    
    # ====================================================
    # Interrupt the current capture
    # ====================================================
    def __set_capture_interrupt(self):
        self.__tiehi_signal('capture_interrupt')
        self.__capture_interrupt = True
    
    
    # ====================================================
    # Tell the frame controller to start the capture
    # ====================================================
    def __set_capture_start(self):
        self.__tiehi_signal('capture_start')
        self.__capture_start = True
        
        
    # ====================================================
    # Set the data_stream bit
    # ====================================================
    def __set_data_stream(self):
        self.__tiehi_signal('data_stream')
        self.__data_stream = True
    
    
    # ====================================================
    # Reset the frame controller
    # ====================================================
    def __set_frame_controller_reset(self):
        self.__tiehi_signal('frame_controller_reset')
        self.__frame_controller_reset = True
    
    
    # ====================================================
    # Notify the frame controller that the frame data was sent
    # ====================================================
    def __set_frame_data_sent(self):
        self.__tiehi_signal('frame_data_sent')
        self.__frame_data_sent = True
    
    
    # ====================================================
    # Notify the frame controller that the scan process is over
    # ====================================================
    def __set_scan_done(self):
        self.__tiehi_signal('scan_done')
        self.__scan_done = True
        
        
    # ====================================================
    # Tie a signal high
    # ====================================================
    def __tiehi_signal(self, signal_name):
        self.__framectrl_reg = self.__framectrl_reg | self.__get_frame_controller_signal(signal_name)
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_FRAMECTRL, self.__framectrl_reg)


    # ====================================================
    # Tie a signal low
    # ====================================================
    def __tielo_signal(self, signal_name):
        self.__framectrl_reg = self.__framectrl_reg & (~self.__get_frame_controller_signal(signal_name))
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_FRAMECTRL, self.__framectrl_reg)
        
        
    # ====================================================
    # Notify the frame controller that blitz mode operation is over
    # ====================================================
    def __unset_blitz_mode(self):
        self.__tielo_signal('blitz_mode')
        self.__blitz_mode = False
    
    
    # ====================================================
    # Unset the capture interrupt bit
    # ====================================================
    def __unset_capture_interrupt(self):
        self.__tielo_signal('capture_interrupt')
        self.__capture_interrupt = False
    
    
    # ====================================================
    # Unset the start capture bit
    # ====================================================
    def __unset_capture_start(self):
        self.__tielo_signal('capture_start')
        self.__capture_start = False
        
        
    # ====================================================
    # Notify the frame controller that data streaming is over
    # ====================================================
    def __unset_data_stream(self):
        self.__tielo_signal('data_stream')
        self.__data_stream = False
        
        
    # ====================================================
    # Update the words per transfer in the data stream
    # ====================================================
    def __update_data_stream_words_per_transfer(self, words_per_transfer):
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_STREAM, words_per_transfer)
        self.__data_stream_words_per_transfer = words_per_transfer
    
    
    # ====================================================
    # End frame controller reset
    # ====================================================
    def __unset_frame_controller_reset(self):
        self.__tielo_signal('frame_controller_reset')
        self.__frame_controller_reset = False
    
    
    # ====================================================
    # Notify the frame controller that the frame data was not sent
    # ====================================================
    def __unset_frame_data_sent(self):
        self.__tielo_signal('frame_data_sent')
        self.__frame_data_sent = False
    
    
    # ====================================================
    # Notify the frame controller that the scan process will begin again
    # ====================================================
    def __unset_scan_done(self):
        self.__tielo_signal('scan_done')
        self.__scan_done = False
    
    
    # ====================================================
    # Update the measurements per pattern in the FSM registers
    # ====================================================
    def __update_measurements_per_pattern(self, measurements_per_pattern):
        measurements_per_pattern_msb = (measurements_per_pattern & 0x00FF0000) >> 16
        measurements_per_pattern_lsb = (measurements_per_pattern & 0x0000FFFF)
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_MEASUREMENT_MSB, measurements_per_pattern_msb)
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_MEASUREMENT_LSB, measurements_per_pattern_lsb)
        self.__measurements_per_pattern = measurements_per_pattern
    

    # ====================================================
    # Update the number of frames in the FSM registers
    # ====================================================
    def __update_number_of_frames(self, number_of_frames):
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_FRAME, number_of_frames)
        self.__number_of_frames = number_of_frames
        
      
    # ====================================================
    # Update the packets in a transfer
    # ====================================================
    def __update_packets_per_transfer(self, packets_per_transfer):
        self.__fpga_interface.wire_in(addr.ADDR_WIREIN_PACKETS_IN_TRANSFER, packets_per_transfer)
        self.__packets_per_transfer = packets_per_transfer
        
        
    # ====================================================
    # Update the pad_captured mask
    # ====================================================
    def __update_pad_captured_mask(self, pad_captured_mask):
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_PAD_CAPTURED_MASK, pad_captured_mask)
    
    
    # ====================================================
    # Update the patterns per frame in the FSM registers
    # ====================================================
    def __update_patterns_per_frame(self, patterns_per_frame):
        self.__fpga_interface.wire_in(addr.ADDR_WIRE_IN_PATTERN, patterns_per_frame)
        self.__patterns_per_frame = patterns_per_frame

            
        