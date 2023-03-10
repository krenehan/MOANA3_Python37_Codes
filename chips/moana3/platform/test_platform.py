import  chip.infrastructure
import chip.DelayLine
from fpga.FrameController import FrameController
import  fpga.interface
import  fpga.__address__ as addr
import  chip.__signal__ as sig
from time import sleep
from numpy import binary_repr

class TestPlatform:
    
    # wafer testing platform: 
    #   1) FPGA control interface  
    #   2) Chip infrastructure states
    #   3) 2 scan chains


    # ====================================================
    # Constructor for the TestPlatform class
    # ====================================================
    def __init__(self, chiplabel = '', verbose = 1):
        
        self.verbose = verbose
        
        # platform info
        if chiplabel == '' and self.verbose:
            print('WARNING: chiplabel is unknown.')
        self.chiplabel = chiplabel;
        self.platform = 'moana3'
        self.packet_length = 0
        self.packet_bits   = 0

        self.signal_reg    = 0x0000
        self.power_signal_reg = 0x0000

        # chip setup
        self.number_multicell_rows        = 16
        self.number_multicells_per_row    = 1
        
        # default wait times
        self.config_wait = 0.0
        self.read_wait = 0.01
        self.equip_wait = 0.5
          
        # platform setup
        self.fpga_interface =       None
        self.chip_infrastructure =  chip.infrastructure.Infrastructure( \
                                        self.number_multicell_rows,          \
                                        self.number_multicells_per_row, \
                                    )
        self.DelayLine = chip.DelayLine.DelayLine()
        self.FrameController = FrameController()
        

    # ====================================================
    # Set the packet length 
    # ====================================================
    def set_packet_length(self, packet_length):
        self.packet_length = packet_length
        self.packet_bits   = self.packet_length * 16


    # ====================================================
    # Initialize the FPGA
    # ====================================================
    def init_fpga(self, bitfile_path = '', wait = 0.5, refclk_freq = 50e6 ):
        
        if self.verbose:
            print("Initializing FPGA interface for chip " + self.chiplabel + ".")

        # set FPGA handle
        # use a bit file of packet length 1100 (16-bit word)
        self.set_packet_length(25);
        self.fpga_interface = fpga.interface.Interface(self.packet_length)
        
        # Pass FPGA interface object to frame controller
        self.FrameController.set_fpga_interface(self.fpga_interface)
        
        # TxRefClk frequency is fixed
        tx_refclk_freq = 12.5e6
        
        # Pass clock frequency to FrameController
        self.FrameController.period = round(1/refclk_freq*1e9, 1)
        self.FrameController.txperiod = round(1/tx_refclk_freq*1e9, 1)

        # Load bit file to FPGA
        if bitfile_path == '':
            raise Exception("No bit file specified.")
        if self.verbose:
            print("Loading bit file to FPGA.")
        self.fpga_interface.configure(bitfile_path) # low speed scanchain clock freq is 5MHz
        
        # Initialize clock
        self.init_clocks(refclk_freq)


    # ====================================================
    # Init clocks
    # ====================================================
    def init_clocks(self, refclk_freq):
        
        # Select bit based on clock frequency
        if refclk_freq == 100e6:
            s0 = False
            s1 = True
        elif refclk_freq == 25e6:
            s0 = True
            s1 = False
        else:
            s0 = False
            s1 = False
            
        print(str(s0) + ',' + str(s1))
            
        # Tie select bits high
        if s0:
            self.tiehi_power_signal('clk_select_0')
        else:
            self.tielo_power_signal('clk_select_0')
            
        if s1:
            self.tiehi_power_signal('clk_select_1')
        else:
            self.tielo_power_signal('clk_select_1')
            
        # Enable clock
        self.tiehi_power_signal('ref_clk_mmcm_enable')


    # ====================================================
    # Reset the signal register to 0
    # ====================================================
    def reset_signal_reg(self):
        self.signal_reg = 0x0000


    # ====================================================
    # Pulse a signal
    # ====================================================
    def pulse_signal(self, signal_name):
        temp_signal = self.signal_reg | self.chip_infrastructure.get_chip_signal(signal_name)
        self.fpga_interface.wire_in_signal(temp_signal)
        self.fpga_interface.wire_in_signal(self.signal_reg)


    # ====================================================
    # Tie a signal high
    # ====================================================
    def tiehi_signal(self, signal_name):
        self.signal_reg = self.signal_reg | self.chip_infrastructure.get_chip_signal(signal_name)
        self.fpga_interface.wire_in_signal(self.signal_reg)
        sleep(self.read_wait)


    # ====================================================
    # Tie a signal low
    # ====================================================
    def tielo_signal(self, signal_name):
        self.signal_reg = self.signal_reg & (~self.chip_infrastructure.get_chip_signal(signal_name))
        self.fpga_interface.wire_in_signal(self.signal_reg)
        sleep(self.read_wait)
        

    # ====================================================
    # Reset the power signal register to 0
    # ====================================================
    def reset_power_signal_reg(self):
        self.power_signal_reg = 0x0000


    # ====================================================
    # Pulse a power signal
    # ====================================================
    def pulse_power_signal(self, signal_name):
        temp_signal = self.power_signal_reg | self.chip_infrastructure.get_chip_signal(signal_name)
        self.fpga_interface.wire_in_power_signal(temp_signal)
        self.fpga_interface.wire_in_power_signal(self.power_signal_reg)


    # ====================================================
    # Tie a power signal high
    # ====================================================
    def tiehi_power_signal(self, signal_name):
        self.power_signal_reg = self.power_signal_reg | self.chip_infrastructure.get_chip_signal(signal_name)
        self.fpga_interface.wire_in_power_signal(self.power_signal_reg)
        sleep(self.read_wait)

    # ====================================================
    # Tie a power signal low
    # ====================================================
    def tielo_power_signal(self, signal_name):
        self.power_signal_reg = self.power_signal_reg & (~self.chip_infrastructure.get_chip_signal(signal_name))
        self.fpga_interface.wire_in_power_signal(self.power_signal_reg)
        sleep(self.read_wait)


    # ====================================================
    # Commit a scan chain to the chip
    # ====================================================
    def commit_scan_chain(self, chain_name = '', config_wait = 0.0, fill_bit = '0'):        
        
        if chain_name == '':
            raise Exception("Scan chain name not defined.")

        scan_data = self.make_scan_bits( \
            cell_length =   self.chip_infrastructure.get_scan_chain(chain_name).get_scan_chain_length(), \
            target_cell =   0, \
            total_cells =   1, \
            scan_row =      self.chip_infrastructure.get_scan_chain(chain_name).get_scan_chain_row_number(), \
            scan_data =     self.chip_infrastructure.get_scan_chain(chain_name).scan_chain_to_bits(), \
            fill_bit =      fill_bit)
        
        self.fpga_interface.write_scan_chain(scan_data)
        sleep(config_wait)


    # ====================================================
    # Retrieve the scan out data and update the infrastructure bits
    # ====================================================
    def update_scan_chain(self, chain_name = '', read_wait = 0.05):
        
        if chain_name == '':
            raise Exception("Scan chain name not defined.")

        scan_data = self.make_scan_bits( \
            cell_length =   self.chip_infrastructure.get_scan_chain(chain_name).get_scan_chain_length(), \
            target_cell =   0, \
            total_cells =   1, \
            scan_row =      self.chip_infrastructure.get_scan_chain(chain_name).get_scan_chain_row_number() )

        self.fpga_interface.read_scan_chain_request(scan_data)

        # Wait a bit
        sleep(read_wait)

        # Read from the FPGA buffer
        raw_data = self.fpga_interface.read_scan_chain_data()
        
        # update the infrastructure scan chain using the received data
        self.chip_infrastructure.update_scan_chain_bits( \
            chain_name =            chain_name, \
            data =                  raw_data, \
            number_packet_bits =    self.packet_bits \
        )
    
    
    # ====================================================
    # Create scan chain bits before piping out to FPGA interface
    # ====================================================
    def make_scan_bits( self, \
            cell_length = 0, \
            target_cell = 0, \
            total_cells = 1, \
            scan_row = 0, \
            scan_data   =   '0' * 0, \
            fill_bit    =   '0'):

        # Total number of bits in header
        header_number_of_bits = 64
        
        # Bits in header used for cmd
        cmd_number_of_bits = 16
        
        # Number of bits in various parameters
        cell_length_number_of_bits = 18
        target_cell_number_of_bits = 8
        total_cells_number_of_bits = 8
        scan_row_number_of_bits = 4

        # Encode length and stuff into bits
        cell_length_bits =  binary_repr(cell_length,    cell_length_number_of_bits)
        target_cell_bits =  binary_repr(target_cell,    target_cell_number_of_bits)
        total_cells_bits =  binary_repr(total_cells,    total_cells_number_of_bits)
        scan_row_bits =     binary_repr(scan_row,       scan_row_number_of_bits)
                        
        # Data bits that must be sent to the FPGA
        data_bits = self.packet_bits - header_number_of_bits

        # Create fillers
        filler = fill_bit * (data_bits - len(scan_data))
        header_fill = fill_bit * ( header_number_of_bits - \
                                  cell_length_number_of_bits - \
                                  target_cell_number_of_bits - \
                                  total_cells_number_of_bits - \
                                  scan_row_number_of_bits - \
                                  cmd_number_of_bits )
        
        if len(scan_data) > data_bits:
            raise ValueError("Number of scan data bits (" + str(len(scan_data)) + ") exceeds max data bits (" + str(data_bits) + "!")
                        
        bits    =   ''
        bits    +=  filler
        bits    +=  scan_data
        bits    +=  header_fill
        bits    +=  scan_row_bits
        bits    +=  total_cells_bits
        bits    +=  target_cell_bits
        bits    +=  cell_length_bits
        
        
		# check final output size
        if len(bits) != self.packet_length * 16 - 16:
            raise ValueError("Number of scan bits (" + str(len(bits)) + ") does not match required (" + str(self.packet_length * 16 - 16) + "!")
        
        return bits

    
    # ====================================================
    # Scan in function for debug
    # ====================================================
    def scan_in(self, \
            cell_length = 0, \
            target_cell = 0, \
            total_cells = 1, \
            scan_row = 0, \
            scan_data = '0' * 0, \
            fill_bit = '0'):

        # Issue a scan write command
        scan_data = self.make_scan_bits( \
            cell_length = cell_length, \
            target_cell = target_cell, \
            total_cells = total_cells, \
            scan_row = scan_row, \
            scan_data = scan_data, \
            fill_bit = fill_bit)

        self.fpga_interface.write_scan_chain(scan_data)
    
    
    # ====================================================
    # Scan out function for debug
    # ====================================================
    def scan_out(self, \
            cell_length = 0, \
            target_cell = 0, \
            total_cells = 1, \
            scan_row = 0, \
            read_wait = 0.2):
        
        # Issue a scan read command
        scan_data = self.make_scan_bits( \
            cell_length = cell_length, \
            target_cell = target_cell, \
            total_cells = total_cells, \
            scan_row = scan_row)            
        self.fpga_interface.read_scan_chain(scan_data)
        # Wait a bit
        sleep(read_wait)
        # Read from the FPGA buffer
        raw = self.fpga_interface.read_scan_chain_data()
        # Return the pruned bits
        return raw[self.packet_length*16-64-cell_length:self.packet_length*16-64]
    
    
    # ====================================================
    # Reset both FIFOs
    # ====================================================
    def reset_fifos(self):
        self.fpga_interface.reset_fifos()

      
    # ====================================================
    # Read FIFO data
    # ====================================================
    def read_fifo_data(self, chip_number, rbuf, receive_array):
        data = self.fpga_interface.pipe_out_fifo(addr.ADDR_PIPE_OUT_FIFO[chip_number], rbuf, receive_array)
    
    
    # ====================================================
    # Read Master FIFO data
    # ====================================================
    def read_master_fifo_data(self, packet):
        self.fpga_interface.pipe_out_master_fifo(packet)
        # return packet.receive_array
    
    
    # ====================================================
    # Read Master FIFO data raw
    # ====================================================
    def read_master_fifo_data_raw(self, rbuf):
        self.fpga_interface.pipe_out_master_fifo_raw(rbuf)
    
    
    # ====================================================
    # Split Master FIFO data into per-chip data
    # ====================================================
    def split_master_fifo_data(self, number_of_chips, frames, patterns_per_frame, data):
        data_list = [ data[chip*frames*patterns_per_frame*1824:(chip+1)*frames*patterns_per_frame*1824] for chip in range(number_of_chips-1, -1, -1)]
        return data_list
    
    # ====================================================
    # Check if read trigger has been sent by chip
    # ====================================================
    def check_read_trigger(self):
        return self.fpga_interface.trigger_out(addr.ADDR_TRIGGER_OUT_DATA_STREAM_READ, sig.TRIGGER_DATA_STREAM_READ)
    
    
    # ====================================================
    # Check if RAM trigger has been sent by chip
    # ====================================================
    def check_ram_trigger(self):
        wire_out = self.fpga_interface.wire_out(addr.ADDR_WIRE_OUT_RAM_READ)
        return bool(wire_out & sig.SIGNAL_RAM_READ)
    
    
    # ====================================================
    # Acknowledge the read trigger
    # ====================================================
    def acknowledge_read_trigger(self):
        return self.fpga_interface.trigger_in(addr.ADDR_TRIGGER_IN_DATA_STREAM_READ_ACK , sig.TRIGGER_DATA_STREAM_READ_ACK)

        
#------------ Signal Out Checks  ---------------------
        
    # ====================================================
    # Check tie hi signals
    # ====================================================
    def check_tie_hi(self):
        wire_out = self.fpga_interface.wire_out(addr.ADDR_WIRE_OUT_SIGNAL)
        print("Tie Hi 1: %d" % ( (wire_out & sig.SIGNAL_TIE_HI_0_) >> sig.TIE_HI_0_INDEX ))
        print("Tie Hi 2: %d" % ( (wire_out & sig.SIGNAL_TIE_HI_1_) >> sig.TIE_HI_1_INDEX ))
    
    
    # ====================================================
    # Check tie lo signals
    # ====================================================
    def check_tie_lo(self):
        wire_out = self.fpga_interface.wire_out(addr.ADDR_WIRE_OUT_SIGNAL)
        print("Tie Lo 1: %d" % ( (wire_out & sig.SIGNAL_TIE_LO_0_) >> sig.TIE_LO_0_INDEX ))
        print("Tie Lo 2: %d" % ( (wire_out & sig.SIGNAL_TIE_LO_1_) >> sig.TIE_LO_1_INDEX ))
        
        
        
#---------------- Power supply convenience functions -----------------
        
    # ====================================================
    # Enable the switch-mode supply for VCSEL cathode bias
    # ====================================================
    def enable_vcsel_cath_sm_supply(self):
        self.tiehi_power_signal('vcsel_cath_sm_enable')
        print("VCSEL Cathode Switch-Mode Power Supply Enabled")
    
    
    # ====================================================
    # Disable the switch-mode supply for VCSEL cathode bias
    # ====================================================
    def disable_vcsel_cath_sm_supply(self):
        self.tielo_power_signal('vcsel_cath_sm_enable')
        print("VCSEL Cathode Switch-Mode Power Supply Disabled")
    
    
    # ====================================================
    # Check the status of the switch-mode supply for VDD
    # ====================================================
    def check_vdd_sm_supply(self):
        out = self.fpga_interface.wire_out(addr.ADDR_WIRE_OUT_SIGNAL)
        #print "WireOut: %s" % bin(out)
        if (out & sig.SIGNAL_VDD_SM_STATUS):
            print("VDD not acceptable")
            return False
        else:
            print("VDD acceptable")
            return True
    
    
    # ====================================================
    # Enable the LDO for HVDD
    # ====================================================
    def enable_hvdd_ldo_supply(self):
        self.tiehi_power_signal('hvdd_ldo_enable')
        print("HVDD LDO Enabled")
    
    
    # ====================================================
    # Disable the LDO for HVDD
    # ====================================================
    def disable_hvdd_ldo_supply(self):
        self.tielo_power_signal('hvdd_ldo_enable')
        print("HVDD LDO Disabled")
    
    
    # ====================================================
    # Enable the LDO for VRST
    # ====================================================
    def enable_vrst_ldo_supply(self):
        self.tiehi_power_signal('vrst_ldo_enable')
        print("VRST LDO Enabled")
        
    
    # ====================================================
    # Disable the LDO for VRST
    # ====================================================
    def disable_vrst_ldo_supply(self):
        self.tielo_power_signal('vrst_ldo_enable')
        print("VRST LDO Disabled")
        
        
    # ====================================================
    # Enable the switch-mode supply for CATH
    # ====================================================
    def enable_cath_sm_supply(self):
        self.tiehi_power_signal('cath_sm_enable')
        print("CATH SM Enabled")
        
    
    # ====================================================
    # Disable the switch-mode supply for CATH
    # ====================================================
    def disable_cath_sm_supply(self):
        self.tielo_power_signal('cath_sm_enable')
        print("CATH SM Disabled")
        
        
    # ====================================================
    # Enable level shifter
    # ====================================================
    def enable_clock_level_shifter(self):
        self.tielo_power_signal('clock_ls_oe_bar')
        print("Clock level shifter enabled")
        

    # ====================================================
    # Disable level shifter
    # ====================================================
    def disable_clock_level_shifter(self):
        self.tiehi_power_signal('clock_ls_oe_bar')
        print("Clock level shifter disabled")


    # ====================================================
    # Set level shifter direction to B->A
    # ====================================================
    def set_clock_level_shifter_for_clock_input(self):
        self.tielo_power_signal('clock_ls_direction')
        print("Clock level shifter set for clock input")


    # ====================================================
    # Set level shifter direction to A->B
    # ====================================================
    def set_clock_level_shifter_for_clock_output(self):
        self.tiehi_power_signal('clock_ls_direction')
        print("Clock level shifter set for clock output")
        
        
    # ====================================================
    # Activate the dynamic features of MOANA3
    # ====================================================
    def activate_dynamic_mode(self, dynamic_packet_obj):
        
        # Set dynamic mode bit high
        self.tiehi_signal('dynamic_mode')
        
        # Pipe in dynamic packet
        self.fpga_interface.pipe_in_pattern(addr.ADDR_PIPE_IN_PATTERN, dynamic_packet_obj.create_pipe_in())
        
        # Indicate dynamic pipe in is done
        self.tiehi_signal('dynamic_pattern_pipe_in_complete')
       
        
    # ====================================================
    # Update the vcsel data bits in the registers
    # ====================================================        
    def update_nir_vcsel_data_bits(self, v1):
        
                               
        if v1 < 0.2:
            raise ValueError("The minium value of NIR bias should be" + str(0.2) + "V" + "!")      
            
        elif v1 > 2.4:
            raise ValueError("The maxium value of NIR bias cannot exceed " + str(2.4) + "V" + "!")     
                
        if (v1 == 0.2):
            div_val_1 = 127
        elif (v1 == 0.3):
            div_val_1 = 125  
        elif (v1 == 0.4):
            div_val_1 = 122              
        elif (v1 == 0.5):
            div_val_1 = 119  
        elif (v1 == 0.6):
            div_val_1 = 115   
        elif (v1 == 0.7):
            div_val_1 = 112  
        elif (v1 == 0.8):
            div_val_1 = 108   
        elif (v1 == 0.9):
            div_val_1 = 104  
        elif (v1 == 1.0):
            div_val_1 = 100   
        elif (v1 == 1.1):
            div_val_1 = 96  
        elif (v1 == 1.2):
            div_val_1 = 91   
        elif (v1 == 1.3):
            div_val_1 = 86  
        elif (v1 == 1.4):
            div_val_1 = 81              
        elif (v1 == 1.5):
            div_val_1 = 75  
        elif (v1 == 1.6):
            div_val_1 = 70   
        elif (v1 == 1.7):
            div_val_1 = 64  
        elif (v1 == 1.8):
            div_val_1 = 57   
        elif (v1 == 1.9):
            div_val_1 = 50  
        elif (v1 == 2.0):
            div_val_1 = 43   
        elif (v1 == 2.1):
            div_val_1 = 35  
        elif (v1 == 2.2):
            div_val_1 = 27    
        elif (v1 == 2.3):
            div_val_1 = 18  
        else:
            div_val_1 = 8    
            
        return div_val_1
    
    # ====================================================
    # Update the vcsel data bits in the registers
    # ====================================================        
    def update_ir_vcsel_data_bits(self, v2):
        
                               
        # max_data_bits = 2**7-1
        
        if v2 < 0.2:
            raise ValueError("The minium value of IR bias should be (" + str(0.2) + ")" + "!")      
            
        elif v2 > 2.4:
            raise ValueError("The maxium value of IR bias cannot exceed (" + str(2.4) + ")" + "!")      
                
        elif (v2 == 0.2):
            div_val_2 = 127
        elif (v2 == 0.3):
            div_val_2 = 125  
        elif (v2 == 0.4):
            div_val_2 = 122              
        elif (v2 == 0.5):
            div_val_2 = 119  
        elif (v2 == 0.6):
            div_val_2 = 115   
        elif (v2 == 0.7):
            div_val_2 = 112  
        elif (v2 == 0.8):
            div_val_2 = 108   
        elif (v2 == 0.9):
            div_val_2 = 104  
        elif (v2 == 1.0):
            div_val_2 = 100   
        elif (v2 == 1.1):
            div_val_2 = 95  
        elif (v2 == 1.2):
            div_val_2 = 90   
        elif (v2 == 1.3):
            div_val_2 = 85  
        elif (v2 == 1.4):
            div_val_2 = 80              
        elif (v2 == 1.5):
            div_val_2 = 75  
        elif (v2 == 1.6):
            div_val_2 = 69   
        elif (v2 == 1.7):
            div_val_2 = 63  
        elif (v2 == 1.8):
            div_val_2 = 56   
        elif (v2 == 1.9):
            div_val_2 = 49  
        elif (v2 == 2.0):
            div_val_2 = 42   
        elif (v2 == 2.1):
            div_val_2 = 34  
        elif (v2 == 2.2):
            div_val_2 = 25    
        elif (v2 == 2.3):
            div_val_2 = 17  
        else:
            div_val_2 = 7    
            
        return div_val_2
         
    # ====================================================
    # update vcsel data bits
    # ====================================================
    def update_vcsel_data_bits(self, v1, v2):
        div_val_1 = self.update_nir_vcsel_data_bits(v1)
        div_val_2 = self.update_ir_vcsel_data_bits(v2)
        
        vcsel_data_val = (div_val_2 << 8) + div_val_1 
        
        self.fpga_interface.wire_in(addr.ADDR_WIREIN_VCSEL_DATA_BITS, vcsel_data_val)  
        
    # ====================================================
    # Activate input vcsel trigger
    # ====================================================
    def vcsel_enable_trigger(self):
        return self.fpga_interface.trigger_in(addr.ADDR_TRIGGERIN_VCSELENABLE , sig.TRIGGER_VCSEL_ENABLE)        
        