# profilometer
import numpy as np
import pandas as pd
from .misc import *
import mat73
import scipy.io
from scipy import signal

__all__ = ['parse_oscilloscope_optical_left_xy_smooth']

def read_files(input_path, txt_path, plot_path, hist_path, interactive=False):
    try:
        mat = mat73.loadmat(input_path)
    except:
        mat = scipy.io.loadmat(input_path)
    x = mat["x"][0,:] # in seconds
    y = mat["y"][0,:] # in V
    data = {
        "Time (ns)": x*1e9, # in nanoseconds
        "Voltage (mV)": smooth(x, y)*1e3, # in mV
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(txt_path, index=False)
    p = Plot(df, interactive=interactive)
    p.plot(plot_path)
    p.hist(hist_path)

def smooth(x, y):
    # band pass filter from 100 MHz to 10 GHz
    freq = 1/(x[1] - x[0])
    sos = signal.butter(10, [100e6, 10e9], 'hp', fs=freq, output='sos')
    filtered = signal.sosfilt(sos, y)
    return filtered

def parse_oscilloscope_optical_left_xy_smooth(**kwargs):
    read_files(kwargs["input_path"], kwargs["txt_path"], kwargs["plot_path"], kwargs["hist_path"])
