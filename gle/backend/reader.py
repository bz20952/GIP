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
    df = pd.read_csv(f'../../fe/sim_data/{filename}.csv', header=0)

    # Adjust the sampling frequency if necessary
    if options['samplingFreq'] != 2048:
        sample_interval = math.floor(2048/options['samplingFreq'])
        df = df.iloc[::sample_interval,:]

    for accel_index in range(5):
        for prefix in ['A', 'F']:
            df[f'{prefix}{accel_index}'] = df[f'{prefix}{accel_index}'] - np.mean(df[f'{prefix}{accel_index}'])

    # print(df)

    return df


