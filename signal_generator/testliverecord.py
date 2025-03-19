import serial
import csv
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import re  # Import regex module
from collections import deque

# Set the correct serial port and baud rate
ser = serial.Serial('COM5', 128000, timeout=0.1, write_timeout=0.1)
time.sleep(2)  # Allow serial connection to initialize

filename = "teensy_data.csv"
recording = False  # Flag to control recording

# Data buffer for plotting
window_size = 1000
time_vals = deque(maxlen=window_size)
a0_vals = deque(maxlen=window_size)

# Initialize start time
start_time = None
accel_offset = 0.98  # ✅ Adjust for accelerometer offset (default reading when stationary)

# Regex pattern to validate acceleration (floating-point number with optional sign)
float_pattern = re.compile(r"^-?\d+(\.\d+)?$")

# Function to listen for keypress (Runs in a separate thread)
def listen_for_keypress():
    global recording
    while True:
        key = input()  # Wait for user input (Enter key)
        if key == "":
            recording = not recording
            print("Recording started..." if recording else "Recording stopped...")

# Start keypress listener thread
thread = threading.Thread(target=listen_for_keypress, daemon=True)
thread.start()

# Initialize live plotting
plt.ion()
fig, ax = plt.subplots()
plot_line, = ax.plot([], [], label="Acceleration (A0)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Acceleration (g)")
ax.set_title("Live Accelerometer Data")
ax.legend()
ax.set_ylim(-4, 4)
#ax.set_xlim(0, 5)  # ✅ Start with a 5-second window

# 🔹 Optimized update_plot() function
def update_plot():
    if len(time_vals) > 1:  # Only update if there's data
        t_last = time_vals[-1]  # Get the latest time value
        x_min = max(0, t_last - 5)  # Start 5 seconds before the latest time
        x_max = t_last  # Keep the latest time as the right boundary

        ax.set_xlim(x_min, x_max)  # Maintain a fixed 5-second window

        # ✅ Use slicing instead of `deque` overwriting to maintain smooth performance
        start_index = next((i for i, t in enumerate(time_vals) if t >= x_min), 0)

        time_vals_window = list(time_vals)[start_index:]  # Slice the last 5 seconds
        a0_vals_window = list(a0_vals)[start_index:]  # Slice corresponding values

        plot_line.set_xdata(time_vals_window)
        plot_line.set_ydata(a0_vals_window)

        ax.relim()
        ax.autoscale_view(scaley=False)  # ✅ Prevents y-axis from rescaling
        plt.draw()
        plt.pause(0.01)



# Open CSV file and start data collection
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "A0 (g)"])  # ✅ Time in seconds and corrected acceleration

    try:
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
                            print(f"Ignored corrupted timestamp: {serial_line}")
                            continue  # Skip invalid data

                        # ✅ Validate acceleration value: Must match float pattern (e.g., -0.03, 1.23, etc.)
                        if not float_pattern.fullmatch(acceleration_str):
                            print(f"Ignored corrupted acceleration data: {serial_line}")
                            continue  # Skip invalid data

                        try:
                            timestamp = int(timestamp_str)  # Teensy's `micros()` time (µs)
                            acceleration = float(acceleration_str) - accel_offset  # ✅ Remove offset

                            # Initialize start time
                            if start_time is None:
                                start_time = timestamp

                            # Convert timestamp to seconds relative to the start time
                            time_in_seconds = (timestamp - start_time) / 1e6  # ✅ Convert µs to seconds

                            # Store data for plotting
                            time_vals.append(time_in_seconds)
                            a0_vals.append(acceleration)

                            # Save to CSV if recording
                            if recording:
                                writer.writerow([time_in_seconds, acceleration])

                        except ValueError:
                            print("Error parsing data:", serial_line)  # ✅ Ignore corrupted data

                update_plot()  # ✅ Update the plot dynamically after processing all lines

    except KeyboardInterrupt:
        print("\nData collection stopped.")
        ser.close()
        plt.ioff()  # Turn off interactive mode































































