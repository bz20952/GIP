import numpy as np
import sounddevice as sd

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

def play_wave(wave, sample_rate=44100):
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

if __name__ == "__main__":
    frequency = float(input("Enter the frequency of the sine wave (Hz): "))
    amplitude = float(input("Enter the amplitude of the sine wave: "))
    phase = float(input("Enter the phase of the sine wave (radians): "))
    duration = float(input("Enter the duration of the sine wave (seconds): "))

    # wave = generate_sine_wave(frequency, amplitude, phase, duration)
    # wave = generate_sine_sweep(20, 200, amplitude, duration)
    wave = generate_random_signal(amplitude, duration)
    play_wave(wave)