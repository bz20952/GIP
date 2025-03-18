import serial
import matplotlib.pyplot as plt
import time
import threading
from collections import deque

# Serial setup - Change to your correct port
ser = serial.Serial('/dev/cu.usbmodem14101', 115200, timeout=0.1)

# Store only the most recent points
max_points = 500  # Reduce this if lag persists
xdata = deque(maxlen=max_points)
ydata = deque(maxlen=max_points)

# Start time for real-time reference
start_time = time.time()

# Plot setup
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-10, 10)  # Adjust range as needed

def read_serial():
    """Continuously read serial data in a separate thread."""
    while True:
        try:
            ser.flush()  # Prevents buffer buildup
            data = ser.readline().decode('utf-8').strip()
            if data:
                parts = data.split(",")
                if len(parts) == 2:
                    arduino_time = float(parts[0]) / 1e6  # Convert µs to sec
                    sensor_value = float(parts[1])

                    real_time = time.time() - start_time  # True real-time tracking

                    xdata.append(real_time)
                    ydata.append(sensor_value)
        except Exception as e:
            print("Error:", e)

# Start background thread for reading serial
thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

while True:
    try:
        if len(xdata) > 2:
            line.set_data(xdata, ydata)
            ax.set_xlim(xdata[0], xdata[-1])  # Dynamic scrolling
            plt.draw()
            plt.pause(0.001)  # Faster refresh rate than FuncAnimation
    except KeyboardInterrupt:
        print("Stopping plot...")
        break

