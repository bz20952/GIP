from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import utils as u
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting module

plt.rcParams.update({
    'font.size': 18,
    'figure.figsize': (8, 5),
    'figure.dpi': 300
})

locations = ['0', 'l/4', 'l/2', '3l/4', 'l']

async def plot_acceleration(data: pd.DataFrame, options: dict):

    """
    Plot raw acceleration data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the acceleration data and corresponding time data.
    options : dict
        Dictionary containing the following keys:
            - 'accelerometers': A dictionary where keys are accelerometer names and values are booleans indicating
                                whether to include that accelerometer in the plot.
            - 'samplingFreq': The sampling frequency of the data.

    Returns
    -------
    str
        The file path where the plot image is saved.
    """

    accelerometers = options['accelerometers']

    for index, acc in enumerate(accelerometers.keys()):
        if accelerometers[acc]:
            plt.plot(data['t'], data[acc], label=acc)

    plot_path = f'./images/{u.format_accel_plot_name(options, "accel")}'
    
    plt.xlabel('Time [s]')
    plt.ylabel(r'Acceleration [g]')
    plt.title('Raw Acceleration Data')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    return plot_path


async def plot_forcing(data: pd.DataFrame, options: dict):
    
    """
    Plot raw forcing data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the forcing data and corresponding time data.
    options : dict
        Dictionary containing the following keys:
            - 'samplingFreq': The sampling frequency of the data.

    Returns
    -------
    str
        The file path where the plot image is saved.
    """

    plot_path = f'./images/{u.format_filename(options)}_{options['samplingFreq']}_force.png'

    plt.plot(data['t'], data['F0'])
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')
    plt.title('Raw Forcing Data')
    plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    return plot_path


async def plot_dft(data: pd.DataFrame, options: dict):

    """
    Plot the Discrete Fourier Transform of the acceleration data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the acceleration data and corresponding force data.
    options : dict
        Dictionary containing the following keys:
            - 'accelerometers': A dictionary where keys are accelerometer names and values are booleans indicating
                                whether to include that accelerometer in the plot.
            - 'samplingFreq': The sampling frequency of the data.

    Returns
    -------
    str
        The file path where the plot image is saved.
    """

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)
            f = f[:n//2]
            fft = np.abs(np.fft.fft(data[acc]))[:n//2]

            plt.scatter(f, fft/max(fft), s=10, label=acc)

    plot_path = f'./images/{u.format_accel_plot_name(options, "dft")}'

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Normalised amplitude')
    plt.title('Discrete Fourier Transform of Acceleration')
    plt.legend()
    plt.grid(True)
    plt.xlim(50, max(f))  # Set limits for the x-axis (frequency)
    plt.ylim(0, 1.1)  # Set limits for the y-axis (frequency)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5) 
    plt.close()          

    return plot_path


async def plot_nyquist(data: pd.DataFrame, options: dict):

    """
    Plot the Nyquist plot of the acceleration.
    This function generates a Nyquist plot for the given acceleration data using the provided options.
    The plot can be either 2D or 3D based on the commented/uncommented lines in the code.
    Parameters:
    data (pd.DataFrame): A DataFrame containing the acceleration data and corresponding force data.
                         The DataFrame should have columns for each accelerometer and corresponding force data.
    options (dict): A dictionary containing the following keys:
                    - 'accelerometers': A dictionary where keys are accelerometer names and values are booleans indicating
                                        whether to include that accelerometer in the plot.
                    - 'samplingFreq': The sampling frequency of the data.
    Returns:
    str: The file path where the plot image is saved.
    """

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']    

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')  # Create a 3D subplot

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)
            f = f[:n//2]
            fftacc = (np.fft.fft(data[acc]))[:n//2]
            fftforce = (np.fft.fft(data['F' + acc[1]]))[:n//2]
            frf = fftacc/fftforce
            frfReal = np.real(frf)
            frfImag = np.imag(frf)

            # ax.plot(f, frfReal, frfImag, label=acc) #3d plot
            plt.plot(frfReal, frfImag, label=acc) #2d plot


    # ax.set_xlim(150, 200)  # Set limits for the z-axis (Frequency) #3d plot
    # ax.set_ylim(y_min, y_max)  # Set limits for the x-axis (Real part) #3d plot
    # ax.set_zlim(z_min, z_max)  # Set limits for the y-axis (Imaginary part) #3d plot

    plot_path = f'./images/{u.format_accel_plot_name(options, "nyquist")}'

    # ax.set_ylabel('Re') #3d plot
    # ax.set_zlabel('Im') #3d plot
    # ax.set_xlabel('Frequency [Hz]') #3d plot
    # ax.set_title('Inertance Nyquist plot') #3d plot

    plt.xlabel('Re') #2d plot
    plt.ylabel('Im') #2d plot
    plt.title('Inertance Nyquist plot') #2d plot
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    return plot_path


async def plot_bode(data: pd.DataFrame, options: dict):

    """Plot the bode plot of the data."""

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc[1]])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function

            # Compute magnitude and phase
            magnitude = 20 * np.log10(np.abs(frf))  # Convert to dB
            phase = np.angle(frf, deg=True)  # Phase in degrees

            # Magnitude Plot
            plt.subplot(2, 1, 1)
            plt.semilogx(f, magnitude, label=acc)
            plt.xlim(50, max(f))
            plt.ylabel('Magnitude [dB]')
            plt.grid(True, which="both")

            # Phase Plot
            plt.subplot(2, 1, 2)
            plt.semilogx(f, phase, label=acc)
            plt.xlim(50, max(f))
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Phase [°]')
            plt.grid(True, which="both")

    # Add legends
    plt.subplot(2, 1, 1)
    plt.legend()
    plt.title('Inertance Bode Plot')

    # plt.subplot(2, 1, 2)
    # plt.legend()

    plot_path = f'./images/{u.format_accel_plot_name(options, "bode")}'
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.show()
    plt.close()

    return plot_path


def frf_matrix(data: pd.DataFrame, options: dict):

    """Plot the bode plot of the data."""

    fig, axes = plt.subplots(3, 3)

    for i, shaker_pos in enumerate([0, 2, 4]):
        options['shakerPosition'] = shaker_pos
        print(options)
        data = r.read_csv(options)
        for j, acc in enumerate(['A0', 'A2', 'A4']):
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/options['samplingFreq'])[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc[1]])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function)

            ax = axes[j,i]
            ax.plot(f, frf.imag)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlim(50, 1000)
            ax.set_ylim(-100, 100)

            if i == 0:
                ax.set_ylabel(acc)

            if j == 0:
                ax.set_title(shaker_pos)

            # # Magnitude Plot
            # plt.subplot(2, 1, 1)
            # plt.semilogx(f, magnitude, label=acc)
            # plt.xlim(1, max(f))
            # plt.ylabel('Magnitude [dB]')
            # plt.grid(True, which="both")

    # plt.subplot(2, 1, 2)
    # plt.legend()

    plt.show()

async def plot_imaginary_r(data: pd.DataFrame, options: dict) -> None:
              #Extract data
    for acc in accelerometers.keys():
        if accelerometers[acc]:
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            sample_rate = 1 / (data['t'][1] - data['t'][0])
            f = np.fft.fftfreq(n, 1/sample_rate)[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc[1]])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function
    
    freqs = f
    # Convert inertance to receptance
    omega = 2 * np.pi * freqs  # Convert frequency to angular frequency (rad/s)
    frf_r = frf / (-omega**2)  # Convert inertance to receptance
    
    # Avoid division by zero at zero frequency
    frf_r[omega == 0] = np.inf

    abs_frf = np.abs(frf_r)

    i_frf_r0 = np.imag(frf_r[0])
    i_frf_r1 = np.imag(frf_r[1])
    i_frf_r2 = np.imag(frf_r[2])

    # Find peaks in the absolute FRF
    peaks, _ = find_peaks(abs_frf, prominence=20)  # Adjust threshold as needed

    im_values = [i_frf_r0[peaks], i_frf_r1[peaks], i_frf_r2[peaks]]
    x_locations = [0, 0.5, 1]  # Normalized locations of the accelerometers

    # Remove the line between points and plot only the points
    plt.scatter(x_locations, im_values, color='red', s=100, label='Imaginary FRF at Natural Frequency')

    # Add vertical lines from the x-axis to each point
    for loc, val in zip(x_locations, im_values):
        plt.plot([loc, loc], [0, val], color='blue', linestyle='--', linewidth=1.5)

    # Center the graph around the x-axis
    plt.axhline(0, color='black', linewidth=1)  # Add a horizontal line at y=0
    plt.ylim(-1.1 * np.max(np.abs(im_values)), 1.1 * np.max(np.abs(im_values)))  # Symmetrical y-axis

    # Add labels and title
    plt.xlabel('Accelerometer Location (Normalized)')
    plt.ylabel('Imaginary Part of FRF')
    plt.title('Imaginary FRF at Natural Frequency for Three Accelerometers')
    plt.xticks(x_locations, ['Start (0)', 'Middle (0.5)', 'End (1)'])  # Label x-axis with locations
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()

    plot_path = f'./images/{u.format_accel_plot_name(options, "imaginary")}'
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)

    return plot_path

async def plot_argand_r(data: pd.DataFrame, options: dict) -> None:
          #Extract data
    for acc in accelerometers.keys():
        if accelerometers[acc]:
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            sample_rate = 1 / (data['t'][1] - data['t'][0])
            f = np.fft.fftfreq(n, 1/sample_rate)[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc[1]])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function
    
    freqs = f
    # Convert inertance to receptance
    omega = 2 * np.pi * freqs  # Convert frequency to angular frequency (rad/s)
    frf_r = frf / (-omega**2)  # Convert inertance to receptance
    
    # Avoid division by zero at zero frequency
    frf_r[omega == 0] = np.inf

    abs_frf = np.abs(frf_r)

    frf_r0 = frf_r[0]
    frf_r1 = frf_r[1]
    frf_r2 = frf_r[2]
    
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(6, 9), sharex=True)

    # Find peaks in the absolute FRF
    peaks, _ = find_peaks(abs_frf, prominence=20)  # Adjust threshold as needed

    # Extract values at peaks
    arg = []
    for i in range(len(peaks)):  # Loop through all peaks
        arg_i = np.array([frf_r0[peaks[i]], frf_r1[peaks[i]], frf_r2[peaks[i]]])
        arg.append(arg_i)

    # Convert list of arrays into a single NumPy array for easier processing
    arg = np.array(arg)

    # Determine the number of rows in arg
    num_rows = arg.shape[0]

    # Create a vertical subplot based on the number of rows in arg
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, figsize=(6, 4 * num_rows), sharex=True, sharey=True)

    # If there's only one row, axs will not be an array, so we convert it to a list for consistency
    if num_rows == 1:
        axs = [axs]

    # Plot each row of arg in a separate subplot
    for i, ax in enumerate(axs):
        point = arg[i]  # Get the i-th row of arg
    
    colors = ['r', 'g', 'b']  # Colors for each point in the row

    # Plot the Argand diagram for this row
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title(f'Argand Diagram - Peak {i+1}')

    for j, p in enumerate(point):
        color = colors[j % len(colors)]  # Cycle through colors
        # Plot the point
        ax.scatter(p.real, p.imag, color=color, s=50, label=f'Point {j+1}')
        # Draw a line from the origin to the point
        ax.plot([0, p.real], [0, p.imag], color=color, linestyle='-', linewidth=2)
        # Add text label for the point
        ax.text(p.real, p.imag, f' ({p.real:.2f}, {p.imag:.2f})', fontsize=10, color=color)

    ax.legend()

    plt.tight_layout()
    plt.legend()
    plt.show()
    plot_path = f'./images/{u.format_accel_plot_name(options, "argand")}'
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    
    return plot_path

if __name__ == '__main__':
    import json
    import asyncio
    import reader as r
    with open('./templates/requestFormat.json') as f:
        options = json.load(f)
    data = r.read_csv(options)
    asyncio.run(plot_argand_r(data, options))
    asyncio.run(plot_imaginary_r(data, options))
