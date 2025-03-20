import reader as r
import utils as u
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import rfft,rfftfreq
import numpy as np

"""
This module contains functions to analyse the data from the input file."""


def get_FRF(data: pd.DataFrame, options: dict) -> None:
        #Extract data
    for acc in accelerometers.keys():
        if accelerometers[acc]:
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            sample_rate = 1 / (data['t'][1] - data['t'][0])
            f = np.fft.fftfreq(n, 1/sample_rate)[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc[1]])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function

     # Frequency vector
    freqs = f

    return freqs, fftacc, frf 

freqs, fftacc, frf = get_FRF(data, {})

def get_natural_freqs(freqs, frf) -> None:

    # Find peaks in FRF to get natural frequencies, choose which measurement location to use
    peaks, _ = find_peaks(np.abs(frf[0]), prominence=3, distance=200)
    natural_frequencies = freqs[peaks]

    #Method to cross-check the value of the natural frequencies
    ## TO BE REMOVED AFTER TESTING ##
    plt.plot(freqs, np.abs(frf[0]))
    plt.title('Frequency Response Function')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()
    
    return natural_frequencies

def get_mode_shapes(freqs, frf)-> None:
    # Convert inertance to receptance
    omega = 2 * np.pi * freqs  # Convert frequency to angular frequency (rad/s)
    frf_r = frf / (-omega**2)  # Convert inertance to receptance
    
    # Avoid division by zero at zero frequency
    frf_r[omega == 0] = np.inf

    abs_frf = np.abs(frf_r)

    i_frf_r0 = np.imag(frf_r[0])
    i_frf_r1 = np.imag(frf_r[1])
    i_frf_r2 = np.imag(frf_r[2])

    ### ARGAND DIAGRAM###
    # Find peaks in FRF to get natural frequencies, choose which measurement location to use
    peaks, _ = find_peaks(abs_frf[0], prominence=3, distance=200)  # Adjust threshold as needed

    #START PRODUCING MODESHAPE LIST
    ms = []  # Initialize an empty list to store ms_i arrays

    for i in range(len(peaks)):  # Loop through all peaks
        ms_i = np.array([i_frf_r0[peaks[i]], i_frf_r1[peaks[i]], i_frf_r2[peaks[i]]])
    
        # Normalize by dividing by the maximum absolute value in ms_i
        max_abs_value = np.max(np.abs(ms_i)) if np.any(ms_i) else 1  # Avoid division by zero
        ms_i = ms_i / max_abs_value
    
        ms.append(ms_i)
    
    # Convert list of arrays into a single NumPy array for easier processing
    modeshape = np.array(ms)

    # Print results
    for idx, m in enumerate(modeshape, start=1):
        print(f"ms_{idx}", m)

    return modeshape
