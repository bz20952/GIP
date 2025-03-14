import pandas as pd
from scipy.integrate import cumulative_trapezoid
import os


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

    filename = format_filename(options) + '_' + str(options['samplingFreq']) + '_' + plot_type + file_suffix + '.png'

    return filename


def accel_to_disp(data: pd.DataFrame, options: dict):

    """Convert acceleration to displacement by numerical integration."""

    # Time intervals (assuming uniform spacing)
    t = data["t"].values

    # Set dict to transfer to disp df
    disp_dict = {"t": t}  # Last two values must be removed due to double integration

    # Perform double integration for each acceleration column
    for col in ["A0", "A1", "A2", "A3", "A4"]:
        a = data[col].values/9.81  # Acceleration data (convert from g to m/s^2)
        
        # First integration: acceleration to velocity (assuming initial velocity = 0)
        v = cumulative_trapezoid(a, t, initial=0)
        
        # Second integration: velocity to displacement (assuming initial displacement = 0)
        s = cumulative_trapezoid(v, t, initial=0)
        
        # Store displacement
        disp_dict[col] = s

    displacement_df = pd.DataFrame(data=disp_dict)

    return displacement_df


if __name__ == '__main__':
    import reader as r
    options = {
        'excitationType': 'FREE',
        'samplingFreq': '400',
        'shakerPosition': '5'
    }
    data = r.read_csv(options)
    accel_to_disp(data, options)