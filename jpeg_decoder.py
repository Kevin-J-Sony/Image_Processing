'''
This is a JPEG decoder. The documentation for the JPEG format used in this program is from https://www.w3.org/Graphics/JPEG/itu-t81.pdf,
and considerable help came from the JPEG article on wikipedia. 

This decoder only implements sequential JPEG
'''
import struct
import numpy as np
from dct import *
from huffman import *

class JPG_IMAGE_DECODER:
    
    zig_zag = np.array([0, 
                        1, 8, 
                        16, 9, 2, 
                        3, 10, 17, 24, 
                        32, 25, 18, 11, 4, 
                        5, 12, 19, 26, 33, 40, 
                        48, 41, 34, 27, 20, 13, 6, 
                        7, 14, 21, 28, 35, 42, 49, 56, 
                        57, 50, 43, 36, 29, 22, 15, 
                        23, 30, 37, 44, 51, 58, 
                        59, 52, 45, 38, 31, 
                        39, 46, 53, 60, 
                        61, 54, 47, 
                        55, 62, 
                        63])
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.idx = 0
        self.eof = False
        self.quant_tables = {}
        self.huff_tables = {}
        self.component_to_qt_id = {}
        self.read_jpeg()
        self.decode_jpeg()

    def read_jpeg(self):
        with open(self.file_name, 'rb') as jpg_image:
            # store the entire file into a binary 
            self.jpeg_file = jpg_image.read()

    def decode_jpeg(self):
        if not (self.jpeg_file[self.idx] == 0xff and self.jpeg_file[self.idx + 1] == 0xd8):
            raise Exception("Invalid JPG file: The SOI markers are not given")
        self.idx += 2
        
        while self.idx < len(self.jpeg_file) - 1 and not self.eof:
            # If EOI marker reached, the jpeg file has been fully read
            if self.jpeg_file[self.idx] == 0xff and self.jpeg_file[self.idx + 1] == 0xd9:
                self.eof = True
                self.idx += 2
                continue
            
            # If DQT marker reached,
            if self.jpeg_file[self.idx] == 0xff and self.jpeg_file[self.idx + 1] == 0xdb:
                self.idx += 2
                self.read_quantization_table()
                continue

            # If SOF marker reached,
            if self.jpeg_file[self.idx] == 0xff and self.jpeg_file[self.idx + 1] == 0xc0:
                self.idx += 2
                self.read_SOF_segment()
                continue
                ...

            # If DHT marker reached,
            if self.jpeg_file[self.idx] == 0xff and self.jpeg_file[self.idx + 1] == 0xc4:
                self.idx += 2
                self.read_huffman_table()
                continue
                
            # If SOS marker reached,
            if self.jpeg_file[self.idx] == 0xff and self.jpeg_file[self.idx + 1] == 0xda:
                ...
            
            
            # Some markers are ignored, such as 0xFFE0 and 0xFFE1 for JFIF and EXIF. This is
            # because JPEG does not actually require it, and specialized decoders are necessary
            # for those formats. A general decoder does not really need it.
            self.idx += 1
            ...
            
        if not self.eof:
            raise Exception("Invalid JPG file: the EOI markers are not given")
        ...
    
    def read_SOF_segment(self):
        length, precision, height, width, number_of_components = struct.unpack(">HBHHB", self.jpeg_file[self.idx : self.idx+8])
        '''
        print("length: ", length)
        print("precision: ", precision)
        print("height: ", height)
        print("width: ", width)
        print("number: ", number_of_components)
        print("===================")
        '''
        self.idx += 8
        
        for i in range(number_of_components):
            component, coded_sampling_factor, qt_id = struct.unpack(">BBB", self.jpeg_file[self.idx : self.idx+3])
            horizontal_sampling = (coded_sampling_factor & 0xf0) >> 4
            vertical_sampling = coded_sampling_factor & 0x0f
            
            #if not (horizontal_sampling == 1 and vertical_sampling == 1):
            #    raise Exception("Subsampling is not supported right now")
            
            self.component_to_qt_id[component] = qt_id
            '''
            print("component: ", component)
            print("horizontal sampling factor", horizontal_sampling)
            print("vertical sampling factor", vertical_sampling)
            print("Quantization table ID: ", qt_id)

            print("===================")
            '''
            self.idx += 3


    def read_huffman_table(self):
        huff_length = struct.unpack(">H", self.jpeg_file[self.idx : self.idx+2])[0]
        huff_length -= 2
        self.idx += 2
                
        while huff_length > 0:
            table_info = struct.unpack(">B", self.jpeg_file[self.idx : self.idx+1])[0]
            ht_type = (table_info & 0xf0) >> 4
            ht_id = table_info & 0x0f
            
            huff_length -= 1
            self.idx += 1
            
            number_of_symbols_per_length = []
            number_of_symbols = 0
            # Get the number of symbols per bit length
            for length_idx in range(16):
                number_of_symbols_per_length.append(struct.unpack(">B", self.jpeg_file[self.idx : self.idx+1])[0])
                number_of_symbols += number_of_symbols_per_length[-1]
                huff_length -= 1
                self.idx += 1
            
            symbols = np.zeros(number_of_symbols)
            # Read all the symbol
            for i in range(number_of_symbols):
                symbols[i] = struct.unpack(">B", self.jpeg_file[self.idx : self.idx+1])[0]
                self.idx += 1
                huff_length -= 1                
                ...
            
            self.huff_tables[(ht_type, ht_id)] = Huffman(number_of_symbols_per_length, symbols)
            
        '''
        for key, value in self.huff_tables.items():
            print(f"{key} : {value}")
            ...
        #'''

    def read_quantization_table(self):
        quant_length = struct.unpack(">H", self.jpeg_file[self.idx : self.idx+2])[0]
        #quant_str = str(self.jpeg_file[self.idx : self.idx + quant_length].hex())
        #new_quant_str = ' '.join(quant_str[i: i+4] for i in range(0, len(quant_str), 4))
        #print(new_quant_str)

        quant_length -= 2
        self.idx += 2
        
        #print("length: ", quant_length)
        
        while quant_length > 0:
            table_info = struct.unpack(">B", self.jpeg_file[self.idx : self.idx+1])[0]
            precision = table_info & 0xf0
            destination = table_info & 0x0f
            quant_length -= 1
            self.idx += 1
            
            #print("table_info: ", bytes(table_info))
            #print("precision: ", precision)
            print("destination: ", destination)
            
            quant_table = np.zeros(64)
            
            for qt_idx in range(64):
                if precision == 0:
                    quant_table[JPG_IMAGE_DECODER.zig_zag[qt_idx]] = struct.unpack(">B", self.jpeg_file[self.idx : self.idx+1])[0]
                    self.idx += 1
                    quant_length -= 1
                    ...
                elif precision == 1: # Only ever using baseline DCT
                    quant_table[JPG_IMAGE_DECODER.zig_zag[qt_idx]] = struct.unpack(">H", self.jpeg_file[self.idx : self.idx+2])[0]
                    self.idx += 2
                    quant_length -= 2
                    ...
            quant_table = quant_table.reshape((8, 8))
            self.quant_tables[destination] = quant_table
            # print(quant_table)


def main():
    bytestr = JPG_IMAGE_DECODER('Lenna.jpg')
    
    # Confirm this is a jpeg file
    if bytestr.jpeg_file[0] == 0xff and bytestr.jpeg_file[1] == 0xd8:
        print("Is a jpeg file")
    
    # read_quant_table(bytestr)

main()