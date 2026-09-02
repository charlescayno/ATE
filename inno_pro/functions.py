import ctypes as ct
from ctypes import c_uint32

# UINT16
class u16_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("byte2",                c_uint32, 8),   # LSB
        ("byte1",                c_uint32, 8)]    # MSB
class u16(ct.Union):
    _fields_ = [("bits", u16_bits),
                ("asbyte", c_uint32)]
    def bytes(self):
        bits = self.bits

        self.bytes = [bits.byte1,
                      bits.byte2]
        return self.bytes

# UINT32
class u32_bits(ct.LittleEndianStructure):
    _fields_ = [
        ("byte4",                c_uint32, 8),   # LSB
        ("byte3",                c_uint32, 8),
        ("byte2",                c_uint32, 8),
        ("byte1",                c_uint32, 8)]   # MSB
class u32(ct.Union):
    _fields_ = [("bits", u32_bits),
                ("asbyte", c_uint32)]
    def bytes(self):
        bits = self.bits

        self.bytes = [bits.byte1,
                      bits.byte2,
                      bits.byte3,
                      bits.byte4]
        return self.bytes


def list_to_uint32(data_list):
    """Apply Little Endian and convert the bytes to a single value"""
    dl = data_list
    return (dl[3]<<24)+(dl[2]<<16)+(dl[1]<<8)+(dl[0])

def list_to_uint16(data_list):
    """Apply Little Endian and convert the bytes to a single value"""
    dl = data_list
    return (dl[1]<<8)+(dl[0])

def u16_bytes(num):
    """Return the bytes of a uint16 in a list."""
    # Prepare a uint16 structure
    u16_temp = u16()
    u16_temp.asbyte = num
    
    # Get the bytes from 
    return u16_temp.bytes()

def join_7bits(ub, lb):
    """Join the bits of 2 7bit numbers"""
    return lb + (ub << 7)

def join_8bits(ub, lb):
    """Join the bits of 2 8bit numbers"""
    return lb + (ub << 8)

def odd_parity(num):
    """Return the odd parity of a number
    
    Example:
    0b1011, 3 bits are 1 
    """
    parity = 1
    while num:
        parity = 1-parity
        num = num & (num - 1)
    return parity

def add_odd_parity_1byte(num):
    """Return the number with odd parity added on bit 8"""
    return (odd_parity(num)<<7) + num

def limit_bits(num:int, num_bits:int)->int:
    """Limit the number of bits of a number.
    Example:
    num = 255 = 0b1111 1111
    num_bits = 7

    return: 0b01111 1111 = 127
    """
    return num & int('1'*num_bits,2)

def add_parity_2bytes(num):
    """Return the input number with odd parity on bits 7 and 15."""
    b = u16()
    b.asbyte = num
    ub, lb = b.bytes()
    ub_p = add_odd_parity_1byte(ub)
    lb_p = add_odd_parity_1byte(lb)

    b.bits.byte1 = ub_p
    b.bits.byte2 = lb_p
    return b.asbyte