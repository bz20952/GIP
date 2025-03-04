import numpy as np
import sounddevice as sd
from trace import plot_wave_gif
import threading

def generate_sine_wave(frequency, amplitude, phase, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return wave

def generate_sine_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, t.size)
    wave = amplitude * np.sin(2 * np.pi * freqs * t)
    return wave

def generate_random_signal(amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.random.uniform(-1, 1, size=t.shape)
    return wave

def generate_stepped_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, t.size)
    wave = amplitude * np.sign(np.sin(2 * np.pi * freqs * t))
    return wave

def play_wave(wave, sample_rate=44100):
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

if __name__ == "__main__":
    # frequency = float(input("Enter the frequency of the sine wave (Hz): "))
    # amplitude = float(input("Enter the amplitude of the sine wave: "))
    # phase = float(input("Enter the phase of the sine wave (radians): "))
    # duration = float(input("Enter the duration of the sine wave (seconds): "))
    sample_rate = 1000

    # wave = generate_sine_wave(2, 50, 0, 5, sample_rate)
    # wave = generate_sine_sweep(0.5, 1.5, 50, 5, sample_rate)
    wave=generate_random_signal(5,10,sample_rate)
    # wave = generate_stepped_sweep(0.5, 2, 50, 10, sample_rate)
   

    # Play the wave in a separate thread
    sound_thread = threading.Thread(target=play_wave, args=(wave, sample_rate))
    sound_thread.start()

    n = 25  # Sample the wave at every nth data point for plotting
    # ani = plot_wave_gif(wave[::n], sample_rate//n, filename='random_signal.gif', save=True)

    # Keep the script running while the sound plays
    sound_thread.join()

    play_wave(wave, sample_rate)
    