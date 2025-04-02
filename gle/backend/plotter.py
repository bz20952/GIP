from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import utils as u
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting module
from scipy.signal import find_peaks
from scipy.fft import rfft,rfftfreq
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

            plt.scatter(f, fft, s=10, label=acc)

    plot_path = f'./images/{u.format_accel_plot_name(options, "dft")}'

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title('Discrete Fourier Transform of Acceleration')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 1000)  # Set limits for the x-axis (frequency)
    # plt.ylim(0, 1.1)  # Set limits for the y-axis (frequency)
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()          

    return plot_path


async def plot_nyquist(data: pd.DataFrame, options: dict, plot_type: str = 'Mobility'):

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
            fftacc = (np.fft.fft(data[acc]))[:n//2]
            fftforce = (np.fft.fft(data['F' + acc[1]]))[:n//2]
            frf = fftacc/fftforce

            # Adjust the frf depending on desired plot type
            if plot_type == 'Mobility':
                frf_mobility = frf/(1j*f*2*np.pi)  # Convert inertance to mobility
                frf = frf_mobility
            elif plot_type == 'Receptance':
                frf_receptance = frf/-((f*2*np.pi)**2)  # Convert inertance to receptance
                frf = frf_receptance

            frfReal = np.real(frf)
            frfImag = np.imag(frf)

            # Filter for desired frequency range (depends on question that we ask i.e. damping ratio at 2nd mode for e.g.)
            valid_idx = (f >= f_min) & (f <= f_max)
            f_filtered=f[valid_idx]
            frfReal_filtered = frfReal[valid_idx]
            frfImag_filtered = frfImag[valid_idx]

            xc, yc, r = plotcircfit(frfReal_filtered, frfImag_filtered, f_filtered)  # Correct usage
            break  # Only plot for first accelerometer

    # Labels & Title
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title(f'Mobility Nyquist plot ({acc})')
    plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim((xc - r)*1.1, (xc + r)*1.1)
    plt.ylim((yc - r)*1.1, (yc + r)*1.1)
    plt.grid(True)

    plot_path = f'./images/{u.format_accel_plot_name(options, "nyquist")}'
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    # plt.show()
    plt.close()

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
    theta_n_index = np.argmax(np.abs(x))
    theta_h_index = u.closest_index(yc+r, y)
    theta_l_index = u.closest_index(yc-r, y)

    # # Create figure
    # fig, ax = plt.subplots(figsize=(20, 6))
    # ax.set_aspect('equal')

    # Plot circle fit
    circle = plt.Circle((xc, yc), r, color='k', fill=False, linewidth=2, label='Fitted Circle')
    plt.gca().add_artist(circle)

    # Plot original data
    plt.plot(x, y, 'bo-', label='Data Points', markersize=5)
    plt.plot(x[0], y[0], 'go', label='Start Point', markersize=5)  # First point (green)
    plt.plot(x[-1], y[-1], 'ro', label='End Point', markersize=5)  # Last point (red)
    plt.plot(xc, yc, 'ko', label=f'Circle Center (Radius={r:.2f})', markersize=5)  # Circle center (black)

    # Annotate labels
    txts = []
    label_indices = np.array([theta_n_index, theta_l_index, theta_h_index])
    for i in label_indices:
        if i == theta_n_index:
            txt = plt.text(x[i], y[i]*0.65, f"Resonant frequency = {z[i]:.2f} Hz", color='k') # text for coordinates and frequency of data point
        else:
            txt = plt.text(x[i], y[i]*0.65, f"Half-power frequency = {z[i]:.2f} Hz", color='k')
        txts.append(txt)

    adjust_text(txts, target_x=x[label_indices], target_y=y[label_indices], arrowprops=dict(arrowstyle="->", color='black', lw=3))

    # # Labels & Title
    # plt.xlabel('Real')
    # plt.ylabel('Imaginary')
    # plt.title(f'Mobility Nyquist plot')
    # plt.legend(loc='center left')
    # plt.grid(True)

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

    return xc, yc, r

    
async def plot_bode(data: pd.DataFrame, options: dict, plot_type: str = 'Mobility'):

    """
    Plot the Bode plot of the acceleration data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the acceleration data and corresponding force data.
    options : dict
        Dictionary containing the following keys:
            - 'accelerometers': A dictionary where keys are accelerometer names and values are booleans indicating
                                whether to include that accelerometer in the plot.
            - 'samplingFreq': The sampling frequency of the data.
    plot_type : str, optional
        Type of plot to generate. Options are 'Mobility' or 'Receptance'.

    Returns
    -------
    str
        The file path where the plot image is saved.
    """
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
            frf = fftacc / fftforce  # Intertance Frequency Response Function
            
            # Adjust the frf depending on desired plot type
            if plot_type == 'Mobility':
                frf_mobility = frf/(1j*f*2*np.pi)  # Convert inertance to mobility
                frf = frf_mobility
            elif plot_type == 'Receptance':
                frf_receptance = frf/-((f*2*np.pi)**2)  # Convert inertance to receptance
                frf = frf_receptance

            # plt.scatter(f, np.abs(fftforce))
            # plt.show()
            # plt.close()

            # Compute magnitude and phase
            magnitude = 20 * np.log10(np.abs(frf))  # Convert to dB
            phase = np.angle(frf)

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

            # Magnitude Plot
            plt.subplot(2, 1, 1)
            # plt.title(f'{plot_type} Bode plot')
            plt.plot(f_filtered, magnitude_filtered, label=acc)
            plt.ylabel('Gain [dB]')
            plt.grid(True, which="both")

            text_objects = []
            
            # # Find first index to the left of peak where magnitude drops to or below -3 dB
            # # Search backwards from the peak index
            # try:
            #     idx_f1 = np.where(magnitude_filtered[:idx_peak] <= half_power_mag)[0][-1]  # First index to the left
            # except IndexError:
            #     pass
            # else:
            #     f1 = f_filtered[idx_f1]
            #     text_objects.append(plt.text(f1, magnitude_filtered[idx_f1]+2, f'f1: {f1:.2f} Hz', color='black', verticalalignment='bottom', horizontalalignment='center'))
            #     plt.axvline(f1, color='black', linestyle='--')  # Vertical line at f1

            # # Find first index to the right of peak where magnitude drops to or below -3 dB
            # # Search forwards from the peak index
            # try:
            #     idx_f2 = np.where(magnitude_filtered[idx_peak:] <= half_power_mag)[0][0] + idx_peak  # First index to the right
            # except IndexError:
            #     pass
            # else:
            #     f2 = f_filtered[idx_f2]
            #     text_objects.append(plt.text(f2, magnitude_filtered[idx_f2]-5, f'f2: {f2:.2f} Hz', color='black', verticalalignment='bottom', horizontalalignment='center'))
            #     plt.axvline(f2, color='black', linestyle='--')  # Vertical line at f2

            # # Annotate Bode Plot with vertical lines 
            # plt.axvline(f_n, color='red', linestyle='--')  # Vertical line at peak frequency
            # plt.text(f_n, peak_mag+2, f'Peak: {f_n:.2f} Hz', color='red', fontsize=8, verticalalignment='bottom', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round4', pad=0.5))
            # plt.text(f1, magnitude_filtered[idx_f1]+2, f'f1: {f1:.2f} Hz', color='blue', fontsize=8, verticalalignment='bottom', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round4', pad=0.5))
            # plt.text(f2, magnitude_filtered[idx_f2]+2, f'f2: {f2:.2f} Hz', color='blue', fontsize=8, verticalalignment='bottom', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round4', pad=0.5))
             
            # # Text labels
            # text_objects.append(plt.text(f_n, peak_mag+2, f'Peak: {f_n:.2f} Hz', color='red', verticalalignment='bottom', horizontalalignment='center'))

            # Use adjustText to automatically adjust text positions to avoid overlap
            # adjust_text(text_objects) #arrowprops=dict(arrowstyle="->", color='grey', lw=1))
            # only_move={'points', 'text'}, arrowprops=dict(arrowstyle="->", color='gray', lw=0.5))

            # # Phase Plot
            # plt.subplot(2, 1, 2)
            # plt.plot(f_filtered, phase_filtered, label=acc)
            plt.xlabel('Frequency [Hz]')
            # plt.ylabel('Phase [rad]')
            # plt.grid(True, which="both")

    # plt.legend()
    plot_path = f'./images/{u.format_accel_plot_name(options, "bode")}'
    plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
    plt.savefig(plot_path, bbox_inches='tight')
    plt.show()
    plt.close()

    return plot_path


def frf_matrix(data: pd.DataFrame, options: dict):

    """Plot the bode plot of the data."""

    fig, axes = plt.subplots(3, 3)

    for i, shaker_pos in enumerate([0, 2, 4]):
        options['shakerPosition'] = shaker_pos
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
    Plot the imaginary part of the Frequency Response Function (FRF) at the natural frequency. Mode shapes
    can be extracted by the ratio of peaks for each accelerometer for a single forcing location.

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

    f_min = options['lowerCutoff']
    f_max = options['upperCutoff']

    # frf_i = []
    # frf_abs = []

    # im_values = []
    abs_values = []
    phase_values = []

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

            # Remove frequencies outside the desired range
            valid_idx = (f >= f_min) & (f <= f_max)
            f = f[valid_idx]
            frf = frf[valid_idx]
    
            # Convert inertance to receptance
            omega = 2 * np.pi * f  # Convert frequency to angular frequency (rad/s)
            omega[np.abs(omega) < 1e-10] = np.finfo(float).eps
            frf_r = frf / (-omega**2)  # Convert inertance to receptance

            # Get gain and imag component
            frf_abs = np.abs(frf_r)
            frf_phase = np.angle(frf_r)
            # frf_img = np.imag(frf_r)

            # Find peak magnitude and corresponding frequency
            idx_peak = np.argmax(frf_abs)
            # im_values.append(frf_img[idx_peak])
            abs_values.append(frf_abs[idx_peak])
            phase_values.append(frf_phase[idx_peak])

            # frf_i.append(frf_img)
            # frf_abs.append(abs_frf)

    # # Convert to NumPy arrays for easier processing
    # frf_i = np.array(frf_i)
    # frf_abs = np.array(frf_abs)

    # Find peaks in the absolute FRF
    ## If find_peaks are not reliable, can hard code the value of peaks as replacement to the line below ##
    # prominence = 0.01

    # if frf_abs.ndim == 1:
    #     peaks, _ = find_peaks(frf_abs, prominence=prominence)  # Use the array directly if it's 1D
    #     # If frf_i is 1D, treat it as a single row
    #     im_values = [(frf_i[peaks])]
    # else:
    #     peaks, _ = find_peaks(frf_abs[0], prominence=prominence)  # Access the first row if it's 2D (only uses first accelerometer)
    #     # If frf_i is 2D, extract imaginary parts for each row
    #     im_values = [(frf_i[i][peaks]) for i in range(frf_i.shape[0])]

    # im_values = []
    # for accelerometer_index in range(frf_i.shape[0]):
    #     # Find peak magnitude and corresponding frequency
    #     idx_peak = np.argmax(frf_abs[accelerometer_index,:])
    #     im_values.append(frf_i[accelerometer_index,idx_peak])

    # im_values /= np.max(np.abs(im_values))  # Normalise imaginary values
    abs_values /= np.max(np.abs(abs_values))  # Normalise abs values
    active_x_locations = [locations[i] for i, acc in enumerate(accelerometers.keys()) if accelerometers[acc]]

    # # Number of peaks found
    # num_peaks = len(peaks)

    # # Dynamic sizing based on the number of subplots
    # base_figsize = 5  # Base size for each subplot
    # fig_height = base_figsize * num_peaks  # Total figure height

    # # Adjust plot size and font size based on the number of peaks
    # base_font_size = 8
    # base_fig_width = 6
    # base_fig_height_per_peak = 4

    # # Scale font size and figure size based on the number of peaks
    # font_size = base_font_size - max(0, num_peaks - 3)  # Decrease font size if there are many peaks
    # tick_label_size = font_size - 1
    # fig_width = base_fig_width
    # fig_height = base_fig_height_per_peak * num_peaks

    # # Create subplots
    # fig, axes = plt.subplots(num_peaks, 1, figsize=(fig_width, fig_height), squeeze=False, sharex=True)
    # print(axes)
    # axes = axes.flatten()  # Flatten to handle single peak case
    # print(axes)

    # for i, ax in enumerate(axes):
    #     if i >= num_peaks:
    #         break  # Break if there are fewer peaks than subplots

    #     # Ensure x_locations and y-values have the same length
    #     y_values = [im_val[i] if i < len(im_val) else np.nan for im_val in im_values]
    #     y_values /= max(np.abs(y_values))

    #     # Plot the imaginary part of FRF for the current peak
    #     ax.scatter(x_locations, y_values, color='red', s=10, label='Mode {}'.format(i + 1))

    #     # Add vertical lines from the x-axis to each point
    #     for loc, val in zip(x_locations, y_values):
    #         if not np.isnan(val):  # Skip NaN values
    #             ax.plot([loc, loc], [0, val], color='blue', linestyle='--', linewidth=1)

    #     # Center the graph around the x-axis
    #     ax.axhline(0, color='black', linewidth=0.5)
    #     # ax.set_ylim(-1.1 * np.nanmax(np.abs(y_values)), 1.1 * np.nanmax(np.abs(y_values)))

    #     # Add labels and title with scaled font sizes
    #     # ax.set_xlabel('Accelerometer Location', fontsize=font_size)
    #     # ax.set_ylabel('Img Receptance', fontsize=font_size)
    #     # ax.set_title('Mode {}'.format(i + 1), fontsize=font_size)  # Slightly larger title
    #     ax.set_xticks(x_locations)
    #     # ax.set_xticklabels(['{:.2f}'.format(loc) for loc in x_locations], fontsize=tick_label_size)
    #     ax.set_xticklabels(x_locations, fontsize=tick_label_size)
    #     ax.tick_params(axis='both', labelsize=tick_label_size)
    #     ax.grid(True, linestyle='--', linewidth=0.5)
    #     # ax.legend(fontsize=tick_label_size)  # Scale legend font size

    # Check quadrant
    plot_phase = []
    datum = phase_values[0]
    for phase in phase_values:
        if abs(phase-datum) < np.pi/2:
            plot_phase.append(1)
        else:
            plot_phase.append(-1)
    
    # Plot the imaginary part of FRF for the current peak
    plt.scatter(active_x_locations, abs_values*plot_phase, color='red', s=10)

    # Add vertical lines from the x-axis to each point
    for loc, val in zip(active_x_locations, abs_values*plot_phase):
        if not np.isnan(val):  # Skip NaN values
            plt.plot([loc, loc], [0, val], color='blue', linestyle='--', linewidth=1)

    # Center the graph around the x-axis
    plt.xticks(active_x_locations)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.xlabel('Accelerometer location')
    plt.ylabel('Normalised Abs(Receptance FRF)')

    plot_path = f'./images/{u.format_accel_plot_name(options, "mode-shapes")}'
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    plt.close()

    return plot_path


async def plot_argand_r(data: pd.DataFrame, options: dict) -> None:

    """
    Plot the Argand diagram for the imaginary part of the FRF for the current peak.

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
    # sample_rate = options['samplingFreq']

    frf_ar = []
    frf_abs = []

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
            # frfs.append(frf)
    
            freqs = f
            # Convert inertance to receptance
            omega = 2 * np.pi * freqs  # Convert frequency to angular frequency (rad/s)
            frf_r = frf / (-omega**2)  # Convert inertance to receptance
    
            # Avoid division by zero at zero frequency
            frf_r[omega == 0] = np.inf

            abs_frf = np.abs(frf_r)

            frf_ar.append(frf_r)
            frf_abs.append(abs_frf)

    active_accelerometers = [key for key, value in accelerometers.items() if value]


    frf_ar = np.array(frf_ar)
    frf_abs = np.array(frf_abs)

    if frf_ar.ndim == 1:
        # If frf_ar is 1D, treat it as a single row
        frf_rows = [frf_ar]
    else:
        # If frf_ar is 2D, extract the rows corresponding to active accelerometers
        frf_rows = [frf_ar[i] for i in range(len(active_accelerometers))]

    # Find peaks in the absolute FRF
    prominence = 0.01

    if frf_abs.ndim == 1:
        peaks, _ = find_peaks(frf_abs, prominence=prominence)  # Use the array directly if it's 1D
    else:
        peaks, _ = find_peaks(frf_abs[0], prominence=prominence)  # Access the first row if it's 2D

    # Extract values at peaks
    arg = []
    for i in range(len(peaks)):  # Loop through all peaks
        arg_i = np.array([frf_row[peaks[i]] for frf_row in frf_rows])
        arg.append(arg_i)

    # Convert list of arrays into a single NumPy array for easier processing
    arg = np.array(arg)

    # Determine the number of rows in arg (number of peaks)
    num_peaks = arg.shape[0]

    # Adjust plot size and font size based on the number of peaks
    base_font_size = 8
    base_fig_width = 6
    base_fig_height_per_peak = 4

    # Scale font size and figure size based on the number of peaks
    font_size = base_font_size - max(0, num_peaks - 3)  # Decrease font size if there are many peaks
    tick_label_size = font_size - 1
    fig_width = base_fig_width
    fig_height = base_fig_height_per_peak * num_peaks

    # Create a vertical subplot based on the number of peaks
    fig, axs = plt.subplots(nrows=num_peaks, ncols=1, figsize=(fig_width, fig_height), sharex=True, sharey=True)

    # If there's only one peak, axs will not be an array, so we convert it to a list for consistency
    if num_peaks == 1:
        axs = [axs]

    # Plot each row of arg in a separate subplot
    for i, ax in enumerate(axs):

        point = arg[i]  # Get the i-th row of arg

        colors = ['r', 'g', 'b', 'c', 'm']  # Colors for each point in the row

        # Plot the Argand diagram for this row
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.set_xlabel('Real', fontsize=font_size)
        ax.set_ylabel('Imaginary', fontsize=font_size)
        ax.set_title(f'Argand Diagram - Mode {i+1}', fontsize=font_size)  # Slightly larger title

        # Adjust tick & legend label size
        ax.tick_params(axis='both', labelsize=tick_label_size)


        for j, p in enumerate(point):
            color = colors[j % len(colors)]  # Cycle through colors
            # Plot the point
            ax.scatter(p.real, p.imag, color=color, s=50, label=f'{active_accelerometers[j]}')
            # Draw a line from the origin to the point
            ax.plot([0, p.real], [0, p.imag], color=color, linestyle='-', linewidth=2)
            # Add text label for the point
            ax.text(p.real, p.imag, f' ({p.real:.2f}, {p.imag:.2f})', fontsize=font_size, color=color)

        ax.legend(fontsize=tick_label_size)

        # Add a common x-axis label for all subplots with a custom font size
        fig.supxlabel('X-axis', fontsize=14)

        # Add a common y-axis label for all subplots with a custom font size
        fig.supylabel('Y-axis', fontsize=14)

        # Add a common title for all subplots with a custom font size
        fig.suptitle('Trigonometric Functions', fontsize=16)

    plt.tight_layout()
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
    # options['samplingFreq'] = 1/(data['t'].max()/len(data))
    print(options)
    # asyncio.run(plot_dft(data, options))
    # asyncio.run(plot_nyquist(data, options))
    asyncio.run(plot_bode(data, options, 'Receptance'))
    # frf_matrix(data, options)
    # asyncio.run(plot_imaginary_r(data, options))
    # asyncio.run(plot_argand_r(data, options))
    # asyncio.run(plot_acceleration(data, options))
    # asyncio.run(plot_forcing(data, options))
