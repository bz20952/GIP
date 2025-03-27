import serial
import csv
import time
import matplotlib.pyplot as plt
import numpy as np
import re  # Import regex module
import threading
import math
import sounddevice as sd


#     """Defines signal sent to shaker."""

def generate_sine_wave(frequency, amplitude, phase, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return wave

def generate_sine_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, t.size)
    wave = amplitude * np.sin(2 * np.pi * freqs * t)
    return wave

def generate_random_signal(lowcut, highcut, amplitude, duration, sample_rate=44100):
    freqs = np.linspace(lowcut, highcut, 100)
    wave = np.zeros(int(sample_rate * duration))
    for freq in freqs:
        sine_amplitude = np.random.random()
        sine_phase = np.random.random() * np.pi
        wave += generate_sine_wave(freq, sine_amplitude, sine_phase, duration, sample_rate)
    wave = (wave/max(np.abs(wave)))*amplitude
    return wave

def gen_step_sweep(start_freq, end_freq, interval, duration_per_freq=0.4, pause_duration=0.3, amplitude=1, sample_rate=44100):
    freqs = np.arange(start_freq, end_freq, interval)
    duration = duration_per_freq*len(freqs)
    signal_duration = duration_per_freq - pause_duration
    print('Duration:', duration, 's')
    wave = np.zeros(0) # Initialize an empty wave
    i = 0
    for freq in freqs:
    # Pause
        pause_samples = int(pause_duration * sample_rate)
        pause_wave = np.zeros(pause_samples)
        # Signal
        signal_samples = int(signal_duration * sample_rate)
        time_array = np.linspace(0, signal_duration, signal_samples)
        sine_wave = amplitude * np.sin(2 * np.pi * freq * time_array)
        # Apply windowing function for fade-in/fade-out
        window = windows.hann(signal_samples)  # You can use other window functions too
        windowed_sine_wave = sine_wave * window
        # Combine pause and signal
        freq_wave = np.concatenate([pause_wave, windowed_sine_wave])
        # Concatenate to the main wave
        wave = np.concatenate([wave, freq_wave])
    return wave

def play_wave(wave, sample_rate=44100):
    sd.play(wave, samplerate=sample_rate)
    sd.wait()


#       """Acquiring data output from microcontroller"""

# Set the correct serial port and baud rate
ser = serial.Serial('COM5', 128000, timeout=0.1, write_timeout=0.1)
time.sleep(2)  # Allow serial connection to fully initialize
ser.reset_input_buffer()  # Flush any old data from the buffer

filename = "NewComp_Sin_850_10s.csv" # Change as needed
recording_duration = 20  # Specify how long to capture data (in seconds)
discard_time = 2  # Discard first 2 seconds of data to remove startup noise

# Define sampling frequency (Change this if needed)
fs = 2000  # Hz (Sampling frequency of the sensor)
nyquist_freq = fs / 2  # Maximum frequency we can analyze

# Data storage list
time_vals = []
a0_vals = []
force_vals = []

# Initialize start time
start_time = None
offset_start_time = None  # ✅ Adjusted start time after discarding first 2s
accel_offset = 0.98  # ✅ Adjust for accelerometer offset (default reading when stationary)

# Regex pattern to validate acceleration (floating-point number with optional sign)
float_pattern = re.compile(r"^-?\d+(\.\d+)?$")

if __name__ == "__main__":

    sample_rate = 44100

    wave = generate_sine_wave(100, 1, 0, 10, sample_rate)
    # wave = generate_sine_sweep(20, 1000, 1, 20, sample_rate)
    # wave = generate_stepped_sweep(50, 1000, 990, 1, 20, sample_rate)
    # wave = gen_step_sweep(365, 375.1, 0.1)
    # wave = generate_random_signal(100, 150, 1, 20, sample_rate)

    # Play the wave in a separate thread
    sound_thread = threading.Thread(target=play_wave, args=(wave, sample_rate))
    sound_thread.start()

    plt.figure()
    plt.plot(wave)
    plt.show()

# ✅ Open CSV file and start data collection
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "A0 (g)", "Force(N)"])  # ✅ Time in seconds and corrected acceleration

    try:
        print(f"Recording for {recording_duration} seconds (first {discard_time}s discarded)...")
        buffer = ""  # Stores incomplete serial data temporarily

        while True:
            if ser.in_waiting > 0:  # ✅ Read only if there is data in the buffer
                serial_chunk = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')  # ✅ Read all available bytes
                buffer += serial_chunk  # Add new data to buffer
                
                # Split into lines and process each one
                lines = buffer.split("\n")
                buffer = lines[-1]  # Keep the last (possibly incomplete) line for the next iteration
                complete_lines = lines[:-1]  # Process only fully completed lines

                for line in complete_lines:
                    serial_line = line.strip()  # Remove extra spaces and newline

                    # Ensure the line contains exactly two values
                    if "," not in serial_line:
                        continue  # Skip lines without proper comma separation
                    
                    data = serial_line.split(",")  # Split values

                    if len(data) == 3:  # ✅ Ensure correct number of values
                        timestamp_str, acceleration_str, force_str = data  # Extract components

                        # ✅ Validate timestamp: Must be a pure integer
                        if not timestamp_str.isdigit():
                            continue  # Skip invalid data

                        # ✅ Validate acceleration value: Must match float pattern (e.g., -0.03, 1.23, etc.)
                        if not float_pattern.fullmatch(acceleration_str):
                            continue  # Skip invalid data

                        try:
                            timestamp = int(timestamp_str)  # Teensy's `micros()` time (µs)
                            acceleration = float(acceleration_str) - accel_offset  # ✅ Remove offset
                            force = float(force_str)

                            # ✅ Correct start_time initialization
                            if start_time is None:
                                start_time = timestamp

                            # ✅ Convert timestamp to seconds relative to the start time
                            time_in_seconds = (timestamp - start_time) / 1e6  # ✅ Convert µs to seconds

                            # ✅ Discard the first 2 seconds of noisy readings
                            if time_in_seconds < discard_time:
                                continue

                            # ✅ Ensure timestamp starts from 0 after discarding phase
                            if offset_start_time is None:
                                offset_start_time = timestamp

                            adjusted_time = (timestamp - offset_start_time) / 1e6  # ✅ Reset time to start at 0s

                            # ✅ Prevent extremely large timestamps from causing issues
                            if adjusted_time > recording_duration + 2:
                                print(f"Warning: Unusual timestamp detected ({adjusted_time}s), skipping...")
                                continue

                            # ✅ Store data in lists
                            time_vals.append(adjusted_time)
                            a0_vals.append(acceleration)
                            force_vals.append(force)

                            # ✅ Save to CSV
                            writer.writerow([adjusted_time, acceleration, force])

                            # ✅ Stop recording after the specified duration
                            if adjusted_time >= recording_duration:
                                print("Recording complete. Generating plots...")
                                raise KeyboardInterrupt  # Exit the loop to plot

                        except ValueError:
                            print("Error parsing data:", serial_line)  # ✅ Ignore corrupted data

    except KeyboardInterrupt:
        print("\nData collection stopped.")
        ser.close()

        # ✅ Generate the final acceleration vs time plot
        plt.figure(figsize=(10, 5))
        plt.plot(time_vals, a0_vals, label="Acceleration (g)", linewidth=1.5)
        plt.plot(time_vals, force_vals, label="Force (N)", linewidth=1.5)
        plt.xlabel("Time (s)")
        plt.ylabel("Response signal")
        plt.title(f"Acceleration Data and Force Over {recording_duration} Seconds")
        plt.legend()
        plt.grid(True)
        plt.show()

        # ✅ Compute & Plot the Discrete Fourier Transform (FFT)
        print("\nComputing Fourier Transform...")
        n = len(a0_vals)  # Number of samples
        f = np.fft.fftfreq(n, 1/fs)
        f = f[:n//2]
        fft = np.abs(np.fft.fft(a0_vals))[:n//2]


        # # ✅ Generate the FFT plot
        plt.figure(figsize=(10, 5))
        #plt.plot(freq_values, fft_magnitude, label="Magnitude Spectrum", linewidth=1.5)
        plt.plot(f, fft/max(fft), label="Magnitude Spectrum", linewidth=1.5)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.title("Frequency Spectrum of Acceleration Data")
        #plt.xlim(0, nyquist_freq)  # ✅ Limit x-axis to Nyquist frequency (fs/2)
        plt.legend()
        plt.grid(True)
        plt.show()

        print("Fourier Transform completed and plotted.")
        print("Plot displayed. Data saved to", filename)