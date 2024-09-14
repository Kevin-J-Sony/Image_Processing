'''
Construct a stream that feeds in data bitwise with the get method
'''
import struct

class BitStream:
    
    
    def __init__(self, data):
        self.data = data
        self.bit_idx = 0
        self.bit_mask = [2**i for i in range(8)]
        
    def get(self):
        if self.data[self.bit_idx // 8] == 0xff:
            # if what follows 0xff is not 0x00, it is most likely a restart marker
            if self.data[1 + self.bit_idx // 8] != 0x00:
                self.bit_idx += 2 * 8
        elif self.data[self.bit_idx // 8] == 0x00:
            # if what follows 0xff is 0x00, it means that 0xff should be counted and 0x00 should be skipped.
            if self.data[-1 + self.bit_idx // 8] == 0xff:
                self.bit_idx += 1 * 8
        
        if self.is_done():
            raise Exception("Bitstream shouldn't end with 0xff00")
        
        bit_of_data = (self.data[self.bit_idx // 8] & self.bit_mask[(8 - 1) - (self.bit_idx % 8)])
        bit_of_data = bit_of_data >> (8 - 1 - (self.bit_idx % 8))
        self.bit_idx += 1
        
        return bit_of_data
    
    
    '''
    This is a modified version of two's complement. As 
    '''
    def get_value_from_bits(self, bitlength):
        value = 0
        for i in range(bitlength):
            print(value)
            value = value << 1 + self.get()
        
        # If the value is less than half of 2^bitlength, then the number it represents is negative. To get this
        # # number to be negative, subtract value by the medium number representable with "bitlength" bits, 2^(bitlength - 1)
        if value < (1 << (bitlength - 1)):
            value -= 1 << (bitlength - 1)
        
        return value
    
    def is_done(self):
        return self.bit_idx // 8 == len(self.data)
    
if __name__ == "__main__":
    x = 255 * 256
    bit = BitStream(x.to_bytes(2, 'big'))
    print(x.to_bytes(2, 'big'))
    
    bit_str = ""
    while not bit.is_done():
        try:
            bit_str += str(bit.get())
        except Exception:
            ...
    print(bit_str, '\n')
    
    bit = BitStream("Aa".encode("ascii"))
    print(bytes("Aa".encode("ascii")))
    
    bit_str = ""
    while not bit.is_done():
        try:
            bit_str += str(bit.get())
        except Exception:
            ...
    print(bit_str, '\n')
    
    x = 0
    bit = BitStream(x.to_bytes(2, "big"))
    print(bit.get_twos_complement(3))
    