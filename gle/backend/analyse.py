import reader as r
import utils as u
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import rfft,rfftfreq
import numpy as np

"""
This module contains functions to analyse the data from the input file."""


async def get_natural_freqs(data: pd.DataFrame, options: dict) -> None:
    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']

    freqs = []
    frf = []
    frf_abs = []

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
            frf_a = fftacc / fftforce  # Frequency Response Function
            frf_magnitude = np.abs(frf_a)

            freqs.append(f)
            frf.append(frf_a)
            frf_abs.append(frf_magnitude)

    freqs = np.array(freqs)
    frf = np.array(frf)
    frf_abs = np.array(frf_abs)

    #parameter for find peak
    prominence = 3
    distance = 200

    if frf_abs.ndim == 1:
        peaks, _ = find_peaks(frf_abs, prominence=prominence, distance=distance)  # Use the array directly if it's 1D
    else:
        peaks, _ = find_peaks(frf_abs[0], prominence=prominence, distance=distance)  # Access the first row if it's 2D

    if len(np.shape(freqs)) == 1:
        natural_frequencies = freqs[peaks]
    else:
        natural_frequencies = freqs[0][peaks]

    print("Natural Frequencies: ", natural_frequencies)
    
    #Method to cross-check the value of the natural frequencies
    ## TO BE REMOVED AFTER TESTING ##

    if len(np.shape(frf_abs)) == 1:
        # If frf_abs is 1D, plot it directly
        plt.plot(freqs, frf_abs)
    else:
        # If frf_abs is 2D, plot the first row
        plt.plot(freqs[0], frf_abs[0])

    plt.title('Frequency Response Function')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()
    
    return natural_frequencies

async def get_mode_shapes(data: pd.DataFrame, options: dict) -> None:
    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']

    freqs = []
    i_frf = []
    frf_abs = []

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
            frf_a = fftacc / fftforce  # Frequency Response Function

            # Convert inertance to receptance
            omega = 2 * np.pi * f  # Convert frequency to angular frequency (rad/s)
            omega[np.abs(omega) < 1e-10] = np.finfo(float).eps
            frf_receptance = frf_a / (-omega**2)  # Convert inertance to receptance

            frf_magnitude = np.abs(frf_a)
            frf_img = np.imag(frf_receptance)

            freqs.append(f)
            i_frf.append(frf_img)
            frf_abs.append(frf_magnitude)

    freqs = np.array(freqs)
    i_frf = np.array(i_frf)
    frf_abs = np.array(frf_abs)

    #parameter for find peak
    prominence = 3
    distance = 200

    if frf_abs.ndim == 1:
        peaks, _ = find_peaks(frf_abs, prominence=prominence, distance=distance)  # Use the array directly if it's 1D
    else:
        peaks, _ = find_peaks(frf_abs[0], prominence=prominence, distance=distance)  # Access the first row if it's 2D

    
    #START PRODUCING MODESHAPE LIST
    ms = []  # List to store modeshapes

    for i in range(len(peaks)):  # Loop through all peaks
        # Handle both 1D and 2D cases for i_frf
        if i_frf.ndim == 1:
            # If i_frf is 1D, directly use peaks[i] as the index
            ms_i = np.array([i_frf[peaks[i]]])
        else:
            # If i_frf is 2D, extract the value at peaks[i] for each row
            ms_i = np.array([i_frf[row, peaks[i]] for row in range(i_frf.shape[0])])
    
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

if __name__ == '__main__':
    import json
    import asyncio
    import reader as r
    with open('./templates/requestFormat.json') as f:
        options = json.load(f)
    data = r.read_csv(options)
    asyncio.run(get_natural_freqs(data, options))
    asyncio.run(get_mode_shapes(data, options))