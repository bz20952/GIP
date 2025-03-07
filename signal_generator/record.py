import serial
import csv
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from gen import define_signal, play_wave
from post_process import post_process

# Define the signal to be sent to the Teensy
wave = define_signal()

# Play the wave in a separate thread
sound_thread = threading.Thread(target=play_wave, args=(wave,))
sound_thread.start()
# # Keep the script running while the sound plays
# sound_thread.join()

# Set the correct serial port and baud rate
ser = serial.Serial('/dev/cu.usbmodem82679401', 115200) # Change to your Teensy's port
time.sleep(2)  # Allow serial connection to initialize

filename = "teensy_data.csv"
recording = False  # Flag to control recording

# Data buffer for plotting
window_size = 200  # Number of points to display
time_vals = deque(maxlen=window_size)
a0_vals = deque(maxlen=window_size)

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
line, = ax.plot([], [], label="Acceleration (A0)")
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Acceleration (A0)")
ax.set_title("Live Accelerometer Data")
ax.legend()

# Function to update plot
def update_plot():
    if time_vals:  # Only update if there's data
        line.set_xdata(time_vals)
        line.set_ydata(a0_vals)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)

# Open CSV file and start data collection
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    # writer.writerow(["Time (ms)", "A0", "A1", "A2", "A3"])  # CSV header
    writer.writerow(["Time (ms)", "A0"])  # CSV header

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()  # Read serial data
            data = line.split(",")  # Split values

            if recording and len(data) == 2:  # Ensure correct number of values
                writer.writerow(data)
                print(data)  # Print to console for debugging


                # Store data for plotting (Convert to float/int)
                time_vals.append(float(data[0]))  # Time (ms)
                a0_vals.append(int(data[1]))  # Acceleration (A0)

                update_plot()  # Update the plot

            # else:
            #     print("\nData collection stopped.")
            #     ser.close()
            #     break

    except KeyboardInterrupt:
        print("\nData collection stopped.")
        ser.close()
        post_process()





