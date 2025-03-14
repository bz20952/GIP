from scipy.signal import butter
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt

#input needed:
#csv file of acceleration vs time
#location of accelerometer
#fs #sampling frequency
#low pass cutoff
#high pass cutoff
#low band cutoff
#high band cutoff

# Read the CSV file
filename = 'gle/backend/data/FREE_400_4.csv'  # Replace with the actual filename

# Assuming the file has two columns: 'Time' and 'Acceleration'
data = pd.read_csv(filename)  # Reads the CSV file into a DataFrame

# Extract time and acceleration data from the DataFrame
time = data['t']  # Time column
acceleration = data['l/2']  # Acceleration column

def lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

if __name__ == "__main__":
    b,a=bandpass(60,500,2000)
    accel_bandpass=signal.lfilter(b,a,acceleration)

plt.figure(figsize=(10, 6))
plt.plot(time, accel_bandpass, label='Filtered Data', color='r', linewidth=2)
plt.plot(time, acceleration, label='Unfiltered Data', color='b', linewidth=2)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
#plt.title('Filtered Signal')
plt.legend(loc='best')
plt.grid(True)
plt.show()