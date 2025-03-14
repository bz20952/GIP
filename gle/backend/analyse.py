import reader as r
import utils as u
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import rfft,rfftfreq
import numpy as np

"""
This module contains functions to analyse the data from the input file."""

def get_natural_freqs(data: pd.DataFrame, options: dict) -> None:

    #Extract data
    t = data['Time'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

    #extract force
    force = data['Force_1'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['Accel_1'].to_numpy()
    response_1 = data['Accel_2'].to_numpy()
    response_2 = data['Accel_3'].to_numpy()
    response_3 = data['Accel_4'].to_numpy()
    response_4 = data['Accel_5'].to_numpy()

    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force)
    F_resp_0 = rfft(response_0)
    F_resp_1 = rfft(response_1)
    F_resp_2 = rfft(response_2)
    F_resp_3 = rfft(response_3)
    F_resp_4 = rfft(response_4)
    
    # Frequency vector
    freqs = rfftfreq(N, 1/Fs)

    # Compute FRF for each measurement point
    FRF_0 = np.abs(F_resp_0 / F_force)
    FRF_1 = np.abs(F_resp_1 / F_force)
    FRF_2 = np.abs(F_resp_2 / F_force)
    FRF_3 = np.abs(F_resp_3 / F_force)
    FRF_4 = np.abs(F_resp_4 / F_force)

    plt.plot(freqs, FRF_1)
    plt.title('Frequency Response Function')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()

    # Find peaks in FRF to get natural frequencies, choose which measurement location to use
    # Can also use FFT to get natural frequencies
    peaks, _ = find_peaks(FRF_1, height=45)  # For Trial Merged Random F1 10sec1, 45 height is acceptable
    natural_frequencies = freqs[peaks]
    #print(type(natural_frequencies))
    
    return print("The first three natural frequencies are ", natural_frequencies[:3], "Hz")



def get_mode_shapes(data= pd.DataFrame, options= dict)-> None:
    
    #Extract data
    t = data['Time'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

    #extract force
    force = data['Force_1'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['Accel_1'].to_numpy()
    response_1 = data['Accel_2'].to_numpy()
    response_2 = data['Accel_3'].to_numpy()
    response_3 = data['Accel_4'].to_numpy()
    response_4 = data['Accel_5'].to_numpy()

    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force)
    F_resp_0 = rfft(response_0)
    F_resp_1 = rfft(response_1)
    F_resp_2 = rfft(response_2)
    F_resp_3 = rfft(response_3)
    F_resp_4 = rfft(response_4)
    
    # Frequency vector
    freqs = np.fft.rfftfreq(N, 1/Fs)

    FRF_0 = np.abs(F_resp_0 / F_force)
    FRF_1 = np.abs(F_resp_1 / F_force)
    FRF_2 = np.abs(F_resp_2 / F_force)
    FRF_3 = np.abs(F_resp_3 / F_force)
    FRF_4 = np.abs(F_resp_4 / F_force)

    # Find peaks in FRF to get natural frequencies, choose which measurement location to use
    peaks, _ = find_peaks(FRF_1, height=45)  # Adjust threshold as needed
    natural_frequencies = freqs[peaks]
    #print(natural_frequencies)

    # Calculating the peak of imaginary value of FRF, based on literature this is the easiest way to find mode shape experimentally
    imgFRF_0 = np.imag(F_resp_0 / F_force)
    imgFRF_1 = np.imag(F_resp_1 / F_force)
    imgFRF_2 = np.imag(F_resp_2 / F_force)
    imgFRF_3 = np.imag(F_resp_3 / F_force)
    imgFRF_4 = np.imag(F_resp_4 / F_force)

    # Array of imaginary gain at idenfitied natural frequencies
    # Assuming we want to identify only the first three mode shapes
    ms_1 = [imgFRF_0[peaks[0]],imgFRF_1[peaks[0]],imgFRF_2[peaks[0]],imgFRF_3[peaks[0]],imgFRF_4[peaks[0]]]
    ms_2 = [imgFRF_0[peaks[1]],imgFRF_1[peaks[1]],imgFRF_2[peaks[1]],imgFRF_3[peaks[1]],imgFRF_4[peaks[1]]]
    ms_3 = [imgFRF_0[peaks[2]],imgFRF_1[peaks[2]],imgFRF_2[peaks[2]],imgFRF_3[peaks[2]],imgFRF_4[peaks[2]]]

    #Note: For random generated data, sometimes there is less than 3 detected 'peaks', which will produce error

    #plt.plot(freqs, imgFRF_0, color='black')
    #plt.plot(freqs, imgFRF_1, color='red')
    plt.plot(freqs, imgFRF_2, color='blue')
    plt.plot(freqs, imgFRF_3, color='green')
    #plt.plot(freqs, imgFRF_4, color='orange')
    plt.title('Frequency Response Function')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.show()

    #Normalizing the mode shapes, accounting for direction. Highest absolute magnitude is set to 1 and other values are scaled accordingly
    modeshape1 = ms_1/max(ms_1, key= abs)
    modeshape2 = ms_2/max(ms_2, key= abs)
    modeshape3 = ms_3/max(ms_3, key= abs)

    mode_shapes = [modeshape1, modeshape2, modeshape3]

    return print("Mode shape 1 is ", modeshape1, ". Mode shape 2 is ", modeshape2, ". Mode shape 3 is ", modeshape3)

data = pd.read_csv(r"gle\backend\data\Trial_Merged_Random_F1_10sec1.csv")
get_natural_freqs(data, {})
get_mode_shapes(data, {})