def list_to_uint32(list_bytes):
    """
    Returns a 32bit uint value equivalent of 4 8bit values
    """
    lb = list_bytes
    
    return (lb[3]<<24)+(lb[2]<<16)+(lb[1]<<8)+(lb[0])


def uint32_to_list(uint32):
    """
    Returns a 4 element list containing 8 bits each representing the input uint_32
    """
    return [uint32>>24 & 0xFF, uint32>>16 & 0xFF, uint32>>8 & 0xFF, uint32 & 0xFF]


def uint32_to_list_reversed(uint32):
    """
    Returns a reversed 4 element list containing 8 bits each
    representing the input uint_32
    """
    lb = uint32_to_list(uint32)
    lb_rev = [lb[3], lb[2], lb[1], lb[0]]
    
    return lb_rev


def list_to_bytes(lst):
    pass


def milliamp_to_10mA(current_milliamp):
    return int( current_milliamp / 10 )


def amp_to_10mA(current_amp):
    return round(current_amp * 100)


def trim_to_spec(param, resolution):
    count = param // resolution
    param = count * resolution