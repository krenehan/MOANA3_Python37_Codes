#-------------------------------------------------------------------------
# interface.py
#
# Define the interface functions for talking to the FPGA
#-------------------------------------------------------------------------
import ok
from numpy import binary_repr, floor, ceil, dtype, uint16, flip, frombuffer
import __address__ 

class Interface:

    # ====================================================
    # Initialize the FPGA interface
    # ====================================================
    def __init__(self, fpga_packet_length):

        self.max_tries = 2000
        self.packet_length = fpga_packet_length;
        self.xem = ok.FrontPanel()

        # Try connecting to the FPGA
        if (self.xem.NoError != self.xem.OpenBySerial("")):
            print("A device could not be opened.  Is one connected?")
            return(False)
            
        # Get device info
        self.deviceInfo = ok.okTDeviceInfo()
        self.xem.GetDeviceInfo(self.deviceInfo)
            
#        if (self.deviceInfo.productID == self.xem.brdXEM6010LX45):
#            print("Device model: XEM6010")

        self.xem.LoadDefaultPLLConfiguration()
            
        if (self.deviceInfo.productID == self.xem.brdXEM6010LX45):
            self.pll = ok.PLL22393()
            self.xem.GetPLL22393Configuration(self.pll)
        
        # Datatype for byte interpretation
        self.dt = dtype(uint16)
        self.dt = self.dt.newbyteorder('>')

        # Get some general information about the device.
#        print("Device ID: %s" % self.xem.GetDeviceID())
#        print("Device firmware version: %d.%d" % (self.xem.GetDeviceMajorVersion(), self.xem.GetDeviceMinorVersion()))
#        print("Device serial number: %s" % self.xem.GetSerialNumber())


    # ====================================================
    # Configure the FPGA with a bitfile
    # ====================================================
    def configure(self, bitfile):
        if(self.xem.NoError != self.xem.ConfigureFPGA(bitfile)):
            print(self.xem.ConfigureFPGA(bitfile))
            raise Exception("FPGA configuration failed. Bitfile: %s" % bitfile)
        # Issue software reset
        self.reset()
    
    
    # ====================================================
    # Reset the FPGA
    # ====================================================
    def reset(self):
        # Toggle the Software Reset pin
        self.wire_in(__address__.ADDR_WIRE_IN_MSGCTRL, 0x0008)
        self.wire_in(__address__.ADDR_WIRE_IN_MSGCTRL, 0x0000)


    # ====================================================
    # Initialize the PLL - Initialized to 200 MHz operation
    # Output 0 sources RefClk if using internal clocks
    # Output 1 sources TxRefClk if using internal clocks or external refclk
    # Output 2 always sources 100 MHz clock for DRAM
    # ====================================================
    def initPLL(self, refclk_freq, tx_refclk_freq):
        
        # PLL frequency
        pll_freq = 200e6
        
        # DRAM frequency MUST be 100 MHz, so double checking happens here
        dram_div = int(pll_freq / 100e6)
        dram_freq_val = int(pll_freq / dram_div / 1e6)
        if dram_freq_val != 100:
            raise Exception("DRAM frequency must be 100 MHz, but was calculated as " + str(dram_freq_val) + " MHz")
        
        # Find the divider value
        refclk_divider, tx_refclk_divider = self.getDividerValues(refclk_freq, tx_refclk_freq, pll_freq)
        
        # PLL reference clock is the USB clocks, which is roughly 48 MHz
        self.pll.SetReference(float(48))
        #self.pll.SetPLLParameters(0, int(refclk_freq/1e6), 48, True)
        # PLL output frequency set to 200 MHz
        self.pll.SetPLLParameters(0, int(pll_freq/1e6), 48, True)
        
        # RefClk setup as clk0 with desired frequency
        self.pll.SetOutputSource(0, ok.okCPLL22393.ClkSrc_PLL0_0)
        self.pll.SetOutputDivider(0, refclk_divider)
        self.pll.SetOutputEnable(0, True)
        
        # TxRefClk set up as clk1 with desired frequency
        self.pll.SetOutputSource(1, ok.okCPLL22393.ClkSrc_PLL0_0)
        self.pll.SetOutputDivider(1, tx_refclk_divider)
        self.pll.SetOutputEnable(1, True)
        
        # DRAM clock set up as clk2 at 100 MHz
        self.pll.SetOutputSource(2, ok.okCPLL22393.ClkSrc_PLL0_0)
        self.pll.SetOutputDivider(2, dram_div)
        self.pll.SetOutputEnable(2, True)
        
        # Changes pushed to FPGA
        if (self.xem.SetPLL22393Configuration(self.pll) == self.xem.NoError):
            print("PLL configured")
            print("Output frequency for RefClk is " + str(round(self.pll.GetOutputFrequency(0), 2)) + " MHz")
            print("Output frequency for TxRefClk is " + str(round(self.pll.GetOutputFrequency(1), 2)) + " MHz")
            print("Output frequency for DRAM is " + str(round(self.pll.GetOutputFrequency(2), 2)) + " MHz")
        else:
            raise Exception("PLL not configured correctly")
            
            
    # ====================================================
    # Find divider values for clocks
    # ====================================================
    def getDividerValues(self, refclk_freq, tx_refclk_freq, pll_freq):
        
        # Dividers if we could set a decimal divider
        refclk_float_divider = pll_freq / refclk_freq
        tx_refclk_float_divider = pll_freq / tx_refclk_freq
        
        # Default refclk divider set to the lower bound
        refclk_divider = int( floor( refclk_float_divider ) )
        
        # Default txrefclk divider to upper bound
        tx_refclk_divider = int( ceil( tx_refclk_float_divider ) )
        
        
        # Loop until we find a value that works
        refclk_acceptable = False
        tx_refclk_acceptable = False
        while not (refclk_acceptable and tx_refclk_acceptable):
            
            # Calculate actual value of clock frequencies
            real_refclk_freq = pll_freq / refclk_divider
            real_tx_refclk_freq = pll_freq / tx_refclk_divider
            
            # Increment or decrement reclk divider
            if (real_refclk_freq > 100e6):
                refclk_divider += 1
            elif (real_refclk_freq < 20e6):
                refclk_divider -= 1
            else:
                refclk_acceptable = True
            
            # Increment or decrement tx_refclk divider
            if (real_tx_refclk_freq > 25e6):
                tx_refclk_divider += 1
            elif (real_tx_refclk_freq < 1e6):
                tx_refclk_divider -= 1
            else:
                tx_refclk_acceptable = True
        
        # Return
        return refclk_divider, tx_refclk_divider
        
    
    # ====================================================
    # Wait for the pipe in to be ready
    # ====================================================
    def wait_pipe_in_ready(self):
        # Poll the tx pipe buffer until it is ready
        tries = 0
        for tries in range(0, self.max_tries, 100):
            for i in range(100):
                msg_stat = self.wire_out(__address__.ADDR_WIRE_OUT_STATUS)
                if(msg_stat & 0x0001 == 0x0001):
                    return(True)                    
            print("FPGA still not ready for pipe in after %d tries..." % tries)            
        raise Exception("Max tries (%d) reached" % self.max_tries)


    # ====================================================
    # Wait for the pipe out to be ready
    # ====================================================
    def wait_pipe_out_valid(self):
        # Poll the OK interface until it has valid data
        tries = 0
        for tries in range(0, self.max_tries, 100):
            for i in range(100):
                msg_stat = self.wire_out(__address__.ADDR_WIRE_OUT_STATUS)
                if(msg_stat & 0x0002 == 0x0002):
                    return(True)
            print("Rx pipe still not valid after %d tries..." % tries)
        raise Exception("Max tries (%d) reached" % self.max_tries)


    # ====================================================
    # Pipe data into the FPGA
    # ====================================================
    def pipe_in(self, addr, data, num_bytes):
        outbuffer = self.encode_data(data, num_bytes)
        self.wait_pipe_in_ready()
        # Changed with new OK front panel version
        #self.xem.WriteToPipeIn(addr, outbuffer)
        self.xem.WriteToPipeIn(addr, outbuffer)
        return(outbuffer)
    
    
    # ====================================================
    # Pipe data into the FPGA
    # ====================================================
    def pipe_in_pattern(self, addr, buf):
        self.xem.WriteToPipeIn(addr, buf)

    # ====================================================
    # Pipe data out of the FPGA
    # ====================================================
    def pipe_out(self, addr):
        # Grab Data returned (expecting 2*self.packet_length bytes)
        # Changed with new OK front panel version
        #rbuffer = '\x00'*2*self.packet_length
        rbuf = bytearray(2*self.packet_length)
        self.wait_pipe_out_valid()
        # Changed with new OK front panel version
        #self.xem.ReadFromPipeOut(addr, rbuffer)
        self.xem.ReadFromPipeOut(addr, rbuf)
        # Changed with new OK front panel version
        # print(rbuf)
        #rbuf = "".join(map(chr, rbuf))
        # flip bytes & get binary data
        # Changed with new OK front panel version
        #rbuffer = self.decode_data(rbuffer)
        # print(len(rbuf))
        rbuffer = self.decode_data(rbuf)
        return(rbuffer)


    # ====================================================
    # Wire in data
    # ====================================================
    def wire_in(self,addr,val):
        # Address, Value, Mask?
        self.xem.SetWireInValue(addr, val)
        self.xem.UpdateWireIns()


    # ====================================================
    # Wire out data
    # ====================================================
    def wire_out(self,addr):
        self.xem.UpdateWireOuts()
        return self.xem.GetWireOutValue(addr)
    
    
    # ====================================================
    # Trigger out data
    # ====================================================
    def trigger_out(self, addr, mask):
        self.xem.UpdateTriggerOuts()
        return self.xem.IsTriggered(addr, 1 << mask)
    
    # ====================================================
    # Trigger in data
    # ====================================================
    def trigger_in(self, addr, bit):
        self.xem.ActivateTriggerIn(addr, bit)
    
    # ====================================================
    # Write the scan chain through the scan pipe
    # ====================================================
    def write_scan_chain(self, data):
        seq = data + binary_repr(__address__.CMD_SCAN_WRITE, 16)
        return self.pipe_in(__address__.ADDR_PIPE_IN_SCAN, seq, 2*self.packet_length)

    
    # ====================================================
    # Read the scan chain request from the scan pipe
    # ====================================================
    def read_scan_chain_request(self, data):
        seq = data + binary_repr(__address__.CMD_SCAN_READ, 16)
        return self.pipe_in(__address__.ADDR_PIPE_IN_SCAN, seq, 2*self.packet_length)


    # ====================================================
    # Read scan chain data from scan pipe
    # ====================================================
    def read_scan_chain_data(self):
        return self.pipe_out(__address__.ADDR_PIPE_OUT_SCAN)


    # ====================================================
    # Wire in to the signal wire
    # ====================================================
    def wire_in_signal(self, val):
        self.wire_in(__address__.ADDR_WIRE_IN_SIGNAL, val)
        
        
    # ====================================================
    # Wire in to the power wire
    # ====================================================
    def wire_in_power_signal(self, val):
        self.wire_in(__address__.ADDR_WIRE_IN_POWER, val)

        
###############################################################################   

    # ====================================================
    # Reset FIFOs
    # ====================================================
    def reset_fifos(self):
        self.wire_in(__address__.ADDR_WIRE_IN_MSGCTRL, 0x0010)
        self.wire_in(__address__.ADDR_WIRE_IN_MSGCTRL, 0x0000)
 

    # ====================================================
    # Pipe out FIFO data
    # ====================================================
    def pipe_out_fifo(self, addr, packet):
        
        # Read from pipe
        self.xem.ReadFromPipeOut(addr, packet.rbuf)

        # Fill read buffer
        self.decode_data_fifo(packet.rbuf, packet.receive_array)
        

    # ====================================================
    # Read Master FIFO data
    # ====================================================
    def pipe_out_master_fifo(self, packet):
        
        # Read from pipe
        self.xem.ReadFromPipeOut(__address__.ADDR_PIPE_OUT_FIFO_MASTER, packet.rbuf)
        
        # Fill read buffer
        self.decode_data_fifo(packet)
        
    
    def pipe_out_master_fifo_to_string(self, packet):
        
        # Read from pipe
        self.xem.ReadFromPipeOut(__address__.ADDR_PIPE_OUT_FIFO_MASTER, packet.rbuf)
        
        # Fill read buffer
        return self.decode_data_fifo_to_string(packet)
    
    
    # ====================================================
    # Read Master FIFO data
    # Read buffer should already be allocated, decoding is not done here, but done later when reading log file
    # No return value from this function. rbuf is modified directly and used at the top level
    # ====================================================
    def pipe_out_master_fifo_raw(self, packet):
        
        # Read from pipe
        self.xem.ReadFromPipeOut(__address__.ADDR_PIPE_OUT_FIFO_MASTER, packet.rbuf)


    #==========================================================================
    # Methods for encoding/decoding data to be streamed into the OK board
    # Looks confusing, DO NOT MODIFY
    #==========================================================================
    def encode_data(self, dataseq, num_bytes):
        # Expect 'dataseq' to be in order of [MSB:LSB] where
        # LSB bytes will get shifted in first so (LSB,MSB)(LSB,MSB),etc..        
        dbuffer = list(dataseq)
        sbuffer = bytearray()#""
        dsize = int(ceil(len(dbuffer)/16.0))
        # Need to send bytes at a time, but Opal Kelly interface
        # expects 16-bit words on the other end
        for i in range(dsize):
            tmp = int(''.join(dbuffer[len(dbuffer)-16:]),2)
            dbuffer = dbuffer[:len(dbuffer)-16]
            tmp = hex(tmp).split('x').pop().zfill(4)
            # We also need to send LSB byte first, then MSB byte
            # So break up by 16-bit words & swap MSB & LSB bytes
            tmp = list(tmp)
            tmp[:4] = tmp[2],tmp[3],tmp[0],tmp[1]
            tmp = ''.join(tmp)
            sbuffer += bytes.fromhex(tmp) #tmp.decode('hex')
        # Verilog controller expects us to write XX bytes of data
        # before shipping off the data to the Scan controller
        for i in range(num_bytes-dsize*2):
            sbuffer += b"\x00"
        return(sbuffer)
    

    def decode_data(self, dataseq):
        # print("Length of dataseq: " + str(len(dataseq)))
        rdata_temp = [hex(dataseq[i]).split('x')[1].zfill(2) for i in range(len(dataseq))]
        rdata = list("".join(rdata_temp))
        # print("Length of rdata is " + str(len(rdata)))
        dsize = int(ceil(len(rdata)/4.0))
        # print("Data size is " + str(dsize))
        rbuffer = ""
        for i in range(dsize):
            rdata[i*4], rdata[i*4+2] = rdata[i*4+2], rdata[i*4]
            rdata[i*4+1], rdata[i*4+3] = rdata[i*4+3], rdata[i*4+1]
            tmp = binary_repr(int(''.join(rdata[i*4:i*4+4]),16),16)
            rbuffer += tmp
        return(rbuffer)
    
    
    def decode_data_fifo(self, packet):
        packet.data =  flip(frombuffer(packet.rbuf, dtype=self.dt)).astype(int)
        # packet.data =  frombuffer(packet.rbuf, dtype=self.dt).astype(int)
        
    def decode_data_fifo_to_string(self, packet):
        rbuffer = ""
        for i in range(len(packet.rbuf)):
            rbuffer = rbuffer + binary_repr(packet.rbuf[i], 8)
        return rbuffer
        

    #==========================================================================
