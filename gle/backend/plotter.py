from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import utils as u
# from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting module
from adjustText import adjust_text
from scipy.signal import find_peaks
 

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
    plt.xlim(0, max(f))  # Set limits for the x-axis (frequency)
    plt.ylim(0, 1.1)  # Set limits for the y-axis (frequency)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5) 
    plt.close()          

    return plot_path


async def plot_nyquist(data: pd.DataFrame, options: dict):

    """ Plot the Nyquist plot of the acceleration.
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

    # Filter for desired frequency range
    f_min=max(options['lowerCutoff'], 10)
    f_max=min(options['upperCutoff'], 1000)

    for acc in accelerometers.keys():
        if accelerometers[acc]:
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/sample_rate)
            f = f[:n//2]
            # u.accel_to_disp(data[acc], options)
            # fftvel=(np.fft.fft(data[acc]))[:n//2]
            fftacc = (np.fft.fft(data[acc]))[:n//2]
            fftforce = (np.fft.fft(data['F' + acc[1]]))[:n//2]
            frf = fftacc/fftforce
            frf_mobility = frf/(1j*f*2*np.pi)
            frf = frf_mobility #uncomment this line if plotting inertance
            frfReal = -np.real(frf)
            frfImag = np.imag(frf)

            # Filter for desired frequency range (depends on question that we ask i.e. damping ratio at 2nd mode for e.g.)
            valid_idx = (f >= f_min) & (f <= f_max)
            f_filtered=f[valid_idx]
            frfReal_filtered = frfReal[valid_idx]
            frfImag_filtered = frfImag[valid_idx]

            plotcircfit(frfReal_filtered, frfImag_filtered, f_filtered)  # Correct usage
            plot_path = f'./images/{u.format_accel_plot_name(options, "nyquist")}'
            plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
            plt.close()
            break  # Only plot for first accelerometer

    return plot_path


def plotcircfit(x,y,z):

    """
    Fit X-Y data to a circle and create a plot.

    Parameters:
    - x: 1-D array (list or NumPy array) of X data
    - y: 1-D array (list or NumPy array) of Y data
    - z: 1-D array (list or NumPy array) of Y data
    """

    # Compute circle fit
    r, xc, yc, RMSE = u.circfit(x, y)
    
    # Find upper and lower indices for theta
    theta_n_index = np.argmax(x)
    theta_h_index = u.closest_index(yc+r, y)
    theta_l_index = u.closest_index(yc-r, y)

    # Create figure
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.set_aspect('equal')

    # Plot circle fit
    circle = plt.Circle((xc, yc), r, color='k', fill=False, linewidth=2, label='Fitted Circle')
    ax.add_patch(circle)

    # Plot original data
    ax.plot(x, y, 'bo-', label='Data Points', markersize=5)
    ax.plot(x[0], y[0], 'go', label='Start Point', markersize=5)  # First point (green)
    ax.plot(x[-1], y[-1], 'ro', label='End Point', markersize=5)  # Last point (red)
    # ax.plot(xc, yc, 'ko', label='Circle Center: 'f'Radius={r:.2f}, 'f'Coordinates=({xc:.2f}, {yc:.2f})', markersize=5)  # Circle center (black)
    ax.plot(xc, yc, 'ko', label=f'Circle Center (Radius={r:.2f})', markersize=5)  # Circle center (black)

    # Annotate labels
    txts = []
    label_indices = np.array([theta_n_index, theta_l_index, theta_h_index])
    for i in label_indices:
        txt = plt.text(x[i]*0.65, y[i]*0.65, f"f = {z[i]:.2f} Hz", color='k') # text for coordinates and frequency of data point
        txts.append(txt)

    adjust_text(txts, target_x=x[label_indices], target_y=y[label_indices], arrowprops=dict(arrowstyle="->", color='black', lw=3))

    # Labels & Title
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title(f'Mobility Nyquist plot')
    plt.legend(bbox_to_anchor=(2, 1))
    plt.grid(True)

    # # Annotate radius
    # radiustexts=[]
    # radiustexts.append(plt.text(xc, yc+0.05, f'Radius = {r:.5f}', fontsize=10))
    # radiustexts.append(plt.text(xc, yc-0.05,f"({xc:.2f}, {yc:.2f})", fontsize=10))
    # adjust_text(radiustexts) #arrowprops=dict(arrowstyle="->", color='gray', lw=1)) 
    
    # # Find sweep rates of all data points
    # sweep_rate=np.zeros(len(x-1))
    # for i in range(len(x)-1):
    
    #     # find sweep angle between data points
    #     vec1= np.array([x[i]-xc, y[i]-yc])
    #     vec2= np.array([x[i+1]-xc, y[i+1]-yc])
    #     dot_product= np.dot(vec1, vec2)
    #     mag1= np.linalg.norm(vec1)
    #     mag2= np.linalg.norm(vec2)
    #     cos_theta= dot_product / (mag1 * mag2)
    #     theta_rad= np.arccos(cos_theta)
    #     theta_deg= np.degrees(theta_rad)

    #     #find freqeuncy change between data points
    #     freq_change= z[i+1]-z[i]
        
    #     # update sweep rate array
    #     sweep_rate[i]=theta_deg/freq_change

    # # Find maximum sweep rate
    # idx_max_sweep_rate = np.argmax(sweep_rate)
    # idx1_of_data_points_surrounding_maximum_sweep_rate=idx_max_sweep_rate
    # idx2_of_data_points_surrounding_maximum_sweep_rate=idx_max_sweep_rate+1

    # # Annotate labels
    # data_points_used=1
    # texts=[]
    # for i in range(idx1_of_data_points_surrounding_maximum_sweep_rate-data_points_used,idx2_of_data_points_surrounding_maximum_sweep_rate+data_points_used+1):
    #     # txt = plt.text(x[i] + 0.05, y[i], f"({x[i]:.2f}, {y[i]:.2f},{z[i]:.2f})", color='k') # text for coordinates and frequency of data point
    #     txt = plt.text(x[i] + 0.05, y[i], f"({z[i]:.2f})", color='k') # text for coordinates and frequency of data point
    #     texts.append(txt)

    # # Adjust text labels to prevent overlap
    # adjust_text(texts, arrowprops=dict(arrowstyle="->", color='gray', lw=1))

    
async def plot_bode(data: pd.DataFrame, options: dict):

    """Plot the bode plot of the data."""

    accelerometers = options['accelerometers']
    sample_rate = options['samplingFreq']

    # Filter for desired frequency range
    f_min=max(options['lowerCutoff'], 10)
    f_max=min(options['upperCutoff'], 1000)

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
            frf_mobility = frf/(1j*f*2*np.pi)
            frf = frf_mobility

            # Compute magnitude and phase
            magnitude = 20 * np.log10(np.abs(frf))  # Convert to dB
            phase = np.angle(frf, deg=True)  # Phase in degrees

            valid_idx = (f >= f_min) & (f <= f_max)
            f_filtered = f[valid_idx]
            magnitude_filtered = magnitude[valid_idx]
            phase_filtered = phase[valid_idx]

            # Find peak magnitude and corresponding frequency
            peak_mag = np.max(magnitude_filtered)
            idx_peak = np.argmax(magnitude_filtered)
            f_n = f_filtered[idx_peak]

            # Find Half-Power (-3 dB) Magnitude
            half_power_mag = peak_mag - 3  # -3 dB point
            
            # Find first index to the left of peak where magnitude drops to or below -3 dB
            # Search backwards from the peak index
            try:
                idx_f1 = np.where(magnitude_filtered[:idx_peak] <= half_power_mag)[0][-1]  # First index to the left
            except IndexError:
                continue

            # Find first index to the right of peak where magnitude drops to or below -3 dB
            # Search forwards from the peak index
            try:
                idx_f2 = np.where(magnitude_filtered[idx_peak:] <= half_power_mag)[0][0] + idx_peak  # First index to the right
            except IndexError:
                continue

            # Get corresponding frequency values
            f1 = f_filtered[idx_f1]
            f2 = f_filtered[idx_f2]

            # Magnitude Plot
            plt.subplot(2, 1, 1)
            plt.title('Mobility Bode Plot')
            plt.plot(f_filtered, magnitude_filtered, label=acc)
            plt.ylabel('Magnitude [dB]')
            plt.grid(True, which="both")

            # Annotate Bode Plot with vertical lines 
            plt.axvline(f_n, color='red', linestyle='--')  # Vertical line at peak frequency
            # plt.text(f_n, peak_mag+2, f'Peak: {f_n:.2f} Hz', color='red', fontsize=8, verticalalignment='bottom', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round4', pad=0.5))
            plt.axvline(f1, color='black', linestyle='--')  # Vertical line at f1
            # plt.text(f1, magnitude_filtered[idx_f1]+2, f'f1: {f1:.2f} Hz', color='blue', fontsize=8, verticalalignment='bottom', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round4', pad=0.5))
            plt.axvline(f2, color='black', linestyle='--')  # Vertical line at f2
            # plt.text(f2, magnitude_filtered[idx_f2]+2, f'f2: {f2:.2f} Hz', color='blue', fontsize=8, verticalalignment='bottom', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round4', pad=0.5))
             
            # Text labels
            text_objects = []
            text_objects.append(plt.text(f_n, peak_mag+2, f'Peak: {f_n:.2f} Hz', color='red', verticalalignment='bottom', horizontalalignment='center'))
            text_objects.append(plt.text(f1, magnitude_filtered[idx_f1]+2, f'f1: {f1:.2f} Hz', color='black', verticalalignment='bottom', horizontalalignment='center'))
            text_objects.append(plt.text(f2, magnitude_filtered[idx_f2]+2, f'f2: {f2:.2f} Hz', color='black', verticalalignment='bottom', horizontalalignment='center'))

            # Use adjustText to automatically adjust text positions to avoid overlap
            adjust_text(text_objects) #arrowprops=dict(arrowstyle="->", color='grey', lw=1))
            # only_move={'points', 'text'}, arrowprops=dict(arrowstyle="->", color='gray', lw=0.5))

            # Phase Plot
            plt.subplot(2, 1, 2)
            plt.plot(f_filtered, phase_filtered, label=acc)
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Phase [°]')
            plt.grid(True, which="both")

    plot_path = f'./images/{u.format_accel_plot_name(options, "bode")}'
    plt.legend()
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
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
    
    """
    Plot the imaginary part of the Frequency Response Function (FRF) at the natural frequency.

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

    frfs = []
    peaks = []
    for acc in accelerometers.keys():
        if accelerometers[acc]:
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            f = np.fft.fftfreq(n, 1/options['samplingFreq'])[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc[1]])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function

            # Convert inertance to receptance
            omega = 2 * np.pi * f  # Convert frequency to angular frequency (rad/s)
            frf_r = frf / (-omega**2)  # Convert inertance to receptance

            # Find peaks in the absolute FRF
            gains = np.abs(frf_r)
            plt.plot(f, gains)
            plt.show()
            peak, _ = find_peaks(gains, prominence=10)  # Adjust threshold as needed
            print(peak)
            peaks.append(peak)

            frfs.append(frf)

    # Convert list to array
    frfs = np.array(frfs)

    # # Avoid division by zero at zero frequency
    # frf_r[omega == 0] = np.inf

    im_values = []
    for accelerometer in range(np.shape(frfs)[0]):
        im_values.append(frfs[accelerometer, peaks[accelerometer]].imag)
    
    # Normalized locations of the accelerometers
    x_locations = [0, 0.5, 1]

    # Remove the line between points and plot only the points
    plt.scatter(x_locations, im_values, color='red', s=100, label='Imaginary FRF at Natural Frequency')

    # Add vertical lines from the x-axis to each point
    for loc, val in zip(x_locations, im_values):
        plt.plot([loc, loc], [0, val], color='blue', linestyle='--', linewidth=1.5)

    # Center the graph around the x-axis
    plt.axhline(0, color='black', linewidth=1)  # Add a horizontal line at y=0
    plt.ylim(-1.1 * np.max(np.abs(im_values)), 1.1 * np.max(np.abs(im_values)))  # Symmetrical y-axis

    # Add labels and title
    plt.xlabel('Accelerometer Location')
    plt.ylabel('Imaginary Component of FRF')
    plt.title('Mode shapes')
    plt.xticks(x_locations, ['Start (0)', 'Middle (l/2)', 'End (l)'])  # Label x-axis with locations
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()

    plot_path = f'./images/{u.format_accel_plot_name(options, "imaginary")}'
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)

    return plot_path


async def plot_argand_r(data: pd.DataFrame, options: dict) -> None:

    accelerometers = options['accelerometers']
    
    frfs = []
    for acc in accelerometers.keys():
        if accelerometers[acc]:
            # Compute FFT and Frequency Response Function
            n = len(data[acc])
            freqs = np.fft.fftfreq(n, 1/options['samplingFreq'])[:n//2]  # Positive frequencies
            fftacc = np.fft.fft(data[acc])[:n//2]
            fftforce = np.fft.fft(data['F' + acc[1]])[:n//2]

            # Avoid division by zero
            fftforce[np.abs(fftforce) < 1e-10] = np.finfo(float).eps
            frf = fftacc / fftforce  # Frequency Response Function
            frfs.append(frf)
    
    # Convert list to array
    frfs = np.array(frfs)

    # Convert inertance to receptance
    omega = 2 * np.pi * freqs  # Convert frequency to angular frequency (rad/s)
    receptance_frf = frfs / (-omega**2)  # Convert inertance to receptance
    abs_frf = np.abs(receptance_frf)
    num_rows = np.shape(abs_frf)[0]
    
    # # Avoid division by zero at zero frequency
    # frf_r[omega == 0] = np.inf

    # Extract values at peaks
    arg = []
    for i in range(num_rows):  # Loop through all peaks
        # Find peaks in the absolute FRF
        peaks, _ = find_peaks(abs_frf[i,:], prominence=1)  # Adjust threshold as needed
        print(peaks)
        arg_i = np.array([abs_frf[j,:][peaks[i]] for j in range(num_rows)])
        arg.append(arg_i)

    # Convert list of arrays into a single NumPy array for easier processing
    arg = np.array(arg)

    # Create a vertical subplot based on the number of rows in arg
    fig, axs = plt.subplots(nrows=num_rows, ncols=1, figsize=(6, 4 * num_rows), sharex=True, sharey=True)

    # If there's only one row, axs will not be an array, so we convert it to a list for consistency
    if num_rows == 1:
        axs = [axs]

    # Plot each row of arg in a separate subplot
    for i, ax in enumerate(axs):
        point = arg[i,:]  # Get the i-th row of arg
    
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

    # ax.legend()

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
    asyncio.run(plot_dft(data, options))
    asyncio.run(plot_nyquist(data, options))
    asyncio.run(plot_bode(data, options))
    # asyncio.run(plot_imaginary_r(data, options))
    # asyncio.run(plot_argand_r(data, options))
