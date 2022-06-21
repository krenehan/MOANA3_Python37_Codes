#-------------------------------------------------------------------------
# __signal__.py
#
# Define signals to the chip
#-------------------------------------------------------------------------

# Software In Signals
SIGNAL_SCAN_RST =               0x0001
SIGNAL_CELL_RST =               0x0002

# Software In Power Signals
SIGNAL_VRST_ADJ_ENABLE =        0x0001
SIGNAL_VDD_SM_ENABLE =          0x0002
SIGNAL_VDD_LDO_ENABLE =         0x0004
SIGNAL_HVDD_LDO_ENABLE =        0x0008
SIGNAL_VRST_LDO_ENABLE =        0x0010
SIGNAL_VRST_POT_CODE0_ =        0x0020
SIGNAL_VRST_POT_CODE1_ =        0x0040
SIGNAL_VRST_POT_CODE2_ =        0x0080
SIGNAL_VRST_POT_CODE3_ =        0x0100
SIGNAL_VRST_POT_CODE4_ =        0x0200
SIGNAL_VRST_POT_CODE5_ =        0x0400
SIGNAL_VCSEL_CATH_SM_ENABLE =   0x0800
SIGNAL_CLOCK_LS_DIRECTION =     0x1000
SIGNAL_CLOCK_LS_OE_BAR =        0x2000
SIGNAL_LEVEL_SHIFTER_ENABLE=    0x4000
SIGNAL_CATH_SM_ENABLE =         0x8000

# Trigger Ins
TRIGGER_DATA_STREAM_READ_ACK = 0x0000

# Trigger Outs
TRIGGER_DATA_STREAM_READ =      0x0000

# Software Out Indexes
TIE_LO_0_INDEX =                0
TIE_HI_0_INDEX =                1
TIE_LO_1_INDEX =                2
TIE_HI_1_INDEX =                3
VDD_SM_STATUS_INDEX =           4
VRST_HIGH_INDEX =               9

# Software Out Signals 
SIGNAL_TIE_LO_0_ =              1 << TIE_LO_0_INDEX
SIGNAL_TIE_HI_0_ =              1 << TIE_HI_0_INDEX
SIGNAL_TIE_LO_1_ =              1 << TIE_LO_1_INDEX
SIGNAL_TIE_HI_1_ =              1 << TIE_HI_1_INDEX
SIGNAL_VDD_SM_STATUS =          1 << VDD_SM_STATUS_INDEX
SIGNAL_VRST_HIGH =              1 << VRST_HIGH_INDEX

# FIFO Status Signals - Chip 1
SIGNAL_FIFO_00_FULL =           0x0001
SIGNAL_FIFO_01_FULL =           0x0002
SIGNAL_FIFO_00_OVERFLOW =       0x0004
SIGNAL_FIFO_01_OVERFLOW =       0x0008
SIGNAL_FIFO_00_EMPTY =          0x0010
SIGNAL_FIFO_01_EMPTY =          0x0020
SIGNAL_FIFO_00_UNDERFLOW =      0x0040
SIGNAL_FIFO_01_UNDERFLOW =      0x0080

# FIFO Status Signals - Chip 2
SIGNAL_FIFO_10_FULL =           0x0100
SIGNAL_FIFO_11_FULL =           0x0200
SIGNAL_FIFO_10_OVERFLOW =       0x0400
SIGNAL_FIFO_11_OVERFLOW =       0x0800
SIGNAL_FIFO_10_EMPTY =          0x1000
SIGNAL_FIFO_11_EMPTY =          0x2000
SIGNAL_FIFO_10_UNDERFLOW =      0x4000
SIGNAL_FIFO_11_UNDERFLOW =      0x8000
