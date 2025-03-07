from scipy.signal import butter
from scipy import signal
import pandas as pd
from utils import format_filename


def filter(data: pd.DataFrame, options: dict):

    """Wrapper function to identify the type of filter and call the appropriate filter function."""

    if options['filterType'] == 'bandPass':
        b, a = bandpass(options['lowerCutoff'], options['upperCutoff'], options['samplingFreq'])
    elif options['filterType'] == 'lowPass':
        b, a = lowpass(options['upperCutoff'], options['samplingFreq'])
    elif options['filterType'] == 'highPass':
        b, a = highpass(options['lowerCutoff'], options['samplingFreq'])
    else:
        return f'./data/{format_filename(options)}.csv'

    accelerometers = options['accelerometers']
    for acc in accelerometers.keys():
        data[acc] = signal.lfilter(b, a, data[acc])

    data_path = f'./data/{format_filename(options)}_filtered_{options['lowerCutoff']}_{options['upperCutoff']}.csv'
    data.to_csv(data_path, index=False)

    return data_path


def lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band', analog=False)
    return b, a


if __name__ == "__main__":
    # The following is used to test the filtering functionality
    import json
    import reader as r
    with open('./templates/requestFormat.json') as f:
        options = json.load(f)
    data = r.read_csv(options)
    data_path = filter(data, options)
    print(data_path)