'''
This is a JPEG decoder, or specifically, a JFIF decoder, as JPEG is a standard, and JFIF is a file format implementing
the standard. The documentation for the JFIF format used in this program is from https://www.w3.org/Graphics/JPEG/itu-t81.pdf,
and considerable help came from the JPEG article on wikipedia.
'''
import struct
import numpy as np
from dct import *

class JPG_IMAGE_DECODER:
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.read_jpeg()
        self.idx = 0
    
    def read_SOF_segment(self):
        idx = 0
        while not (self.jpeg_file[idx] == 0xff and self.jpeg_file[idx + 1] == 0xc0): # 255 is 0xff and 192 is 0xc0
            idx = idx + 1
        print(hex(self.jpeg_file[idx]), ' ', hex(self.jpeg_file[idx + 1]))
        idx = idx + 2
        
        length_of_segment = self.jpeg_file[idx] * 256 + self.jpeg_file[idx + 1] 
        print(str(self.jpeg_file[idx]), ' ', str(self.jpeg_file[idx + 1]))
        idx = idx + 2
        precision = self.jpeg_file[idx]
        print(str(self.jpeg_file[idx]))
        idx = idx + 1
        height = self.jpeg_file[idx] * 256 + self.jpeg_file[idx + 1] 
        print(str(self.jpeg_file[idx]), ' ', str(self.jpeg_file[idx + 1]))

        idx = idx + 2
        width = self.jpeg_file[idx] * 256 + self.jpeg_file[idx + 1] 
        print(str(self.jpeg_file[idx]), ' ', str(self.jpeg_file[idx + 1]))

        print('length_of_segment:   ', length_of_segment)
        print('precision:   ', precision)
        print('height:   ', height)
        print('width:   ', width)
        
        idx = idx - 5
        # python stores in big endain format
        l, p, h, w = struct.unpack(">HBHH", self.jpeg_file[idx: idx+7])
        print("{}\t{}\t{}\t{}".format(l, p, h, w))
        print(str(self.jpeg_file[idx: idx+7]))


    def read_huffman_table(self):
        ...
                
    def dequantization(block):
        quant_block = np.array([[]])
        ...

    def read_quantization_table(self):
        idx = 0
        while not (self.jpeg_file[idx] == 0xff and self.jpeg_file[idx + 1] == 0xdb): # 255 is 0xff and 192 is 0xc0
            idx = idx + 1
        print(idx)
        print(hex(self.jpeg_file[idx]), ' ', hex(self.jpeg_file[idx + 1]))    
        
        # read until Oxff 0xdb
        while not (self.jpeg_file[idx] == 0xff and self.jpeg_file[idx + 1] == 0xdb):
            ...
        
        # read until Oxff 0xdb
        while not (self.jpeg_file[idx] == 0xff and self.jpeg_file[idx + 1] == 0xdb): 
            ...
            
        
        # read until Oxff 0xc4
        while not (self.jpeg_file[idx] == 0xff and self.jpeg_file[idx + 1] == 0xdb): 
            ...        
        
    def read_jpeg(self):
        with open(self.file_name, 'rb') as jpg_image:
            self.jpeg_file = jpg_image.read()
        



def main():
    bytestr = JPG_IMAGE_DECODER('jpeg444.jpg')
    
    # Confirm this is a jpeg file
    if bytestr.jpeg_file[0] == 0xff and bytestr.jpeg_file[1] == 0xd8:
        print("Is a jpeg file")
    
    
    bytestr.read_SOF_segment()
    # read_quant_table(bytestr)

main()