from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


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


def plot_acceleration(data: pd.DataFrame, options: dict):

    """Plot raw acceleration data."""

    accelerometers = options['accelerometers']

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            plt.plot(data['t'], data[acc], label=acc)
    
    plt.xlabel('Time [s]')
    plt.ylabel(r'Acceleration [m/s$^2$]')
    plt.title('Raw Acceleration Data')
    plt.legend()
    plt.grid(True)
    plt.savefig('raw_acceleration.png')


def plot_forcing(data: pd.DataFrame):
    
    """Plot raw forcing data."""

    plt.plot(data['t'], data['F'])
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')
    plt.title('Raw Forcing Data')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    import reader as r
    data = r.read_csv('FREE_400_5')
    plot_forcing(data)
    # plot_acceleration(data, {
    #     '0': True,
    #     'l/4': False,
    #     'l/2': False,
    #     '3l/4': False,
    #     'l': True
    # })