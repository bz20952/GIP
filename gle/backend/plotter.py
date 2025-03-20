from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import utils as u
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting module
from adjustText import adjust_text
# from circle_fit import taubinSVD
# import control as ctrl 

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

    # fig= plt.figure()
    # ax = fig.add_subplot(111, projection='3d')  # Create a 3D subplot

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
            frf_mobility=frf/1j*f*2*np.pi
            frf=frf_mobility #uncomment this line if plotting inertance
            frfReal = np.real(frf)
            frfImag = np.imag(frf)

            # Filter for desired frequency range (depends on question that we ask i.e. damping ratio at 2nd mode for e.g.)
            f_min=108
            f_max=115 #for first natural frequency damping ratio
            valid_idx = (f >= f_min) & (f <= f_max)
            f_filtered=f[valid_idx]
            frfReal_filtered = frfReal[valid_idx]
            frfImag_filtered = frfImag[valid_idx]

            # #Fit a circle
            # coordinates=list(zip(frfReal_filtered,frfImag_filtered))
            # xc,yc,r,sigma=taubinSVD(coordinates)

            plotcircfit(frfReal_filtered,frfImag_filtered,f_filtered)  # Correct usage
            
            # Plot data points and circle fit using circle plotting function
            # plotcircfit(x,y)

            # Plot the data points
            # fig,ax=plt.subplots(figsize=(20,6))
            # ax.scatter(frfReal_filtered, frfImag_filtered, color='red', label='Data Points', zorder=2)
            # ax.plot(f, frfReal, frfImag, label=acc) #3d plot
            # ax.plot(frfReal_filtered, frfImag_filtered, label=acc) #2d plot

            # # Plot the fitted circle
            # circle = plt.Circle((xc, yc), r, color='blue', fill=False, linewidth=2, label='Fitted Circle', zorder=1)
            # ax.add_patch(circle)
            # ax.set_aspect('equal')  # Ensures the circle is not distorted

    # ax.set_xlim(150, 200)  # Set limits for the z-axis (Frequency) #3d plot
    # ax.set_ylim(y_min, y_max)  # Set limits for the x-axis (Real part) #3d plot
    # ax.set_zlim(z_min, z_max)  # Set limits for the y-axis (Imaginary part) #3d plot

    plot_path = f'./images/{u.format_accel_plot_name(options, "nyquist")}'

    # ax.set_ylabel('Re') #3d plot
    # ax.set_zlabel('Im') #3d plot
    # ax.set_xlabel('Frequency [Hz]') #3d plot
    # ax.set_title('Inertance Nyquist plot') #3d plot

    # plt.xlabel('Re') #2d plot
    # plt.ylabel('Im') #2d plot
    # plt.title('Inertance Nyquist plot') #2d plot
    # plt.legend()
    # plt.grid(True)
    plt.savefig(plot_path, bbox_inches='tight', pad_inches=0.5)
    # plt.close()

    return plot_path
# for plot nyquist labellings, the following input is required: 1) range of frequencies interested
# as of now, Ammar has them hardcoded into the function 
    
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

            # Filter for desired frequency range (depends on question that we ask i.e. damping ratio at 2nd mode for e.g.)
            f_min=110 
            f_max=150 #for first natural frequency damping ratio
            valid_idx = (f >= f_min) & (f <= f_max)
            f_filtered = f[valid_idx]
            magnitude_filtered = magnitude[valid_idx]
            phase_filtered=phase[valid_idx]
            phase_filtered = phase[valid_idx]

            # # Use system identification to estimate a transfer function
            # f_filtered_rad=2*np.pi*f_filtered # change to rad/s
            # magnitude_filtered_lin=10**(magnitude_filtered/20) # change to linear scale for transfer function fitting
            # num,den=ctrl.magfit(f_filtered_rad, magnitude_filtered_lin,n=2,m=2)
            # tf_fit=ctrl.TransferFunction(num,den)
            # mag_tf,phase_tf, omega= ctrl.bode(tf_fit, dB=True, omega=f_filtered_rad, plot=False)
            # f_filtered_Hz=omega/(2*np.pi)


            # Find peak magnitude and corresponding frequency
            peak_mag = np.max(magnitude_filtered)
            idx_peak = np.argmax(magnitude_filtered)
            f_n = f_filtered[idx_peak]

            # Find Half-Power (-3 dB) Magnitude
            half_power_mag = peak_mag - 3  # -3 dB point

            # # Find indices for half-power frequencies
            # idx_f1 = np.where(magnitude_filtered >= half_power_mag)[0][0]  # First occurrence
            # idx_f2 = np.where(magnitude_filtered >= half_power_mag)[0][-1]  # Last occurrence

            
            # Find first index to the left of peak where magnitude drops to or below -3 dB
            # Search backwards from the peak index
            idx_f1 = np.where(magnitude_filtered[:idx_peak] <= half_power_mag)[0][-1]  # First index to the left

            # Find first index to the right of peak where magnitude drops to or below -3 dB
            # Search forwards from the peak index
            idx_f2 = np.where(magnitude_filtered[idx_peak:] <= half_power_mag)[0][0] + idx_peak  # First index to the right

            # Get corresponding frequency values
            f1 = f_filtered[idx_f1]
            f2 = f_filtered[idx_f2]

            # Magnitude Plot
            plt.figure(figsize=(20,6)) #make figure bigger
            plt.subplot(2, 1, 1)
            plt.semilogx(f_filtered, magnitude_filtered, label=acc)
            # plt.semilogx(f_filtered_Hz,20*np.log10(mag_tf))
            # plt.xlim(1, max(f))
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
            text_objects.append(plt.text(f_n, peak_mag+2, f'Peak: {f_n:.2f} Hz', color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='center'))

            text_objects.append(plt.text(f1, magnitude_filtered[idx_f1]+2, f'f1: {f1:.2f} Hz', color='black', fontsize=12, verticalalignment='bottom', horizontalalignment='center'))

            text_objects.append(plt.text(f2, magnitude_filtered[idx_f2]+2, f'f2: {f2:.2f} Hz', color='black', fontsize=12, verticalalignment='bottom', horizontalalignment='center'))

            # Use adjustText to automatically adjust text positions to avoid overlap
            adjust_text(text_objects) #arrowprops=dict(arrowstyle="->", color='grey', lw=1))
            # only_move={'points', 'text'}, arrowprops=dict(arrowstyle="->", color='gray', lw=0.5))

            # Phase Plot
            plt.subplot(2, 1, 2)
            plt.semilogx(f_filtered, phase_filtered, label=acc)
            # plt.xlim(1, max(f))
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
    # plt.close()

    return plot_path
# for plot bode labellings, the following input is required: 1) range of frequencies interested
# as of now, Ammar has them hardcoded into the function similar to nyquist plot

def circfit(x,y):
                """ Least squares fit of X-Y data to a circle.
                Parameters:
                - x: array-like, 1-D array of X data points
                - y: array-like, 1-D array of Y data points
    
                Returns:
                - r: Radius of the fitted circle
                - xc, yc: Center coordinates of the fitted circle (optional)
                - rmse: Root Mean Squared Error (optional) """ 
     
                # Prepare variables for solving the linear system
                xx = x ** 2
                yy = y ** 2
                xy = x * y
                xxyy = xx + yy
                sx = np.sum(x)
                sy = np.sum(y)
                sxx = np.sum(xx)
                syy = np.sum(yy)
                sxy = np.sum(xy)

                # Solve the linear system using LU decomposition
                A = np.array([[sx, sy, len(x)], [sxy, syy, sy], [sxx, sxy, sx]])
                B = np.array([sxx + syy, np.sum(xxyy * y), np.sum(xxyy * x)])
    
                # # LU decomposition
                # L, U = np.linalg.lu(A)
                # a = np.linalg.solve(U, np.linalg.solve(L, b))
                a = np.linalg.solve(A, B)
    
                # Compute the circle parameters
                xc = 0.5 * a[0]  # X-position of the center of the fitted circle
                yc = 0.5 * a[1]  # Y-position of the center of the fitted circle
                r = np.sqrt(xc**2 + yc**2 + a[2])  # Radius of the fitted circle
                # Calculate RMSE if needed
                rmse = np.sqrt(np.mean((np.sqrt((x - xc) ** 2 + (y - yc) ** 2) - r) ** 2))

                # Return the fitted circle parameters
                return r, xc, yc, rmse

            
def plotcircfit(x,y,z):
                """Fit X-Y data to a circle and create a plot.
    
                Parameters:
                - x: 1-D array (list or NumPy array) of X data
                - y: 1-D array (list or NumPy array) of Y data
                - z: 1-D array (list or NumPy array) of Y data """
    
                # Compute circle fit
                r, xc, yc, RMSE = circfit(x, y)

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
                ax.plot(xc, yc, 'ko', label='Circle Center: 'f'Radius={r:.2f}, 'f'Coordinates=({xc:.2f}, {yc:.2f})', markersize=5)  # Circle center (black)

                # Labels & Title
                plt.xlabel('Real',fontsize=10)
                plt.ylabel('Imaginary',fontsize=10)
                plt.title(f'Inertance plot and Best Fit Circle, RMSE = {RMSE:.5f} ',fontsize=10)
                plt.legend(fontsize=8, bbox_to_anchor=(1, 1))
                plt.grid(True)

                # # Annotate radius
                # radiustexts=[]
                # radiustexts.append(plt.text(xc, yc+0.05, f'Radius = {r:.5f}', fontsize=10))
                # radiustexts.append(plt.text(xc, yc-0.05,f"({xc:.2f}, {yc:.2f})", fontsize=10))
                # adjust_text(radiustexts) #arrowprops=dict(arrowstyle="->", color='gray', lw=1)) 
                
                # Find sweep rates of all data points
                sweep_rate=np.zeros(len(x-1))
                for i in range(len(x)-1):
                
                    # find sweep angle between data points
                    vec1= np.array([x[i]-xc, y[i]-yc])
                    vec2= np.array([x[i+1]-xc, y[i+1]-yc])
                    dot_product= np.dot(vec1, vec2)
                    mag1= np.linalg.norm(vec1)
                    mag2= np.linalg.norm(vec2)
                    cos_theta= dot_product / (mag1 * mag2)
                    theta_rad= np.arccos(cos_theta)
                    theta_deg= np.degrees(theta_rad)

                    #find freqeuncy change between data points
                    freq_change= z[i+1]-z[i]
                    
                    # update sweep rate array
                    sweep_rate[i]=theta_deg/freq_change

                # Find maximum sweep rate
                max_sweep_rate= np.max(sweep_rate)
                idx_max_sweep_rate = np.argmax(sweep_rate)
                idx1_of_data_points_surrounding_maximum_sweep_rate=idx_max_sweep_rate
                idx2_of_data_points_surrounding_maximum_sweep_rate=idx_max_sweep_rate+1

                # Annotate labels
                data_points_intervals=1
                data_points_used=5
                texts=[]
                # for i in range(0,len(x),Data_points_intervals):
                    # if x[i]>0 and y[i]<0:
                for i in range(idx1_of_data_points_surrounding_maximum_sweep_rate-data_points_used,idx2_of_data_points_surrounding_maximum_sweep_rate+data_points_used+1):
                    txt= plt.text(x[i] + 0.05, y[i], f"({x[i]:.2f}, {y[i]:.2f},{z[i]:.2f})", fontsize=8, color='k') # text for coordinates and frequency of data point
                    texts.append(txt)

                # Adjust text labels to prevent overlap
                adjust_text(texts, arrowprops=dict(arrowstyle="->", color='gray', lw=1))

                # # Show plot
                # plt.show()
# for plot circle function, the code labels 10 points to each side of the maximum sweep rate in the plot

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


if __name__ == '__main__':
    import json
    import asyncio
    import reader as r
    with open('./templates/requestFormat.json') as f:
        options = json.load(f)
    data = r.read_csv(options)
    

    import asyncio
    result = asyncio.run(plot_nyquist(data, options))  # Correct usage

    # async def main():
    #     result = await plot_acceleration(data, options)  
    # asyncio.run (main())

    # plot_forcing(data, options)
    # plot_dft(data, options)
    # plot_nyquist(data, options)
    # plot_bode(data, options)

# "C:\Users\Ammar Haziq\Downloads\GIP\gle\backend\templates\requestFormat.json"
