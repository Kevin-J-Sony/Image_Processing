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
        if self.is_done():
            print("Second last value of bitstream {}".format(hex(self.data[self.bit_idx // 8 - 2])))
            print("Last value of bitstream {}".format(hex(self.data[self.bit_idx // 8 - 1])))
            raise Exception("Last value of bitstream {}".format(self.data[self.bit_idx // 8 - 1]))
        
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
    This is a modified version of two's complement. In reading DC/AC coefficients, we first get the category n, then we get
    n number of bits. The values the bit represents does not fully span -2^n to 2^n, since that would require n+1 bits; however,
    given that we know that there is a certain amount of bits to be read, we can exclude half of the "inner" values just from
    our assumption: thus the values span -2^n to -2^(n-1) and 2^(n-1) to 2^n.
    
    For example, with a category of 3, the range of values encoded is -7, -6, -5, -4, 4, 5, 6, 7. 2^3=8 values are encoded, but
    there is a jump from -2^(3-1)=-4 to 2^(3-1)=4. 
    
    It might seem crazy that n bits are able to "effectively" encode 2^(n+1) values (if excluding the elements still
    counts as information encoding), but notice that the first argument acts like an extra "bit".
    '''
    def get_value_from_bits(self, bitlength):
        if bitlength == 0:
            return 0
        value = 0
        t_str = ""
        for i in range(bitlength):
            t = self.get()
            value = (value << 1) | t
            t_str += str(t)
        '''
        If the first bit is 0, then the value the n bits represents is negative. Since "value" is currently a positive number,
        subtract it by -2^n + 1 to shift the "value" in such a way that 0 maps to -2^n + 1. 
        '''
        if value < (1 << (bitlength - 1)):
            value -= (1 << bitlength) - 1
        #print(bitlength, '\t', value, '\t', t_str)
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
    print(bit.get_value_from_bits(2))
    