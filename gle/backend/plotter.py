from matplotlib import pyplot as plt
import numpy as np

def plot_sine_wave(frequency, amplitude, duration, sample_rate=1000):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    y = amplitude * np.sin(2 * np.pi * frequency * t)
    
    plt.figure(figsize=(10, 4))
    plt.plot(t, y)
    plt.title(f'Sine Wave: {frequency}Hz, {amplitude} Amplitude')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.savefig('./images/ssine_wave.png')