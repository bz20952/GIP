import numpy as np
import sounddevice as sd
from tracer import plot_wave_gif
import matplotlib.pyplot as plt
from scipy.signal.windows import hann


def generate_sine_wave(frequency, amplitude, phase, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return wave


def generate_sine_sweep(start_freq, end_freq, amplitude, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # freqs = np.linspace(start_freq, end_freq, t.size)
    # wave = amplitude * np.sin(2 * np.pi * freqs * t)
    hz_per_second = (end_freq - start_freq) / duration
    wave = amplitude * np.sin(2*np.pi*(start_freq+(hz_per_second*t))*t)
    return wave


def generate_random_signal(lowcut, highcut, amplitude, duration, sample_rate=44100):
    freqs = np.linspace(lowcut, highcut, 1000)
    wave = np.zeros(int(sample_rate * duration))
    for freq in freqs:
        sine_amplitude = np.random.random()
        sine_phase = np.random.random() * np.pi
        wave += generate_sine_wave(freq, sine_amplitude, sine_phase, duration, sample_rate)
    wave = (wave/max(np.abs(wave)))*amplitude
    return wave


def generate_stepped_sweep(start_freq, end_freq, interval, amplitude, duration_per_freq=0.4, pause_duration=0.3, sample_rate=44100):
    freqs = np.arange(start_freq, end_freq, interval)
    duration = duration_per_freq*len(freqs)
    signal_duration = duration_per_freq - pause_duration
    print('Duration:', duration, 's')
    wave = np.zeros(0) # Initialize an empty wave
    for freq in freqs:
        # Pause
        pause_samples = int(pause_duration * sample_rate)
        pause_wave = np.zeros(pause_samples)
        # Signal
        signal_samples = int(signal_duration * sample_rate)
        time_array = np.linspace(0, signal_duration, signal_samples)
        sine_wave = amplitude * np.sin(2 * np.pi * freq * time_array)
        window = hann(signal_samples)  # You can use other window functions too
        windowed_sine_wave = sine_wave * window
        # Combine pause and signal
        freq_wave = np.concatenate([pause_wave, windowed_sine_wave])
        # Concatenate to the main wave
        wave = np.concatenate([wave, freq_wave])
    return wave


def play_wave(wave, delay=0, sample_rate=44100):
    silence = np.zeros(int(delay * sample_rate))  # Create silence for the delay
    wave = np.concatenate([silence, wave])  # Prepend silence to the wave
    sd.play(wave, samplerate=sample_rate)
    sd.wait()


if __name__ == "__main__":
    sample_rate = 44100

    # wave = generate_sine_wave(300, 1, 0, 60, sample_rate)
    wave = generate_sine_sweep(0.5, 10, 1, 20, sample_rate)
    # wave = generate_stepped_sweep(50, 1000, 50, 0.1, sample_rate)
    # wave = generate_stepped_sweep(0.5, 1000, 1, 20, sample_rate)

    # # Play the wave in a separate thread
    # sound_thread = threading.Thread(target=play_wave, args=(wave, sample_rate))
    # sound_thread.start()

    # n = 25  # Sample the wave at every nth data point for plotting
    # ani = plot_wave_gif(wave[::n], sample_rate//n, filename='sine_sweep.gif', save=True)

    # # Keep the script running while the sound plays
    # sound_thread.join()

    # play_wave(wave, sample_rate)
    # plot_path = f'./images/wave.png'
    plt.plot(np.linspace(0, 20, len(wave)), wave)
    plt.show()
