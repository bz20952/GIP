from matplotlib import pyplot as plt
import numpy as np

def plot_sine_wave(frequency, amplitude, phase, duration, sample_rate=1000):
    
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    
    plt.figure(figsize=(10, 4))
    plt.plot(t, wave)
    plt.title(f'Sine Wave: {frequency}Hz, Amplitude: {amplitude}')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.savefig('sine_wave.png')