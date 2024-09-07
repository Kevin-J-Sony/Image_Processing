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
            if self.data[1 + self.bit_idx // 8] != 0x00:
                self.bit_idx += 2 * 8
        elif self.data[self.bit_idx // 8] == 0x00:
            if self.data[-1 + self.bit_idx // 8] == 0xff:
                self.bit_idx += 1 * 8
        
        if self.is_done():
            raise Exception("Bitstream shouldn't end with 0xff00")
        
        bit_of_data = (self.data[self.bit_idx // 8] & self.bit_mask[(8 - 1) - (self.bit_idx % 8)])
        bit_of_data = bit_of_data >> (8 - 1 - (self.bit_idx % 8))
        self.bit_idx += 1
        
        return bit_of_data
    
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
    print(bit_str)