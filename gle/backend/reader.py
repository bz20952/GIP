import pandas as pd
import utils as u
import math

# This is where we store our data manipulation functions

def read_csv(options: dict):

    """Reads csv file and returns a pandas dataframe."""

    # Make sure that free vibration reads hammer testing data
    if options['excitationType'] == 'Free vibration':
        options['excitationType'] = 'Hammer testing'

    filename = u.format_filename(options)
    df = pd.read_csv(f'./data/{filename}.csv', header=0)

    # Adjust the sampling frequency if necessary
    if options['samplingFreq'] != 2048:
        sample_interval = math.floor(2048/options['samplingFreq'])
        df = df.iloc[::sample_interval,:]

    return df


