'''
Basic dataclass which contains the minimum coded unit containing the color channels for a given block. 
'''
from dataclasses import dataclass, field
import numpy as np

@dataclass
class MCU:
    Y: np.ndarray = field(default_factory=lambda: np.zeros((8, 8)))
    Cr: np.ndarray = field(default_factory=lambda: np.zeros((8, 8)))
    Cb: np.ndarray = field(default_factory=lambda: np.zeros((8, 8)))
    R: np.ndarray = field(default_factory=lambda: np.zeros((8, 8)))
    G: np.ndarray = field(default_factory=lambda: np.zeros((8, 8)))
    B: np.ndarray = field(default_factory=lambda: np.zeros((8, 8)))
    
    jpeg_color: list[np.ndarray] = field(default_factory=lambda: [np.zeros((8, 8)) for i in range(3)])
