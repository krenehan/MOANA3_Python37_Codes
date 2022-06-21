#-------------------------------------------------------------------------
# interface.py
#
# Define the interface functions for talking to the FPGA
#-------------------------------------------------------------------------
import ok
from numpy import binary_repr, floor, ceil, dtype, uint32, flip, frombuffer
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
        
        # Datatype for byte interpretation
        self.dt = dtype(uint32)
        self.dt = self.dt.newbyteorder('>')

        # Get some general information about the device.
        print("Device ID: %s" % self.xem.GetDeviceID())
        print("Device firmware version: %d.%d" % (self.xem.GetDeviceMajorVersion(), self.xem.GetDeviceMinorVersion()))
        print("Device serial number: %s" % self.xem.GetSerialNumber())


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
