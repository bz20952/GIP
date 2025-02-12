import reader as r
import utils as u
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal


def get_natural_freqs(data: pd.DataFrame, options: dict):
    
    """Get natural frequencies from acceleration data."""
    
    accelerometers = options['accelerometers']
    peakind = signal.find_peaks_cwt(data, np.arange(1,10))

    # Do FFT
    # Pick peaks
    # Save plots with labelled peaks to images folder
    
    return