import scan_chains.base_scan_chain as base_scan_chain
import scan_chains.DigitalCore_scan_bits as DigitalCore_scan_bits

class DigitalCoreScanChain(base_scan_chain.BaseScanChain):

    def __init__(self, row_number = -1, number_multicells_per_row = 1):
        
        parent = base_scan_chain.BaseScanChain()

        self.row_number = parent.row_number
        self.scan_chain_segment_names = parent.scan_chain_segment_names
        self.scan_chain = parent.scan_chain
        self.number_scan_chain_segments = parent.number_scan_chain_segments
        self.scan_chain_length = parent.scan_chain_length
        
        self.row_number = row_number
        if self.row_number < 0:
            raise Exception("Multicell row number is not defined correctly.")

        self.number_multicells_per_row = number_multicells_per_row

        # create the scan chain segment names
        self.clear_scan_chain_segment_names()
        for i in range(self.number_multicells_per_row):
            self.scan_chain_segment_names.append('multicell_' + str(i))

        # instantiate the slice scan chain segments
        for i in range(self.number_multicells_per_row):
            self.add_new_scan_chain_segment(self.scan_chain_segment_names[i], DigitalCore_scan_bits.DigitalCore_scan_bits())


    def reset_all_scan_bits(self):

        # delete all scan chains
        self.clear_scan_chain_segments()

        # instantiate the slice scan chain segments
        for i in range(self.number_multicells_per_row):
            self.add_new_scan_chain_segment(self.scan_chain_segment_names[i], DigitalCore_scan_bits.DigitalCore_Scan_Bits())

    
    @classmethod
    def scan_chain_from_bits(cls, bits, number_packet_bits, row_number = -1, number_multicells_per_row = 4):
    
        # get the length of each scan chain segment
        DigitalCore_scan_chain_length  = DigitalCore_scan_bits.DigitalCore_scan_bits().length()
        
        # create the scan chain segment names
        scan_chain_segment_names = []
        for i in range(number_multicells_per_row):
            scan_chain_segment_names.append('multicell_' + str(i))

        # create the class instance
        DigitalCore_scan_chain = cls(row_number, number_multicells_per_row)

        # delete all scan chains
        DigitalCore_scan_chain.clear_scan_chain_segments()

        # create new scan chain names
        DigitalCore_scan_chain.set_scan_chain_segment_names(scan_chain_segment_names)

        # instantiate the slice scan chain segments from bits
        for i in range(number_multicells_per_row):
            DigitalCore_scan_chain.add_new_scan_chain_segment( \
                scan_chain_segment_names[i], \
                DigitalCore_scan_bits.DigitalCore_scan_bits.from_bits( \
                    bits[number_packet_bits-64-(DigitalCore_scan_chain_length*(i+1)):number_packet_bits-64-(DigitalCore_scan_chain_length*i)] \
                ) \
            )

        # return the instance
        return(DigitalCore_scan_chain)
        

