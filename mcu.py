'''
Basic dataclass which contains the minimum coded unit containing the color channels for a given block. 
'''
from dataclasses import dataclass, field
import numpy as np

@dataclass
class MCU:
    jpeg_color: list[np.ndarray] = field(default_factory=lambda: [np.zeros((8, 8)) for i in range(3)])
    rgb: list[np.ndarray] = field(default_factory=lambda: [np.zeros((8, 8)) for i in range(3)])