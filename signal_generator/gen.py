import numpy as np
import sounddevice as sd
from trace import plot_wave_gif
import threading
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

def generate_sine_wave(frequency, amplitude, phase, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return wave

def generate_sine_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, t.size)
    wave = amplitude * np.sin(2 * np.pi * freqs * t)
    return wave

# def bandpass_filter(data, lowcut, highcut, sample_rate, order=5):
#     nyquist = 0.5 * sample_rate
#     low = lowcut / nyquist
#     high = highcut / nyquist
#     b, a = butter(order, [low, high], btype='band')
#     y = lfilter(b, a, data)
#     return y

def generate_random_signal(lowcut, highcut, amplitude, duration, sample_rate=44100):
    freqs = np.linspace(lowcut, highcut, 1000)
    wave = np.zeros(int(sample_rate * duration))
    for freq in freqs:
        sine_amplitude = (np.random.random() - 0.5)*2
        wave += generate_sine_wave(freq, sine_amplitude, 0, duration, sample_rate)
    wave = (wave/max(np.abs(wave)))*amplitude
    return wave

def generate_stepped_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, t.size)
    wave = amplitude * np.sign(np.sin(2 * np.pi * freqs * t))
    return wave

def play_wave(wave, sample_rate=44100):
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

# def define_signal():

#     """Defines signal sent to shaker."""

#     excitation_type = input("Enter the type of excitation (sine, sweep, random, stepped): ")
#     amplitude = float(input("Enter the amplitude of the sine wave: "))
#     duration = float(input("Enter the duration of the sine wave (seconds): "))

#     if excitation_type == "sine":
#         frequency = float(input("Enter the frequency of the sine wave (Hz): "))
#         wave = generate_sine_wave(frequency, amplitude, 0, duration)
#     elif excitation_type == "sweep":
#         start_freq = float(input("Enter the start frequency of the sweep (Hz): "))
#         end_freq = float(input("Enter the end frequency of the sweep (Hz): "))
#         wave = generate_sine_sweep(start_freq, end_freq, amplitude, duration)
#     elif excitation_type == "random":
#         lowcut = float(input("Enter the lower cutoff frequency of the bandpass filter (Hz): "))
#         highcut = float(input("Enter the upper cutoff frequency of the bandpass filter (Hz): "))
#         wave = generate_random_signal(lowcut, highcut, amplitude, duration)

#     # wave = generate_sine_wave(1000, 1, 0, 60)

#     return wave


if __name__ == "__main__":
    # frequency = float(input("Enter the frequency of the sine wave (Hz): "))
    # amplitude = float(input("Enter the amplitude of the sine wave: "))
    # phase = float(input("Enter the phase of the sine wave (radians): "))
    # duration = float(input("Enter the duration of the sine wave (seconds): "))
    sample_rate = 44100

    # wave = generate_sine_wave(300, 1, 0, 60, sample_rate)
    # wave = generate_sine_sweep(0.5, 1000, 1, 20, sample_rate)
    wave = generate_random_signal(50, 100, 0.1, 10, sample_rate)
    # wave = generate_stepped_sweep(0.5, 1000, 1, 20, sample_rate)

    # # Play the wave in a separate thread
    # sound_thread = threading.Thread(target=play_wave, args=(wave, sample_rate))
    # sound_thread.start()

    # n = 25  # Sample the wave at every nth data point for plotting
    # ani = plot_wave_gif(wave[::n], sample_rate//n, filename='sine_sweep.gif', save=True)

    # # Keep the script running while the sound plays
    # sound_thread.join()

    # play_wave(wave, sample_rate)
    plt.figure()
    # plot_path = f'./images/wave.png'
    plt.plot(wave)
    plt.show()
