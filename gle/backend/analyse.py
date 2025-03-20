import reader as r
import utils as u
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import rfft,rfftfreq
import numpy as np

"""
This module contains functions to analyse the data from the input file."""



def get_dft(data: pd.DataFrame, options: dict) -> None:

    #extract force
    force_0 = data['F0'].to_numpy()
    force_1 = data['F1'].to_numpy()
    force_2 = data['F2'].to_numpy()
    force_3 = data['F3'].to_numpy()
    force_4 = data['F4'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['A0'].to_numpy()
    response_1 = data['A1'].to_numpy()
    response_2 = data['A2'].to_numpy()
    response_3 = data['A3'].to_numpy()
    response_4 = data['A4'].to_numpy()


    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force_0)
    F_force_1 = rfft(force_1)
    F_force_2 = rfft(force_2)
    F_force_3 = rfft(force_3)
    F_force_4 = rfft(force_4)

    F_resp_0 = rfft(response_0)
    F_resp_1 = rfft(response_1)
    F_resp_2 = rfft(response_2)
    F_resp_3 = rfft(response_3)
    F_resp_4 = rfft(response_4)

    return F_force, F_resp_0, F_resp_1, F_resp_2, F_resp_3, F_resp_4

def get_FRF(data: pd.DataFrame, options: dict) -> None:
        #Extract data
    t = data['t'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

     # Frequency vector
    freqs = rfftfreq(N, 1/Fs)

    # Compute FRF for each measurement point
    FRF_0 = np.abs(F_resp_0 / F_force)
    FRF_1 = np.abs(F_resp_1 / F_force)
    FRF_2 = np.abs(F_resp_2 / F_force)
    FRF_3 = np.abs(F_resp_3 / F_force)
    FRF_4 = np.abs(F_resp_4 / F_force)

    return freqs, FRF_0, FRF_1, FRF_2, FRF_3, FRF_4

def plot_FRF_gain(data: pd.DataFrame, options: dict) -> None:
     #Extract data
    t = data['t'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

    #extract force
    force_0 = data['F0'].to_numpy()
    force_1 = data['F1'].to_numpy()
    force_2 = data['F2'].to_numpy()
    force_3 = data['F3'].to_numpy()
    force_4 = data['F4'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['A0'].to_numpy()
    response_1 = data['A1'].to_numpy()
    response_2 = data['A2'].to_numpy()
    response_3 = data['A3'].to_numpy()
    response_4 = data['A4'].to_numpy()


    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force_0)

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

def inertance_to_receptance(frequency, inertance_FRF):
    omega = 2 * np.pi * frequency  # Convert frequency to angular frequency (rad/s)
    receptance = inertance_FRF / (-omega**2)  # Convert inertance to receptance
    
    # Avoid division by zero at zero frequency
    receptance[omega == 0] = np.inf

      #Conversion to receptance
    rF_resp_0 = inertance_to_receptance(frequency, FRF_0)
    rF_resp_1 = inertance_to_receptance(frequency, FRF_1)
    rF_resp_2 = inertance_to_receptance(frequency, FRF_2)
    rF_resp_3 = inertance_to_receptance(frequency, FRF_3)
    rF_resp_4 = inertance_to_receptance(frequency, FRF_4)

    # Calculating the peak of imaginary value of receptance FRF, based on literature this is the easiest way to find mode shape experimentally
    imgFRF_0 = np.imag(rF_resp_0 / F_force)
    imgFRF_1 = np.imag(rF_resp_1 / F_force)
    imgFRF_2 = np.imag(rF_resp_2 / F_force)
    imgFRF_3 = np.imag(rF_resp_3 / F_force)
    imgFRF_4 = np.imag(rF_resp_4 / F_force)

    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(6, 9), sharex=True)

    # Plot data
    ax[0].plot(freqs, imgFRF_0, color='r')
    ax[0].set_title("Imaginary FRF - Accelerometer 1")
    ax[0].set_xlabel("Frequency (Hz)")
    ax[0].set_ylabel("Response")

    ax[1].plot(freqs, imgFRF_2, color='g')
    ax[1].set_title("Imaginary FRF - Accelerometer 2")
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_ylabel("Response")

    ax[2].plot(freqs, imgFRF_4, color='b')
    ax[2].set_title("Imaginary FRF - Accelerometer 3")
    ax[2].set_xlabel("Frequency (Hz)")
    ax[2].set_ylabel("Response")

    plt.show()
    
    return receptance

def plot_imaginary(data: pd.DataFrame, options: dict) -> None:
        
   #Extract data
    t = data['t'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

    #extract force
    force_0 = data['F0'].to_numpy()
    force_1 = data['F1'].to_numpy()
    force_2 = data['F2'].to_numpy()
    force_3 = data['F3'].to_numpy()
    force_4 = data['F4'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['A0'].to_numpy()
    response_1 = data['A1'].to_numpy()
    response_2 = data['A2'].to_numpy()
    response_3 = data['A3'].to_numpy()
    response_4 = data['A4'].to_numpy()


    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force_0)

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

    ## Remove this if argand plot plan is abandoned
    FRF_0 = (F_resp_0 / F_force)
    FRF_1 = (F_resp_1 / F_force)
    FRF_2 = (F_resp_2 / F_force)
    FRF_3 = (F_resp_3 / F_force)
    FRF_4 = (F_resp_4 / F_force)

    #Use this if sticking with imaginary inertance. Scale of imaginary receptance is too low
    # Calculating the peak of imaginary value of FRF, based on literature this is the easiest way to find mode shape experimentally
    imgFRF_0 = np.imag(F_resp_0 / F_force)
    imgFRF_1 = np.imag(F_resp_1 / F_force)
    imgFRF_2 = np.imag(F_resp_2 / F_force)
    imgFRF_3 = np.imag(F_resp_3 / F_force)
    imgFRF_4 = np.imag(F_resp_4 / F_force)


    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(6, 9), sharex=True)

    # Plot data
    ax[0].plot(freqs, imgFRF_0, color='r')
    ax[0].set_title("Imaginary FRF - Accelerometer 1")
    ax[0].set_xlabel("Frequency (Hz)")
    ax[0].set_ylabel("Response")

    ax[1].plot(freqs, imgFRF_2, color='g')
    ax[1].set_title("Imaginary FRF - Accelerometer 2")
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_ylabel("Response")

    ax[2].plot(freqs, imgFRF_4, color='b')
    ax[2].set_title("Imaginary FRF - Accelerometer 3")
    ax[2].set_xlabel("Frequency (Hz)")
    ax[2].set_ylabel("Response")

    fig.tight_layout()
    plt.show()

    return

def plot_argand(data: pd.DataFrame, options: dict) -> None:
    #Extract data
    t = data['t'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

    #extract force
    force_0 = data['F0'].to_numpy()
    force_1 = data['F1'].to_numpy()
    force_2 = data['F2'].to_numpy()
    force_3 = data['F3'].to_numpy()
    force_4 = data['F4'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['A0'].to_numpy()
    response_1 = data['A1'].to_numpy()
    response_2 = data['A2'].to_numpy()
    response_3 = data['A3'].to_numpy()
    response_4 = data['A4'].to_numpy()


    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force_0)

    F_resp_0 = rfft(response_0)
    F_resp_1 = rfft(response_1)
    F_resp_2 = rfft(response_2)
    F_resp_3 = rfft(response_3)
    F_resp_4 = rfft(response_4)
    
    # Frequency vector
    freqs = np.fft.rfftfreq(N, 1/Fs)

    ## Remove this if argand plot plan is abandoned
    cFRF_0 = (F_resp_0 / F_force)
    cFRF_1 = (F_resp_1 / F_force)
    cFRF_2 = (F_resp_2 / F_force)
    cFRF_3 = (F_resp_3 / F_force)
    cFRF_4 = (F_resp_4 / F_force)
    
    peaks, _ = find_peaks(FRF_1, prominence=3, distance=200)  # Adjust threshold as needed

    arg = []

    for i in range(len(peaks)):  # Loop through all peaks
        arg_i = np.array([cFRF_0[peaks[i]], cFRF_2[peaks[i]], cFRF_4[peaks[i]]])
        arg.append(arg_i)

    # Convert list of arrays into a single NumPy array for easier processing
    arg = np.array(arg)

    fig, ax = plt.subplots()
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Argand Diagram')
    
    arg_peaks = arg
    colors = ['r', 'g', 'b']  # Default colors if none provided
    
    for i, point in enumerate(arg_peaks):
        color = colors[i % len(colors)]  # Cycle through colors if needed
        plt.scatter(point.real, point.imag, color=color, s=50, label=f'Accelerometer {i*2}')
        plt.plot([0, point.real], [0, point.imag], color=color, linestyle='-', linewidth=2)
        plt.text(point.real, point.imag, f' {point}', fontsize=12)
    
    plt.legend()
    plt.show()

def get_natural_freqs(data: pd.DataFrame, options: dict) -> None:

    #Extract data
    t = data['t'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

    #extract force
    force_0 = data['F0'].to_numpy()
    force_1 = data['F1'].to_numpy()
    force_2 = data['F2'].to_numpy()
    force_3 = data['F3'].to_numpy()
    force_4 = data['F4'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['A0'].to_numpy()
    response_1 = data['A1'].to_numpy()
    response_2 = data['A2'].to_numpy()
    response_3 = data['A3'].to_numpy()
    response_4 = data['A4'].to_numpy()


    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force_0)

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

    # Find peaks in FRF to get natural frequencies, choose which measurement location to use
    peaks, _ = find_peaks(FRF_1, prominence=3, distance=200)
    natural_frequencies = freqs[peaks]

    # For Trial Merged Random F1 10sec1, 50 height is acceptable
    
    return print("Natural frequencies are", natural_frequencies, "Hz")

def get_mode_shapes(data= pd.DataFrame, options= dict)-> None:
    
   #Extract data
    t = data['t'].to_numpy()

    #If sampling frequency and duration is available, use code below
    #Fs = 1000  #insert sampling frequency
    #T = 5      #Insert sampling duration
    #N = Fs * T # Number of samples datapoints

    #If not, extract from csv and use code below
    Fs = 1/(t[1]-t[0])
    T = t[-1]
    N = len(t)

    #extract force
    force_0 = data['F0'].to_numpy()
    force_1 = data['F1'].to_numpy()
    force_2 = data['F2'].to_numpy()
    force_3 = data['F3'].to_numpy()
    force_4 = data['F4'].to_numpy()

    # extract responses (accelerations)
    response_0 = data['A0'].to_numpy()
    response_1 = data['A1'].to_numpy()
    response_2 = data['A2'].to_numpy()
    response_3 = data['A3'].to_numpy()
    response_4 = data['A4'].to_numpy()


    # fft - rfft is used to only get the positive frequencies
    F_force = rfft(force_0)

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

    ## Remove this if argand plot plan is abandoned
    cFRF_0 = (F_resp_0 / F_force)
    cFRF_1 = (F_resp_1 / F_force)
    cFRF_2 = (F_resp_2 / F_force)
    cFRF_3 = (F_resp_3 / F_force)
    cFRF_4 = (F_resp_4 / F_force)

    #Use this if sticking with imaginary inertance. Scale of imaginary receptance is too low
    # Calculating the peak of imaginary value of FRF, based on literature this is the easiest way to find mode shape experimentally
    imgFRF_0 = np.imag(F_resp_0 / F_force)
    imgFRF_1 = np.imag(F_resp_1 / F_force)
    imgFRF_2 = np.imag(F_resp_2 / F_force)
    imgFRF_3 = np.imag(F_resp_3 / F_force)
    imgFRF_4 = np.imag(F_resp_4 / F_force)


    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(6, 9), sharex=True)

    # Plot data
    ax[0].plot(freqs, imgFRF_0, color='r')
    ax[0].set_title("Imaginary FRF - Accelerometer 1")
    ax[0].set_xlabel("Frequency (Hz)")
    ax[0].set_ylabel("Response")

    ax[1].plot(freqs, imgFRF_2, color='g')
    ax[1].set_title("Imaginary FRF - Accelerometer 2")
    ax[1].set_xlabel("Frequency (Hz)")
    ax[1].set_ylabel("Response")

    ax[2].plot(freqs, imgFRF_4, color='b')
    ax[2].set_title("Imaginary FRF - Accelerometer 3")
    ax[2].set_xlabel("Frequency (Hz)")
    ax[2].set_ylabel("Response")

    fig.tight_layout()

    plt.show()

    ### ARGAND DIAGRAM###
    # Find peaks in FRF to get natural frequencies, choose which measurement location to use
    peaks, _ = find_peaks(FRF_1, prominence=3, distance=200)  # Adjust threshold as needed


    arg = []

    for i in range(len(peaks)):  # Loop through all peaks
        arg_i = np.array([cFRF_0[peaks[i]], cFRF_2[peaks[i]], cFRF_4[peaks[i]]])
        arg.append(arg_i)

    # Convert list of arrays into a single NumPy array for easier processing
    arg = np.array(arg)

    fig, ax = plt.subplots()
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Argand Diagram')
    
    arg_peaks = arg[1]
    colors = ['r', 'g', 'b']  # Default colors if none provided
    
    for i, point in enumerate(arg_peaks):
        color = colors[i % len(colors)]  # Cycle through colors if needed
        plt.scatter(point.real, point.imag, color=color, s=50, label=f'Accelerometer {i*2}')
        plt.plot([0, point.real], [0, point.imag], color=color, linestyle='-', linewidth=2)
        plt.text(point.real, point.imag, f' {point}', fontsize=12)
    
    plt.legend()
    plt.show()


    #START PRODUCING MODESHAPE LIST
    ms = []  # Initialize an empty list to store ms_i arrays

    for i in range(len(peaks)):  # Loop through all peaks
        ms_i = np.array([imgFRF_0[peaks[i]], imgFRF_2[peaks[i]], imgFRF_4[peaks[i]]])
    
        # Normalize by dividing by the maximum absolute value in ms_i
        max_abs_value = np.max(np.abs(ms_i)) if np.any(ms_i) else 1  # Avoid division by zero
        ms_i = ms_i / max_abs_value
    
        ms.append(ms_i)

    # Convert list of arrays into a single NumPy array for easier processing
    ms = np.array(ms)

    # Print results
    for idx, m in enumerate(ms, start=1):
        print(f"ms_{idx}", m)

    return ms

data = pd.read_csv(r"gle\backend\data\STEPPED_2.csv") 
get_natural_freqs(data, {})
mode_shape = get_mode_shapes(data, {})