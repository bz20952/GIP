import pandas as pd

# This is where we store our data manipulation functions

def read_csv(file_name: str):

    """Reads csv file and returns a pandas dataframe."""

    df = pd.read_csv(f'./data/{file_name}', header=0)

    return df