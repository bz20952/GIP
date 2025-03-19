import serial
import csv
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Set the correct serial port and baud rate
ser = serial.Serial('COM5', 128000, timeout=0.1, write_timeout=0.1)  # Change to your Teensy's port
time.sleep(2)  # Allow serial connection to initialize

filename = "teensy_data.csv"
recording = False  # Flag to control recording

# Data buffer for plotting
window_size = 200  # Number of points to display
time_vals = deque(maxlen=window_size)
a0_vals = deque(maxlen=window_size)

# Initialize start time
start_time = None
accel_offset = 0.98  # ✅ Adjust for accelerometer offset (default reading when stationary)

# Function to listen for keypress (Runs in a separate thread)
def listen_for_keypress():
    global recording
    while True:
        key = input()  # Wait for user input (Enter key)
        if key == "":
            recording = not recording
            if recording:
                print("Recording started...")
            else:
                print("Recording stopped...")

# Start keypress listener thread
thread = threading.Thread(target=listen_for_keypress, daemon=True)
thread.start()

# Initialize live plotting
plt.ion()
fig, ax = plt.subplots()
plot_line, = ax.plot([], [], label="Acceleration (A0)")
ax.set_xlabel("Time (s)")  # ✅ Time now in seconds
ax.set_ylabel("Acceleration (g)")
ax.set_title("Live Accelerometer Data")
ax.legend()
ax.set_ylim(-4, 4)  # ✅ Fixed y-axis range from -4 to 4 g
ax.set_xlim(0, 10)  # ✅ Set an initial x-axis window (adjusts dynamically)

# Function to update plot
def update_plot():
    if time_vals:  # Only update if there's data
        plot_line.set_xdata(time_vals)
        plot_line.set_ydata(a0_vals)
        ax.set_xlim(max(0, time_vals[0]), max(10, time_vals[-1]))  # Keep a scrolling 10s window
        ax.relim()
        ax.autoscale_view(scaley=False)  # ✅ Prevents y-axis from rescaling
        plt.draw()
        plt.pause(0.01)

# Open CSV file and start data collection
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "A0 (g)"])  # ✅ Time in seconds and corrected acceleration

    try:
        while True:
            if ser.in_waiting > 0:  # ✅ Read only if there is data in the buffer
                serial_chunk = ser.read(ser.in_waiting).decode('utf-8')  # ✅ Read all available bytes at once
                
                # Split into lines and process each one
                lines = serial_chunk.split("\n")
                
                for line in lines:
                    serial_line = line.strip()  # Remove extra spaces and newline
                    
                    data = serial_line.split(",")  # Split values

                    if len(data) == 2:  # Ensure correct number of values
                        try:
                            timestamp = int(data[0])  # Teensy's `millis()` time (ms)
                            acceleration = float(data[1]) - accel_offset  # ✅ Remove offset

                            # Initialize start time
                            if start_time is None:
                                start_time = timestamp

                            # Convert timestamp to seconds relative to the start time
                            time_in_seconds = (timestamp - start_time) / 1e6  # ✅ Convert ms to seconds

                            # Store data for plotting
                            time_vals.append(time_in_seconds)
                            a0_vals.append(acceleration)

                            # Save to CSV if recording
                            if recording:
                                writer.writerow([time_in_seconds, acceleration])
                                print(f"Time: {time_in_seconds:.3f} s, Acceleration: {acceleration:.3f} g")  # ✅ Print to console

                        except ValueError:
                            print("Error parsing data:", serial_line)

                update_plot()  # ✅ Update the plot dynamically after processing all lines

    except KeyboardInterrupt:
        print("\nData collection stopped.")
        ser.close()
        plt.ioff()  # Turn off interactive mode