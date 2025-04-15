import serial
import csv
import time
import matplotlib.pyplot as plt
import numpy as np
import re
import threading
import gen
from datetime import datetime
import pandas as pd


def run_test():

    """Entrypoint for semi-automated testing."""

    duration = float(input("Enter the duration over which you wish to excite the structure (in seconds): "))
    sampling_frequency = int(input("Enter the sampling frequency (in Hz): "))
    com_port = input("Enter the COM port of your data logger (default is COM4): ").strip() or 'COM4'
    is_shaker = input("Are you using a shaker? (y/n): ").strip().lower() == 'y'  # Converts user input to boolean
    if is_shaker:
        wave = define_signal(duration)
    else:
        wave = []
    sound_thread = threading.Thread(target=gen.play_wave, args=(wave, 3))  # Add a three second delay so that excitation starts after data collection begins
    
    # read_data_thread = threading.Thread(target=read_data, args=(com_port, duration, sampling_frequency))  # Start reading data from the Teensy

    print("Starting test...")
    sound_thread.start()  # Start the sound thread if using a shaker
    read_data(com_port, duration+3, sampling_frequency)  # Start reading data from the Teensy
    sound_thread.join()  # Wait for the sound thread to finish
    # read_data_thread.start()  # Start the data collection thread
    # read_data_thread.join()  # Wait for the data collection thread to finish
    print("Test completed.")


def define_signal(duration):

    """Defines signal sent to shaker."""

    valid_excitation = False
    while not valid_excitation:
        excitation_type = input("Enter the type of excitation (sine, sine sweep, random, stepped sweep): ").strip().lower()
        if excitation_type in ["sine", "sine sweep", "random", "stepped sweep"]:
            valid_excitation = True
        else:
            print('Not a valid excitation type. Please try again.')
    amplitude = float(input("Enter the amplitude of the signal: "))

    if excitation_type == "sine":
        frequency = float(input("Enter the frequency of the sine wave (Hz): "))
        wave = gen.generate_sine_wave(frequency, amplitude, 0, duration)
    elif excitation_type == "sine sweep":
        start_freq = float(input("Enter the start frequency of the sweep (Hz): "))
        end_freq = float(input("Enter the end frequency of the sweep (Hz): "))
        wave = gen.generate_sine_sweep(start_freq, end_freq, amplitude, duration)
    elif excitation_type == "random":
        lowcut = float(input("Enter the lower bound of the desired frequency range (Hz): "))
        highcut = float(input("Enter the upper bound of the desired frequency range (Hz): "))
        wave = gen.generate_random_signal(lowcut, highcut, amplitude, duration)
    elif excitation_type == "stepped sweep":
        start_freq = float(input("Enter the start frequency of the sweep (Hz): "))
        end_freq = float(input("Enter the end frequency of the sweep (Hz): "))
        wave = gen.generate_stepped_sweep(start_freq, end_freq, 1, amplitude)

    return wave


def read_data(com_port, duration, fs):

    """Reads data from the serial port."""

    # Set the correct serial port and baud rate
    ser = serial.Serial(com_port, 128000, timeout=0.1, write_timeout=0.1)
    time.sleep(2)  # Allow serial connection to fully initialize
    ser.reset_input_buffer()  # Flush any old data from the buffer

    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv" # Change as needed
    # discard_time = 2  # Discard first 2 seconds of data to remove startup noise

    # Initialize start time
    start_time = None
    offset_start_time = None  # Adjusted start time after discarding first 2s
    accel_offset = 0.98  # Adjust for accelerometer offset (steady-state reading)

    # Regex pattern to validate acceleration (floating-point number with optional sign)
    float_pattern = re.compile(r"^-?\d+(\.\d+)?$")

    # Open CSV file and start data collection
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Acceleration", "Force"])

        start_time = time.time()  # Record the start time

        try:
            print(f"Recording. Press CTRL+C to stop.")
            buffer = ""  # Stores incomplete serial data temporarily

            while True:
                if ser.in_waiting > 0:  # Read only if there is data in the buffer
                    serial_chunk = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')  # Read all available bytes
                    buffer += serial_chunk  # Add new data to buffer
                    
                    # Split into lines and process each one
                    lines = buffer.split("\n")
                    buffer = lines[-1]  # Keep the last (possibly incomplete) line for the next iteration
                    complete_lines = lines[:-1]  # Process only fully completed lines

                    for line in complete_lines:
                        serial_line = line.strip()  # Remove extra spaces and newline

                        if "," not in serial_line:
                            continue  # Skip lines without proper comma separation
                        
                        data = serial_line.split(",")  # Split values

                        if len(data) == 3:  # Ensure correct number of values
                            timestamp_str, acceleration_str, force_str = data  # Extract components

                            # Validate timestamp: Must be a pure integer
                            if not timestamp_str.isdigit():
                                continue  # Skip invalid data

                            # Validate acceleration value: Must match float pattern (e.g., -0.03, 1.23, etc.)
                            if not float_pattern.fullmatch(acceleration_str):
                                continue  # Skip invalid data

                            try:
                                timestamp = int(timestamp_str)  # Teensy's `micros()` time (µs)
                                acceleration = float(acceleration_str) - accel_offset  # Remove offset
                                force = float(force_str)

                                # Correct start_time initialization
                                if start_time is None:
                                    start_time = timestamp

                                # Convert timestamp to seconds relative to the start time
                                time_in_seconds = timestamp / 1E6  # Convert µs to seconds

                                # Discard the first 2 seconds of noisy readings
                                # if time_in_seconds < discard_time:
                                #     continue

                                # Ensure timestamp starts from 0 after discarding phase
                                # if offset_start_time is None:
                                #     offset_start_time = timestamp

                                # adjusted_time = (timestamp - offset_start_time) / 1e6  # ✅ Reset time to start at 0s

                                # # Prevent extremely large timestamps from causing issues
                                # if adjusted_time > duration + 2:
                                #     print(f"Warning: Unusual timestamp detected ({adjusted_time}s), skipping...")
                                #     continue

                                # Save to CSV
                                writer.writerow([time_in_seconds, acceleration, force])

                                # # Stop recording after the specified duration
                                # if adjusted_time >= duration:
                                #     print("Recording complete. Generating plots...")
                                #     raise KeyboardInterrupt  # Exit the loop to plot

                            except ValueError:
                                print("Error parsing data:", serial_line)  # Ignore corrupted data

                current_time = time.time()  # Get the current time
                elapsed_time = current_time - start_time  # Calculate elapsed time
                if elapsed_time >= duration:  # Stop reading after the specified duration
                    print("Recording complete. Generating plots...")
                    raise KeyboardInterrupt  # Exit the loop to plot

        except KeyboardInterrupt:
            print("Data collection stopped.")
            ser.close()  # Close the serial connection
    
    # Save data and plot
    print("Data saved to", filename)
    plot(filename, fs)  # Plot the data


def plot(filename, fs):

    df = pd.read_csv(filename)  # Read the CSV file
    time_vals = df["Time (s)"].values  # Time values in seconds
    a0_vals = df["Acceleration"].values  # Acceleration values in g
    force_vals = df["Force"].values  # Force values in N

    # Generate the final acceleration and force vs time plot
    plt.figure(figsize=(10, 5))
    plt.plot(time_vals, a0_vals, label="Acceleration", linewidth=1.5)
    plt.plot(time_vals, force_vals, label="Force", linewidth=1.5)
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration / Force (unknown units)")
    plt.title(f"Recorded Data")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Compute & Plot the Discrete Fourier Transform (DFT)
    n = len(a0_vals)  # Number of samples
    f = np.fft.fftfreq(n, 1/fs)
    f = f[:n//2]
    fft = np.abs(np.fft.fft(a0_vals))[:n//2]

    # Generate the FFT plot
    plt.figure(figsize=(10, 5))
    plt.plot(f, fft/max(fft), label="Magnitude Spectrum", linewidth=1.5)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Frequency Spectrum of Acceleration Data")
    plt.xlim(0, fs/2)  # Limit x-axis to Nyquist frequency (fs/2)
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    run_test()
