#!/usr/bin/env python
__author__ = 'Danelle Cline'
__copyright__ = '2022'
__license__ = 'GPL v3'
__contact__ = 'dcline at mbari.org'
__doc__ = '''

PCEN denoise and cache

@var __date__: Date of last svn commit
@undocumented: __doc__ raven
@status: production
@license: GPL
'''

import h5py
import librosa
import sklearn
import numpy as np
from pathlib import Path
from oceansoundscape.raven import BLEDParser
from oceansoundscape.spectrogram import conf as global_conf
from oceansoundscape.spectrogram import utils


class PCENSmooth(object):

    def __init__(self, hdf_path: Path, bled: BLEDParser, conf: dict(), x: np.array([]), sample_rate: int):
        """
        Denoises file with PCEN and caches in an HDF file; it if exists it will be overwritten
        :param hdf_path: absolute path to hdf file
        :param bled: RavenBLEDParser
        :param conf: configuration parameters for the call
        :param x: raw wav data as a float32
        :param sample_rate: sample rate of the raw data
        """
        try:
            if bled.num_detections == 0:
                print(f'No valid detections - skipping cache for {bled.wav_path}')
                return

            detections_df = bled.data
            hop_length = round(conf['num_fft'] * (1 - global_conf.OVERLAP))
            self._cache = hdf_path

            with h5py.File(self._cache.as_posix(), 'w') as hf:

                call_width = int(conf['duration_secs'] * sample_rate)
                max_width = len(x) - 1

                for row, item in sorted(detections_df.iterrows()):
                    start = int(item.call_start - call_width)
                    end = int(item.call_end + call_width)
                    if start > 0 and end < max_width:

                        # get the frequency ranges from the duplet in conf['freq_range']
                        freq_range = conf['freq_range']

                        # the first range is the largest, so we'll use it to set the size of the output array
                        stft = librosa.feature.melspectrogram(
                            y=sklearn.preprocessing.minmax_scale(x[start:end], feature_range=((-2 ** 31), (2 ** 31))),
                            sr=sample_rate,
                            hop_length=hop_length,
                            power=1,
                            n_mels=conf['num_mels'],
                            fmin=freq_range[0][0],
                            fmax=freq_range[0][1])

                        stft_pcen = librosa.pcen(stft * (2 ** 31), sr=sample_rate,
                                                 hop_length=hop_length,
                                                 gain=global_conf.PCEN_GAIN, bias=global_conf.PCEN_BIAS,
                                                 time_constant=global_conf.PCEN_TIME_CONSTANT)

                        # if there is a secondary range, otherwise just use the first range
                        if len(freq_range) > 1:
                            # the second range is smaller, so we will pad it with zeros to match the size of the first range
                            stft_second = librosa.feature.melspectrogram(
                                y=sklearn.preprocessing.minmax_scale(x[start:end], feature_range=((-2 ** 31), (2 ** 31))),
                                sr=sample_rate,
                                hop_length=hop_length,
                                power=1,
                                n_mels=conf['num_mels'],
                                fmin=freq_range[1][0],
                                fmax=freq_range[1][1])

                            stft_pcen_second = librosa.pcen(stft_second * (2 ** 31), sr=sample_rate,
                                                     hop_length=hop_length,
                                                     gain=global_conf.PCEN_GAIN, bias=global_conf.PCEN_BIAS,
                                                     time_constant=global_conf.PCEN_TIME_CONSTANT)


                            # make the stft_pcen_second the same size as stft_pcen
                            stft_pcen_second = np.pad(stft_pcen_second, ((0, 0), (0, stft_pcen.shape[1] - stft_pcen_second.shape[1])), 'constant')

                            # concatenate the two arrays
                            stft_pcen_final = np.concatenate((stft_pcen, stft_pcen_second), axis=0)
                        else:
                            stft_pcen_final = stft_pcen

                        stft_smooth = utils.ImageUtils.smooth(stft_pcen_final, conf['blur_axis'])

                        try:
                            hf.create_dataset(str(item.Selection), data=stft_smooth)
                        except Exception as ex:
                            # allow for exceptions when unable to create links
                            # can have duplicates in the training files
                            print(f'Error denoising {ex}')
                            continue
                    else:
                        print(f'Skipping {row} call out of bounds')


        except Exception as ex:
            print(f'Error denoising {ex}')
            self._cache.unlink()
            raise ex

    def __del__(self):
        if hasattr(self, '_cache') and self._cache.exists():
            self._cache.unlink()

    def get_data(self, selection):
        """
        Fetch preprocessed PCEN data from cache
        :param selection: selection table number
        :return:
        """
        with h5py.File(self._cache.as_posix(), mode='r') as hf:
            stft_pcen = hf[str(selection)][:]
        return stft_pcen
