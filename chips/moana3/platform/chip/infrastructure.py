import scan_chains.DigitalCore_scan_chain
import __signal__

class Infrastructure:
    # == Scan Chain Row Number Mapping ==
    # Multicells            scan rows 0 - 1


    def __init__(self, number_multicell_rows = 1, number_multicells_per_row = 1):
        
        # set row parameters
        self.number_multicell_rows                 = number_multicell_rows
        self.number_multicells_per_row             = number_multicells_per_row

        self.hsclock_control_cell_number    = 0

        # create the scan chain rows
        self.scan_chains = {}
        self.chain_names = []

        # create multicell scan chain row names
        for i in range(number_multicell_rows):
            self.chain_names.append('chip_row_' + str(i))

        # Scan chain rows
        self.multicell_row_start = 0;        

        # instantiate multicell rows
        for i in range(self.multicell_row_start, number_multicell_rows):
            self.scan_chains[self.chain_names[i]] = scan_chains.DigitalCore_scan_chain.DigitalCoreScanChain(i, self.number_multicells_per_row)            

        # create signal name to signal val mapping
        self.chip_signal = {}

        self.chip_signal['cell_reset'] =                __signal__.SIGNAL_CELL_RST
        self.chip_signal['scan_reset'] =                __signal__.SIGNAL_SCAN_RST
        
        # Software in power signals
        self.chip_signal['hvdd_ldo_enable'] =           __signal__.SIGNAL_HVDD_LDO_ENABLE
        self.chip_signal['vrst_ldo_enable'] =           __signal__.SIGNAL_VRST_LDO_ENABLE
        self.chip_signal['clock_ls_direction'] =        __signal__.SIGNAL_CLOCK_LS_DIRECTION
        self.chip_signal['clock_ls_oe_bar'] =           __signal__.SIGNAL_CLOCK_LS_OE_BAR
        self.chip_signal['cath_sm_enable'] =            __signal__.SIGNAL_CATH_SM_ENABLE
        self.chip_signal['vcsel_cath_sm_enable'] =      __signal__.SIGNAL_VCSEL_CATH_SM_ENABLE
        self.chip_signal['ref_clk_mmcm_enable'] =       __signal__.SIGNAL_REF_CLK_MMCM_ENABLE
        self.chip_signal['clk_select_0'] =              __signal__.SIGNAL_CLK_SELECT_0
        self.chip_signal['clk_select_1'] =              __signal__.SIGNAL_CLK_SELECT_1
        
        

    # update the scan chain bits from the data received from FPGA
    def update_scan_chain_bits(self, chain_name, data, number_packet_bits):
        row_number = self.scan_chains[chain_name].get_scan_chain_row_number()
        
        # create new scan chains from the data
        # Kind of annoying, but have to do this
        new_scan_chain = self.scan_chains[chain_name].scan_chain_from_bits(data, number_packet_bits, row_number, self.number_multicells_per_row)

        # replace the old scan chain with the new one
        self.scan_chains[chain_name] = new_scan_chain

    def get_hsclock_control_cell_number(self):
        return(self.hsclock_control_cell_number)

    def get_scan_chain(self, chain_name):
        return(self.scan_chains[chain_name])

    def set_scan_chain(self, chain_name, scan_chain):
        self.scan_chains[chain_name] = scan_chain

    def set_chip_signal(self, signal_name, signal_val):
        self.chip_signal[signal_name] = signal_val

    def get_chip_signal(self, signal_name):
        return(self.chip_signal[signal_name])




















