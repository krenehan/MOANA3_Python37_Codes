

class BaseScanChain:

    def __init__(self):
        # scan chain row number
        self.row_number = -1
        # scan chain names and scan chain instance dictionary
        self.scan_chain_segment_names = []
        self.scan_chain = {}
        # number of scan chain segments
        self.number_scan_chain_segments = 0
        # scan chain total length
        self.scan_chain_length = 0

    # clear scan chain segment names
    def clear_scan_chain_segment_names(self):
        self.scan_chain_segment_names = []

    # set scan chain segment names
    def set_scan_chain_segment_names(self, new_scan_chain_segment_names):
        self.scan_chain_segment_names = new_scan_chain_segment_names

    # clear everything in the scan chain
    def clear_scan_chain_segments(self):
        self.scan_chain = {}
        self.number_scan_chain_segments = 0
        self.scan_chain_length = 0

    # add new scan chain segment to the current scan chain
    def add_new_scan_chain_segment(self, new_scan_chain_segment_name, new_scan_chain_segment):
        self.scan_chain[new_scan_chain_segment_name] = new_scan_chain_segment
        self.number_scan_chain_segments += 1
        self.scan_chain_length += new_scan_chain_segment.length()

    # reset all scan chain segment bits to zero - need to rebind the dictionary, so not implemented here
    def reset_all_scan_bits(self):
        raise NotImplementedError("reset_all_scan_bits is virtual.")
    
    def get_scan_chain_row_number(self):
        if self.row_number < 0:
            raise Exception("scan chain row number is not defined correctly")
        return(self.row_number)
        
    def get_number_scan_chain_segments(self):
        return self.number_scan_chain_segments

    def get_scan_chain_length(self):
        return(self.scan_chain_length)

    def get_scan_chain_segment(self, scan_chain_segment_name):
        return(self.scan_chain[scan_chain_segment_name])

    # return the scan chain data as a bit string
    def scan_chain_to_bits(self):
        if len(self.scan_chain) != self.number_scan_chain_segments:
            raise Exception("Error, Number of scan chain " + self.number_scan_chain_segments + " != scan chain list length " + len(self.scan_chain) + "!")

        if len(self.scan_chain) != len(self.scan_chain_segment_names):
            raise Exception("Error, Number of scan chain names" + len(self.scan_chain_segment_names) + " != scan chain list length " + len(self.scan_chain) + "!")

        bits = ''
        for i in range(len(self.scan_chain_segment_names)):
            bits = self.scan_chain[self.scan_chain_segment_names[i]].to_bits() + bits

        return(bits)

    # return the scan chain class from the received bits
    @classmethod
    def scan_chain_from_bits(cls, bits):
        raise NotImplementedError("scan_chain_from_bits is virtual.")








