import pandas as pd
import numpy as np
import utils as u
import math

# This is where we store our data manipulation functions

def read_csv(options: dict):

    """Reads csv file and returns a pandas dataframe."""

    # Make sure that free vibration reads hammer testing data
    if options['excitationType'] == 'Free vibration':
        options['excitationType'] = 'Soft'
    elif options['excitationType'] == 'Hammer testing':
        options['excitationType'] = options['tipHardness']

    filename = u.format_filename(options)
    df = pd.read_csv(f'./data/{filename}.csv', header=0)

    # Adjust the sampling frequency if necessary
    if options['samplingFreq'] != 2048:
        sample_interval = math.floor(2048/options['samplingFreq'])
        df = df.iloc[::sample_interval,:]

    # Normalise the data to have zero mean
    for accel_index in range(5):
        for prefix in ['A', 'F']:
            df[f'{prefix}{accel_index}'] = df[f'{prefix}{accel_index}'] - np.mean(df[f'{prefix}{accel_index}'])

    # # Mirror measurement locations if mirroring shaker position
    # if options['shakerPosition'] > 2:
    #     df.columns = ['t', 'F4', 'A4', 'F3', 'A3', 'F2', 'A2', 'F1', 'A1', 'F0', 'A0']

    return df


