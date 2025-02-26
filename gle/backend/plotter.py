from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import utils as u
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting module


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

    plot_path = f'./images/{u.format_filename(options)}_accel.png'
    
    plt.xlabel('Time [s]')
    plt.ylabel(r'Acceleration [m/s$^2$]')
    plt.title('Raw Acceleration Data')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path)

    return plot_path


def plot_forcing(data: pd.DataFrame, options: dict):
    
    """Plot raw forcing data."""

    plt.plot(data['t'], data['F'])
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')
    plt.title('Raw Forcing Data')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'./images/{u.format_filename(options)}_forcing.png')


def plot_dft(data: pd.DataFrame, options: dict):

    """Plot the Discrete Fourier Transform of the acceleration data."""

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)
            f = f[:n//2]
            fft = np.abs(np.fft.fft(data[acc]))[:n//2]

            plt.plot(f, fft, label=acc)

    plot_path = f'./images/{u.format_filename(options)}_dft.png'

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title('Discrete Fourier Transform of Acceleration')
    plt.legend()
    plt.grid(True)
    plt.ylim(0, (max(f)))  # Set limits for the x-axis (frequency)
    plt.ylim(0, (max(fft[100:])*1.2))  # Set limits for the y-axis (frequency)
    plt.savefig(plot_path) 
    plt.close()          

    return plot_path


def plot_nyquist(data: pd.DataFrame, options: dict):

    """Plot the Nyquist plot of the acceleration."""

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')  # Create a 3D subplot

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)
            # f = f[:n//2]
            f = f[:5000]
            fftacc = (np.fft.fft(data[acc]))[:5000]
            fftforce = (np.fft.fft(data['F']))[:5000]
            frf = fftacc/fftforce
            frfReal = np.real(frf)
            frfImag = np.imag(frf)

            # ax.scatter(f, frfReal, frfImag, label=acc)
            plt.scatter(frfReal, frfImag, label=acc)


    # ax.set_xlim(150, 200)  # Set limits for the z-axis (Frequency)
    # # ax.set_ylim(y_min, y_max)  # Set limits for the x-axis (Real part)
    # # ax.set_zlim(z_min, z_max)  # Set limits for the y-axis (Imaginary part)

    plot_path = f'./images/{u.format_filename(options)}_nyquist.png'

    # ax.set_ylabel('Re')
    # ax.set_zlabel('Im')
    # ax.set_xlabel('Frequency [Hz]')
    # ax.set_title('Inertance Nyquist plot')

    # plt.xlabel('Re')
    # plt.ylabel('Im')
    # plt.title('Inertance Nyquist plot')
    plt.legend()
    plt.grid(True)
    plt.show()
    # plt.close()          

    return plot_path


if __name__ == '__main__':
    import reader as r
    options = {
        'excitationType': 'random',
        'accelerometers': {
            '0': True,
            'l/4': False,
            'l/2': False,
            '3l/4': False,
            'l': False
        },
        'samplingFreq': 2048,
        'shakerPosition': 5,
    }
    data = r.read_csv(options)
    # plot_dft(data, options)
    plot_nyquist(data, options)