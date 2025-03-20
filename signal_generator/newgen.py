import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import threading
from scipy.signal import butter, lfilter

def generate_sine_wave(frequency, amplitude, phase, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return wave, t

def generate_sine_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, t.size)
    wave = amplitude * np.sin(2 * np.pi * freqs * t)
    return wave, t

def bandpass_filter(data, lowcut, highcut, sample_rate, order=5):
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def generate_random_signal(lowcut, highcut, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.random.uniform(-1, 1, size=t.shape)
    filtered_wave = bandpass_filter(wave, lowcut, highcut, sample_rate)
    return wave, t

def generate_stepped_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, t.size)
    wave = amplitude * np.sign(np.sin(2 * np.pi * freqs * t))
    return wave, t

def play_wave(wave, sample_rate=44100):
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

def plot_waveform(wave, t, title):
    plt.figure(figsize=(10, 4))
    plt.plot(t, wave, label=title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title(f"Waveform of {title}")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    sample_rate = 44100
    t = None  # Ensure t is defined before use
    wave = None
    
    # Uncomment the desired wave to play
    # wave, t = generate_sine_wave(300, 1, 0, 5, sample_rate)
    # wave, t = generate_sine_sweep(1, 5, 1, 5, sample_rate)
    wave, t = generate_random_signal(0.5, 1, 1, 5, sample_rate)
    # wave, t = generate_stepped_sweep(0.5, 600, 1, 60, sample_rate)
    
    if wave is not None and t is not None:
        # Play the wave in a separate thread
        sound_thread = threading.Thread(target=play_wave, args=(wave, sample_rate))
        sound_thread.start()
        sound_thread.join()

        # Plot the waveform
        plot_waveform(wave, t, "Generated Signal")