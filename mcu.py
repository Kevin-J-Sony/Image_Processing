'''
Basic dataclass which contains the minimum coded unit containing the color channels for a given block
'''
from dataclasses import dataclass
import numpy as np

@dataclass
class MCU:
    Y: np.ndarray = np.zeros((8, 8))
    Cr: np.ndarray = np.zeros((8, 8))
    Cb: np.ndarray = np.zeros((8, 8))
    R: np.ndarray = np.zeros((8, 8))
    G: np.ndarray = np.zeros((8, 8))
    B: np.ndarray = np.zeros((8, 8))
