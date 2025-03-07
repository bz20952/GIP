import serial
import csv
import time
import threading
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

            # else:
            #     print("\nData collection stopped.")
            #     ser.close()
            #     break

    except KeyboardInterrupt:
        print("\nData collection stopped.")
        ser.close()
        post_process()





