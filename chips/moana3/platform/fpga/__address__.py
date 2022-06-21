#-------------------------------------------------------------------------
# __addresses__.py
#
# Define command and control addresses for talking to FPGA
#-------------------------------------------------------------------------

# Scan Command Protocols
CMD_SCAN_READ =                         0x000C
CMD_SCAN_WRITE =                        0x0004
# Deprecated
CMD_RESET =                             0xFFFF
CMD_RESET_SCAN =                        0xFFFF

# Address Definitions
ADDR_WIRE_IN_MSGCTRL =                  0x00
ADDR_WIRE_IN_SIGNAL =                   0x01
ADDR_WIRE_IN_POWER =                    0x02
ADDR_WIRE_IN_FRAME =                    0x03
ADDR_WIRE_IN_PATTERN =                  0x04
ADDR_WIRE_IN_MEASUREMENT =              0x05
ADDR_WIRE_IN_FRAMECTRL =                0x06
ADDR_WIRE_IN_TRANSFER_SIZE =            0x07
ADDR_WIRE_IN_STREAM =                   0X08
ADDR_WIRE_OUT_STATUS =                  0x20
ADDR_WIRE_OUT_SIGNAL =                  0x21
ADDR_WIRE_OUT_FIFO_01_COUNT =           0x22
ADDR_WIRE_OUT_FIFO_11_COUNT =           0x23
ADDR_WIRE_OUT_FIFO_STATUS =             0x24
ADDR_WIRE_OUT_REGBANK_LSB =             0x25
ADDR_WIRE_OUT_REGBANK_MSB =             0x26
ADDR_WIRE_OUT_FIFO_SIZE =               0x27
ADDR_TRIGGER_IN_DATA_STREAM_READ_ACK =  0x40
ADDR_TRIGGER_OUT_DATA_STREAM_READ =     0x60
ADDR_PIPE_IN_SCAN =                     0x80
ADDR_PIPE_IN_PATTERN =                  0x81
ADDR_PIPE_OUT_SCAN =                    0xA0
ADDR_PIPE_OUT_FIFO =                   [0xA1 + i for i in range(16)]
ADDR_PIPE_OUT_FIFO_MASTER =             0XB8

