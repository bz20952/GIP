import pandas as pd
from scipy.integrate import cumulative_trapezoid
import os


def format_filename(options: dict):

    """Format filename to standard schema."""

    excitation = options['excitationType'].split(' ')[0].upper()

    locations = ['0', 'l/4', 'l/2', '3l/4', 'l']
    shaker_position = locations.index(options['shakerPosition'])

    return f"{excitation}_{options['samplingFreq']}_{shaker_position}"


def check_if_file_exists(options: dict, plot_type: str):

    """Check if file exists before generating a new one."""

    filename = format_filename(options) + '_'  + plot_type

    return os.path.isfile(f"./images/{filename}")


def accel_to_disp(data: pd.DataFrame, options: dict):

    """Convert acceleration to displacement by numerical integration."""

    # Time intervals (assuming uniform spacing)
    t = data["t"].values

    # Initialize displacement DataFrame
    displacement_df = pd.DataFrame({"t": t})

    # Perform double integration for each acceleration column
    for col in ["0", "l/4", "l/2", "3l/4", "l"]:
        a = data[col].values  # Acceleration data
        
        # First integration: acceleration to velocity (assuming initial velocity = 0)
        v = cumulative_trapezoid(a, t, initial=0)
        
        # Second integration: velocity to displacement (assuming initial displacement = 0)
        s = cumulative_trapezoid(v, t, initial=0)
        
        # Store displacement
        displacement_df[col] = s

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