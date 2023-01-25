import matplotlib.pyplot as plt
import librosa.display
import librosa as lr
import os

__all__ = ['quickPlotSpectrogram']


def quickPlotSpectrogram(signal, sample_rate=22050):
    """
    Draw a spectrogram of the specified signal

    Parameters
    ------
    `y`:
        Array, String. Path to audio or audio data.
    `sample_rate`:
        Desired sample rate of audio. Default is `22050`.
    """

    if os.path.isfile(signal):
        x, _ = lr.load(signal, sr=sample_rate)
    else:
        x = signal    

    X = lr.stft(x)
    Xdb = lr.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sample_rate, x_axis='time', y_axis='hz')
    plt.colorbar()
    plt.show()