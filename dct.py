'''
Implementation of the Discrete Cosine Transformation. The DCT is a transformation on periodic functions that singles out the major
frequencies composing the function.

The DCT is based on a variation of the Fourier Series:
        f: [0, P] -> R
        f(x) = sum n=0 to n=inf (C_n * cos(2pi * nx/P))

From this, it is simple to derive the equation for C_n, which represents how much weight should be assigned to a multiple of
the fundamental frequency.

However, this variation of the FS relies on a infinite amount of terms. In a finite set of points, the number of terms needed is:
        N=|finite set of points|

The function f can be written as the dot product of the coefficients and the cosine function. On a finite 
'''
import numpy as np

def dct(number_list):
    # Assume period is the size of the list
    P = len(number_list)
    
    # DCT-2 gives X_k = sum from n=0 to n=N-1 x_n * cos(n*k/N) (unsure why wikipedia uses (n+1/2) instead of n inside cosine)
    dct_matrix = np.array([[np.cos((i * (j + 1/2)*np.pi/P)) for j in range(P)] for i in range(P)])
    
    # Normalize the resulting matrix
    normalization_mat = np.vstack((
        np.array([[np.sqrt(1/P) for j in range(P)] for i in range(1)]),
        np.array([[np.sqrt(2/P) for j in range(P)] for i in range(1, P)])
    ))
    dct_matrix = dct_matrix * normalization_mat
    
    dct_coeffs = np.dot(dct_matrix, number_list) / P
    return dct_coeffs

def idct(coeff_list):
    # IDCT of DCT-2 is just the transpose of the DCT Matrix since the rows of the DCT Matrix are orthogonal

    P = len(coeff_list)
    dct_matrix = np.array([[np.cos((i * (j + 1/2)*np.pi/P)) for j in range(P)] for i in range(P)])
    normalization_mat = np.vstack((
        np.array([[np.sqrt(1/P) for j in range(P)] for i in range(1)]),
        np.array([[np.sqrt(2/P) for j in range(P)] for i in range(1, P)])
    ))
    dct_matrix = dct_matrix * normalization_mat
    idct_matrix = dct_matrix.T

    number_list = np.dot(idct_matrix, coeff_list) / P
    return number_list


if __name__ == '__main__':
    data_points = np.array([np.cos(np.pi * i/3) for i in range(4)])
    print("original data: ", data_points)
    coeff_list = dct(data_points)
    print("\ndct: ", coeff_list)
    reconstituted_data = idct(coeff_list)
    print("\nidct: ", reconstituted_data)
    
