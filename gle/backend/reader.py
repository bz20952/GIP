import pandas as pd
import utils as u

# This is where we store our data manipulation functions

def read_csv(options: dict):

    """Reads csv file and returns a pandas dataframe."""

    filename = u.format_filename(options)
    df = pd.read_csv(f'./data/{filename}', header=0)

    return df


