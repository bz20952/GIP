import pandas as pd
from scipy.integrate import cumulative_trapezoid
import os
import numpy as np


def format_filename(options: dict):

    """Format filename to standard schema."""

    excitation = options['excitationType'].split(' ')[0].upper()

    # locations = ['0', 'l/4', 'l/2', '3l/4', 'l']
    # shaker_position = locations.index(options['shakerPosition'])

    # Because recorded data is symetric we can use data recorded at 0 as l and l/4 and 3l/4
    shaker_position = options['shakerPosition']
    if options['shakerPosition'] > 2:
        shaker_position = 5-shaker_position-1

    return f"{excitation}_{shaker_position}"


def check_if_file_exists(options: dict, plot_type: str):

    """Check if file exists before generating a new one."""

    if plot_type in ['accel', 'dft', 'anim', 'nyquist', 'bode']:
        filename = format_accel_plot_name(options, plot_type)
    else:
        filename = format_filename(options) + '_'  + plot_type + '.png'

    return os.path.isfile(f"./images/{filename}")


def format_accel_plot_name(options: dict, plot_type: str):

    """Format filename to standard schema."""

    accelerometers = options['accelerometers']
    file_suffix = ''
    for index, acc in enumerate(accelerometers.keys()):
        if accelerometers[acc]:
            file_suffix += f'_{index}'

    if plot_type in ['bode', 'nyquist', 'argand']:
        filename = format_filename(options) + '_' + str(options['samplingFreq']) + '_' + plot_type + file_suffix + '_f' + str(options['lowerCutoff']) + '-' + str(options['upperCutoff']) + '.png'
    else:
        filename = format_filename(options) + '_' + str(options['samplingFreq']) + '_' + plot_type + file_suffix + '.png'

    return filename


def accel_to_disp(data: pd.DataFrame, options: dict):

    """Convert acceleration to displacement by numerical integration."""

    # Time intervals (assuming uniform spacing)
    t = data["t"].values

    # Set dict to transfer to disp df
    disp_dict = {"t": t}  # Last two values must be removed due to double integration
    vel_dict = {"t": t}

    # Perform double integration for each acceleration column
    for col in ["A0", "A1", "A2", "A3", "A4"]:
        a = data[col].values/9.81  # Acceleration data (convert from g to m/s^2)

        # Normalise accelerations to have zero mean (i.e. zero steady state)
        a -= np.mean(a)
        
        # First integration: acceleration to velocity (assuming initial velocity = 0)
        v = cumulative_trapezoid(a, t, initial=0)
        
        # Second integration: velocity to displacement (assuming initial displacement = 0)
        s = cumulative_trapezoid(v, t, initial=0)
        
        # Store displacement
        disp_dict[col] = s
        vel_dict[col] = v

    displacement_df = pd.DataFrame(data=disp_dict)
    velocity_df = pd.DataFrame(data=velocity_df)

    return displacement_df, velocity_df


def circfit(x,y):

    """
    Least squares fit of X-Y data to a circle.
    Parameters:
    - x: array-like, 1-D array of X data points
    - y: array-like, 1-D array of Y data points

    Returns:
    - r: Radius of the fitted circle
    - xc, yc: Center coordinates of the fitted circle (optional)
    - rmse: Root Mean Squared Error (optional)
    """ 

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


def closest_index(point, arr):
    return min(range(len(arr)), key=lambda i: abs(arr[i] - point))


if __name__ == '__main__':
    import reader as r
    options = {
        'excitationType': 'FREE',
        'samplingFreq': '400',
        'shakerPosition': '5'
    }
    data = r.read_csv(options)
    accel_to_disp(data, options)