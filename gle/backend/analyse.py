import reader as r
import utils as u
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal
from scipy.fft import fft
import numpy as np


def get_natural_freqs(data: pd.DataFrame, options: dict):
    
    """Get natural frequencies from acceleration data."""
    
    accelerometers = options['accelerometers']

    # Do FFT
    dft = fft.fft(data)
    # Pick peaks
    peakind = signal.find_peaks_cwt(dft, np.arange(1,10))


    # Save plots with labelled peaks to images folder
    
    return