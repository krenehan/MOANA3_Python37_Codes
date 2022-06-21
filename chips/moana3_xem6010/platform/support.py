import time

# Finds the 2's complement integer of a binary string
def bin2int_twos_comp(bits):
    length = len(bits)
    val = int(bits, 2)
    if( (val & (1 << (length-1))) != 0 ):
        val = val - (1 << length)
    return val

# Inverts the bits in a bit string
def invert_bits(bit_string):
    return reduce(lambda x, y: x + ('0' if y == '1' else '1'), bit_string, '')

# Splits the string into substrings at every 'bits_per_way'
# Expects bits_per_way * serdes_ratio number of bits
# Note that the highest numbered way is at substring index 0, just from
# the nature of how python prints its strings
def way_split(bits, bits_per_way, ser_des_ratio):
    expected_length = bits_per_way * ser_des_ratio
    if len(bits) != expected_length:
        raise ValueError("Expected " + str(expected_length) + " bits, got " + str(len(bits)) + "!")    
    bits_list = []
    for i in range(0, ser_des_ratio):
        bits_list.append(bits[expected_length-(i+1)*bits_per_way:expected_length-i*bits_per_way])
    return bits_list

# Returns a concatenated bit string using the bits in bits list,
# with each entry in the bits list corresponding to a serdes way
def way_set(bits_list, bits_per_way, ser_des_ratio):
    expected_length = bits_per_way * ser_des_ratio
    bits = ''
    for i in range(ser_des_ratio-1, -1, -1):
        bits += bits_list[i]
    if len(bits) != expected_length:
        raise ValueError("Expected " + str(expected_length) + " bits, got " + str(len(bits)) + "!")    
    return bits

# Prints the bits as a string separated by 'bits_per_way' using the way_split
# function. An optional format function is used to print the string in a
# specific way
def way_print(bits, bits_per_way, ser_des_ratio, format = lambda way, bits: "    Way %d: %s" % (way, bits)):
    bits_list = way_split(bits, bits_per_way, ser_des_ratio)
    for i in range(0, ser_des_ratio):
        print(format(i, bits_list[i]))

# For the given list of cells in the given row, perform the following
# function with arguments passed to it using **funargs
# Returns a dict of return results of for the function
def do_for_cells(dut, row, cells, fun, *funargs, **funkwargs):
    out = ()
    for cell in cells:
        # Convert anything in **funargs that is cell_dict
        rawargs = []
        for value in funargs:            
            rawargs.append(value.data[cell] if isinstance(value, cell_dict) else value)
        
        # Convert annthing in **funkwargs that is a cell_dict
        rawkwargs = dict()
        for key, value in funkwargs.items():
            rawkwargs[key] = value.data[cell] if isinstance(value, cell_dict) else value

        # Call the function, get the output
        out_tup = fun(dut, row, cell, *rawargs, **rawkwargs)
        if out_tup:
            # Add everything from the output tuple into the correct cell_dict()
            for i in range(len(out_tup)):
                # If output tuple does not have enough length, extend it
                if i >= len(out):
                    out = out + (cell_dict(), )
                # Add to the cell_dict() of the output tuple
                out[i].data[cell] = out_tup[i]
        
    return out
    
# Basically a dict, but only used in conjunction with the do_for_cells method.
# It is not a pretty solution, but it makes things a lot easier
class cell_dict:
    def __init__(self):
        self.data = dict()
    
# Integer to binary, this will return a bit string
def int2bin(n, count=8):
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

# Like range, but with floats
def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L

