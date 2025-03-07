from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import utils as u
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting module

plt.rcParams.update({
    'font.size': 18,
    'figure.figsize': (8, 5),
    'figure.dpi': 120
})

def plot_acceleration(data: pd.DataFrame, options: dict):

    """Plot raw acceleration data."""

    accelerometers = options['accelerometers']
    file_suffix = ''

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            file_suffix += f'_{acc}'
            plt.plot(data['t'], data[acc], label=acc)

    plot_path = f'./images/{u.format_filename(options)}_{options['samplingFreq']}_accel{file_suffix}.png'
    
    plt.xlabel('Time [s]')
    plt.ylabel(r'Acceleration [m/s$^2$]')
    plt.title('Raw Acceleration Data')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    return plot_path

def plot_forcing(data: pd.DataFrame, options: dict):
    
    """Plot raw forcing data."""

    plot_path = f'./images/{u.format_filename(options)}_{options['samplingFreq']}_force.png'

    plt.plot(data['t'], data['FA_0'])
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')
    plt.title('Raw Forcing Data')
    plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

def plot_dft(data: pd.DataFrame, options: dict):

    """Plot the Discrete Fourier Transform of the acceleration data."""

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']
    file_suffix = '' 

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            file_suffix += f'_{acc}'
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)
            f = f[:n//2]
            fft = np.abs(np.fft.fft(data[acc]))[:n//2]

            plt.scatter(f, fft, s=10, label=acc)

    plot_path = f'./images/{u.format_filename(options)}_{options['samplingFreq']}_dft{file_suffix}.png'

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title('Discrete Fourier Transform of Acceleration')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, (max(f)))  # Set limits for the x-axis (frequency)
    plt.ylim(0, (max(fft[100:])*1.2))  # Set limits for the y-axis (frequency)
    plt.savefig(plot_path) 
    plt.close()          

    return plot_path

def plot_nyquist(data: pd.DataFrame, options: dict):

    """Plot the Nyquist plot of the acceleration."""

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']
    file_suffix = ''    

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  # Create a 3D subplot

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            file_suffix += f'_{acc}'
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)
            f = f[:n//2]
            fftacc = (np.fft.fft(data[acc]))[:n//2]
            fftforce = (np.fft.fft(data['F' + acc]))[:n//2]
            frf = fftacc/fftforce
            frfReal = np.real(frf)
            frfImag = np.imag(frf)

            ax.plot(f, frfReal, frfImag, label=acc) #3d plot
            # plt.plot(frfReal, frfImag, label=acc) #2d plot


    # ax.set_xlim(150, 200)  # Set limits for the z-axis (Frequency) #3d plot
    # ax.set_ylim(y_min, y_max)  # Set limits for the x-axis (Real part) #3d plot
    # ax.set_zlim(z_min, z_max)  # Set limits for the y-axis (Imaginary part) #3d plot

    plot_path = f'./images/{u.format_filename(options)}_{options['samplingFreq']}_nyquist{file_suffix}.png'

    ax.set_ylabel('Re') #3d plot
    ax.set_zlabel('Im') #3d plot
    ax.set_xlabel('Frequency [Hz]') #3d plot
    ax.set_title('Inertance Nyquist plot') #3d plot

    # plt.xlabel('Re') #2d plot
    # plt.ylabel('Im') #2d plot
    # plt.title('Inertance Nyquist plot') #2d plot
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.close()

    return plot_path

def plot_bode(data: pd.DataFrame, options: dict):

    """Plot the bode plot of the data."""

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']
    file_suffix = '' 

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            file_suffix += f'_{acc}'
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function

            # Compute magnitude and phase
            magnitude = 20 * np.log10(np.abs(frf))  # Convert to dB
            phase = np.angle(frf, deg=True)  # Phase in degrees

            # Magnitude Plot
            plt.subplot(2, 1, 1)
            plt.semilogx(f, magnitude, label=f'Accelerometer {acc}')
            plt.ylabel('Magnitude [dB]')
            plt.grid(True, which="both")

            # Phase Plot
            plt.subplot(2, 1, 2)
            plt.semilogx(f, phase, label=f'Accelerometer {acc}')
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Phase [°]')
            plt.grid(True, which="both")

    # Add legends
    plt.subplot(2, 1, 1)
    plt.legend()
    plt.title('Bode Plot (Frequency Response)')

    plt.subplot(2, 1, 2)
    plt.legend()

    plot_path = f'./images/{u.format_filename(options)}_{options['samplingFreq']}_bode{file_suffix}.png'
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.show()
    plt.close()

    return plot_path

if __name__ == '__main__':
    import reader as r
    options = {
        'excitationType': 'SINE_SWEEP',
        'accelerometers': {
            'A_1': True,
            'A_2': False,
            'A_3': False,
            'A_4': False,
            'A_5': False
        },
        'samplingFreq': 2048,
        'shakerPosition': '0',
    }
    data = r.read_csv(options)
    # plot_acceleration(data, options)
    # plot_forcing(data, options)
    plot_dft(data, options)
    plot_nyquist(data, options)
    plot_bode(data, options)