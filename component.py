'''
Basic dataclass which contains the Huffman Table ID, Quantization Table ID, vertical sampling factor, and horizontal
sampling factor for each component. 
'''
from dataclasses import dataclass

@dataclass
class Component:
    ht_dc_id: int = -1
    ht_ac_id: int = -1
    qt_id: int = -1
    horizontal_sampling: int = 1
    vertical_sampling: int = 1

