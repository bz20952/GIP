import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def post_process():

    # Load the CSV file
    df = pd.read_csv("teensy_data.csv", header=0)  # Load only the first 1000 rows

    print(df)

    df['Time (ms)'] = (df['Time (ms)'] - df['Time (ms)'].iloc[0])/1e6
    df['A0'] = (df['A0'] - 2114.0)/40.775  # for acceleration in m/s^2
    # df['A0'] = (df['A0']-2114.0)/400.0 # for acceleration in g

    plt.figure()
    plt.scatter(df['Time (ms)'], df['A0'])
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Accelerometer data')
    plt.show()

    # Save to CSV
    df.to_csv("output.csv", index=False, header=False)  # No row/column headers