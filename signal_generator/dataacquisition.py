import serial
import csv
import time
import matplotlib.pyplot as plt
import numpy as np
import re  # Import regex module

# Set the correct serial port and baud rate
ser = serial.Serial('COM5', 128000, timeout=0.1, write_timeout=0.1)
time.sleep(2)  # ✅ Allow serial connection to fully initialize
ser.reset_input_buffer()  # ✅ Flush any old data from the buffer

filename = "teensy_data.csv"
recording_duration = 10  # ✅ Specify how long to capture data (in seconds)
discard_time = 2  # ✅ Discard first 2 seconds of data to remove startup noise

# ✅ Define sampling frequency (Change this if needed)
fs = 2000  # Hz (Sampling frequency of the sensor)
nyquist_freq = fs / 2  # Maximum frequency we can analyze

# Data storage lists
time_vals = []
a0_vals = []

# Initialize start time
start_time = None
offset_start_time = None  # ✅ Adjusted start time after discarding first 2s
accel_offset = 0.98  # ✅ Adjust for accelerometer offset (default reading when stationary)

# Regex pattern to validate acceleration (floating-point number with optional sign)
float_pattern = re.compile(r"^-?\d+(\.\d+)?$")

# ✅ Open CSV file and start data collection
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "A0 (g)"])  # ✅ Time in seconds and corrected acceleration

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

                    if len(data) == 2:  # ✅ Ensure correct number of values
                        timestamp_str, acceleration_str = data  # Extract components

                        # ✅ Validate timestamp: Must be a pure integer
                        if not timestamp_str.isdigit():
                            continue  # Skip invalid data

                        # ✅ Validate acceleration value: Must match float pattern (e.g., -0.03, 1.23, etc.)
                        if not float_pattern.fullmatch(acceleration_str):
                            continue  # Skip invalid data

                        try:
                            timestamp = int(timestamp_str)  # Teensy's `micros()` time (µs)
                            acceleration = float(acceleration_str) - accel_offset  # ✅ Remove offset

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

                            # ✅ Save to CSV
                            writer.writerow([adjusted_time, acceleration])

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
        plt.plot(time_vals, a0_vals, label="Acceleration (A0)", linewidth=1.5)
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (g)")
        plt.title(f"Acceleration Data Over {recording_duration} Seconds")
        plt.legend()
        plt.grid(True)
        plt.show()

        # ✅ Compute & Plot the Discrete Fourier Transform (FFT)
        print("\nComputing Fourier Transform...")
        n = len(a0_vals)  # Number of samples
        #freq_values = np.fft.rfftfreq(n, d=1/fs)  # Frequency bins up to fs/2
        #fft_magnitude = np.abs(np.fft.rfft(a0_vals))  # Compute the FFT magnitude

        #Trial FFT computation
        X = np.fft.fft(a0_vals)
        X_mag = np.abs(X) / n

        fstep = fs / n
        f = np.linspace(0, (n-1)*fstep, n) #freq steps

        f_plot = f[0:int(n/2+1)]
        X_mag_plot = 2 * X_mag[0:int(n/2+1)]
        X_mag_plot[0] = X_mag_plot[0] / 2


        # ✅ Generate the FFT plot
        plt.figure(figsize=(10, 5))
        #plt.plot(freq_values, fft_magnitude, label="Magnitude Spectrum", linewidth=1.5)
        plt.plot(f_plot, X_mag_plot, label="Magnitude Spectrum", linewidth=1.5)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.title("Frequency Spectrum of Acceleration Data")
        #plt.xlim(0, nyquist_freq)  # ✅ Limit x-axis to Nyquist frequency (fs/2)
        plt.legend()
        plt.grid(True)
        plt.show()

        print("Fourier Transform completed and plotted.")
        print("Plot displayed. Data saved to", filename)



