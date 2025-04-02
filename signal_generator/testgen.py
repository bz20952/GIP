import numpy as np
import sounddevice as sd
from trace import plot_wave_gif
import threading
import math
from scipy.signal import butter, lfilter, windows, welch
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

# def generate_random_signal(lowcut, highcut, amplitude, duration, sample_rate=44100):
#     freqs = np.linspace(lowcut, highcut, 10000)
#     wave = np.zeros(int(sample_rate * duration))
#     for freq in freqs:
#         # sine_amplitude = np.random.random()
#         sine_amplitude = 1.0 / np.sqrt(len(freqs))
#         sine_phase = np.random.random() * np.pi
#         wave += generate_sine_wave(freq, sine_amplitude, sine_phase, duration, sample_rate)
#     wave = (wave/max(np.abs(wave)))*amplitude
#     return wave

def generate_random_ifft_signal(lowcut, highcut, duration, sample_rate, target_psd_level):
    N = int(sample_rate * duration)
    freqs = np.fft.rfftfreq(N, 1 / sample_rate)

    # Define desired PSD shape (flat within band)
    PSD = np.zeros_like(freqs)
    in_band = (freqs >= lowcut) & (freqs <= highcut)
    PSD[in_band] = target_psd_level  # g²/Hz or arbitrary power units

    # Generate random phase
    phase = np.exp(1j * 2 * np.pi * np.random.rand(len(freqs)))

    # Create complex spectrum with defined magnitude
    amplitude = np.sqrt(PSD * sample_rate)  # magnitude per bin
    spectrum = amplitude * phase

    # Inverse FFT to get time-domain signal
    wave = np.fft.irfft(spectrum, n=N)

    # Normalize to max amplitude of 1
    wave /= np.max(np.abs(wave))

    return wave, sample_rate

def generate_stepped_sweep(start_freq, end_freq, num_freqs, amplitude, num_periods, sample_rate=44100):
    freqs = np.linspace(start_freq, end_freq, num_freqs)
    duration = sum([num_periods*(1/freq) for freq in freqs])
    print('Duration:', duration, 's')
    wave = np.zeros(int(sample_rate * duration))
    i = 0
    for freq in freqs:
        period = num_periods*(1/freq)
        period_samples = math.floor(period*sample_rate)
        wave[i:i+period_samples] = amplitude * np.sin(2*np.pi*freq*np.linspace(0, period, period_samples))
        i += period_samples
    return wave

def gen_step_sweep(start_freq, end_freq, interval, duration_per_freq=0.4, pause_duration=0.3, amplitude=1, sample_rate=44100):
    freqs = np.arange(start_freq, end_freq, interval)
    duration = duration_per_freq*len(freqs)
    signal_duration = duration_per_freq - pause_duration
    print('Duration:', duration, 's')
    wave = np.zeros(0) # Initialize an empty wave
    i = 0
    for freq in freqs:
    # Pause
        pause_samples = int(pause_duration * sample_rate)
        pause_wave = np.zeros(pause_samples)
        # Signal
        signal_samples = int(signal_duration * sample_rate)
        time_array = np.linspace(0, signal_duration, signal_samples)
        sine_wave = amplitude * np.sin(2 * np.pi * freq * time_array)
        # Apply windowing function for fade-in/fade-out
        window = windows.hann(signal_samples)  # You can use other window functions too
        windowed_sine_wave = sine_wave * window
        # Combine pause and signal
        freq_wave = np.concatenate([pause_wave, windowed_sine_wave])
        # Concatenate to the main wave
        wave = np.concatenate([wave, freq_wave])
    return wave

def play_wave(wave, sample_rate=44100):
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

# Analyze and plot Time, FFT, and PSD
def plot_signal_analysis(wave, acqu_sample_rate=2048):
    N = len(wave)
    T = 1.0 / acqu_sample_rate
    t = np.linspace(0.0, N * T, N, endpoint=False)

    # FFT
    yf = np.fft.fft(wave)
    xf = np.fft.fftfreq(N, T)
    xf = xf[:N//2]
    fft_mag = 2.0 / N * np.abs(yf[:N//2])

    # PSD using Welch
    f_psd, Pxx = welch(wave, fs=acqu_sample_rate, window='hann', nperseg=2048)

    # Plot
    plt.figure(figsize=(14, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t, wave)
    plt.title("Time Domain Signal")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")

    plt.subplot(3, 1, 2)
    plt.plot(xf, fft_mag)
    plt.title("FFT Magnitude Spectrum (Full Range)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.xlim(0, acqu_sample_rate / 2)

    plt.subplot(3, 1, 3)
    plt.semilogy(f_psd, Pxx)
    plt.title("Power Spectral Density (Welch, Full Range)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Power [V²/Hz]")
    plt.xlim(0, acqu_sample_rate / 2)

    plt.tight_layout()
    plt.show()


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

    sample_rate = 44100

    # wave = generate_sine_wave(100, 1, 0, 10, sample_rate)
    wave = generate_sine_sweep(20, 1000, 1, 20, sample_rate)
    # wave = generate_stepped_sweep(50, 1000, 990, 1, 20, sample_rate)
    # wave = gen_step_sweep(365, 375.1, 0.1)
    # wave = generate_random_signal(100, 150, 1, 5, sample_rate)
    # wave, sample_rate = generate_random_ifft_signal (100,150, 5, sample_rate, target_psd_level=1e-4)

    # Play the wave in a separate thread
    sound_thread = threading.Thread(target=play_wave, args=(wave, sample_rate))
    sound_thread.start()

    # Plot time, FFT, and PSD
    acqu_sample_rate = 2048
    plot_signal_analysis(wave, sample_rate)

    # plt.figure()
    # plt.plot(wave)
    # plt.show()
