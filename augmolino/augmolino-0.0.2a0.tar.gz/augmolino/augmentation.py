import warnings
import librosa as lr
import numpy as np
import soundfile as sf
import random as rd
import os

__all__ = ['timeStretch', 'pitchShift',
           'offsetAudio', 'fadeAudio', 'mixAudio']

descriptors = {
    "_augmentation": "base class",
    __all__[0]: "time_stretch",
    __all__[1]: "pitch_shift",
    __all__[2]: "time_offset",
    __all__[3]: "time_fade",
    __all__[4]: "sound_mix"}


class _augmentation:
    """
    Private base class for different augmentations.
    Prepares general parameters which every augmentation
    needs. 

    Parameters
    ----------
    `sample_rate`:
        sample rate of audio file (used for resampling). Default
        is `22050`.
    `function`:
        function which applies the augmentation to the signal
        array. Can be used to reference internal functions or
        functions provided by other modules. Default is `None`.
    `kwargs`:
        Arguments for `function`.

    Notes
    -----
    This is a private base class which is not intened to be
    called on its own. Always call an actual augmentation.
    """

    def __init__(self, sample_rate=22050, function=None, **kwargs):

        self.sample_rate = sample_rate
        self.descriptor = descriptors["_augmentation"]
        self.function = function
        self.kwargs = kwargs
        # use all kwargs values to create a unique ID
        kwargs_vals = []
        for arg in kwargs.values():
            if isinstance(arg, str):
                if "/" in arg or "\\" in arg:
                    arg = self._shortenName(arg)
            kwargs_vals.append(str(arg))
        self.tag = ('_'.join(kwargs_vals)).replace('.', '_')

    def run(self, f_source, f_dest=None, **kwargs):
        """
        Apply the augmentation to a specified file and store 
        the result as array or other file.

        Parameters
        ----------
        `f_source`:
            path to file which should be augmented. Must be in wav format.
        `f_dest`:
            path to augmented file which will be saved. If left unspecified,
            a `numpy` array of the augmented signal is returned instead. Pass
            `"auto"` to store in the source with unique names. Default
            is `None`.
        `kwargs`:
            Arguments for executing of `function`.    
        """
        self._load(f_source)
        self.f_dest = self._parsePath(f_dest)

        # append kwargs in case some are appended after init
        self.kwargs |= kwargs

        x_new = self._executeFunction()

        if self.f_dest != None:
            sf.write(self.f_dest, x_new, self.sample_rate)
            return None

        else:
            return x_new

    def _load(self, f_source):

        path_details = os.path.splitext(f_source)
        extension = path_details[1]

        if extension != ".wav":
            raise ValueError("File type not supported! Use '.wav' instead.")

        self.f_source = f_source

        x, sr = lr.load(path=self.f_source, sr=self.sample_rate)
        self.signal = x

    def _parsePath(self, f_dest):
        # user wants to save the augmentation
        if f_dest != None:
            if self.f_source == f_dest:
                warnings.warn("Source and save name are the same,\
                    original file will be overwritten!")
                return f_dest
            elif f_dest == "auto":
                return self._autoName(self.descriptor, self.tag)
            else:
                return f_dest

        # user wants a temporary array
        else:
            return None

    def _autoName(self, descriptor, tag):
        if self.f_source == None:
            raise ValueError("No source to autoname from!")
        return self.f_source[:-4] + f"_{descriptor}_{tag}.wav"

    def _executeFunction(self):
        return self.function(self.signal, **self.kwargs)

    def _shortenName(self, f_path):
        return os.path.basename(f_path)[:-4]


class timeStretch(_augmentation):
    """
    Stretch or squeeze a sound while retaining pitch.

    Parameters
    ----------
    `rate`:
        Float. Stretch factor defined by speed of playback. A `rate` < 1
        stretches the sound, a `rate` > 1 squeezes it.
        Default is `1`
    `sample_rate`:
        Int. Sample rate of audio file (used for resampling).
        Default is `22050`
    """

    def __init__(self, rate=1, sample_rate=22050):
        self.rate = rate
        super().__init__(sample_rate=sample_rate,
                         function=lr.effects.time_stretch,
                         rate=rate)
        self.descriptor = descriptors[__all__[0]]


class pitchShift(_augmentation):
    """
    Shift a given input signal's pitch by semitones.

    Parameters
    ----------
    `semitones`:
        Float. Number of western scale semitones to shift up or down.
        Default is `1`
    `sample_rate`:
        Int. Sample rate of audio file (used for resampling).
        Default is `22050`
    """

    def __init__(self, semitones=1, sample_rate=22050):
        self.semitones = semitones
        super().__init__(sample_rate=sample_rate,
                         function=lr.effects.pitch_shift,
                         sr=sample_rate,
                         n_steps=semitones)
        self.descriptor = descriptors[__all__[1]]


class offsetAudio(_augmentation):
    """
    Offset a sound by added dead-time or or by later start.

    Parameters
    ----------
    `s`:
        Float. Offset in seconds. s < 0: skip first samples. 
        s > 0: add dead-time to start. Default is `0`.
    `sample_rate`:
        Int. Sample rate of audio file (used for resampling).
        Default is `22050`
    """

    def __init__(self, s=0, sample_rate=22050):
        self.s = s
        super().__init__(sample_rate=sample_rate,
                         function=self._offset,
                         s=s)
        self.descriptor = descriptors[__all__[2]]

    def _offset(self, y, s):

        sample_offs = int(self.sample_rate * abs(s))

        if len(y) <= sample_offs:
            raise ValueError("Offset longer than duration of sound!")
        if s < 0:
            return y[sample_offs:]
        else:
            return np.insert(y, 0, np.zeros(sample_offs))


class fadeAudio(_augmentation):
    """
    Create a logarithmic fade-in or fade-out for a sound.

    Parameters
    ----------
    `s`:
        Float. Fade time in seconds. Default is `0`.
    `direction`:
        String. Direction from which the fade is applied. Default
        is `"in"`.    
    `sample_rate`:
        Int. Sample rate of audio file (used for resampling).
        Default is `22050`
    """

    def __init__(self, s=0, direction="in", sample_rate=22050):
        self.s = s
        self.direction = direction
        if direction not in ["in", "out"]:
            raise ValueError(f"parameter '{direction}' not recognized!")

        super().__init__(sample_rate=sample_rate,
                         function=self._fade,
                         s=s,
                         direction=direction)
        self.s = s
        self.direction = direction
        self.descriptor = descriptors[__all__[3]]

    def _fade(self, y, s, direction):

        fade_len = self.sample_rate * s
        x_new = y

        if direction == "out":
            end = len(y)
            start = end - fade_len
            fade_curve = np.logspace(0, -3, fade_len)
            x_new[start:end] *= fade_curve
        else:
            fade_curve = np.logspace(-3, 0, fade_len)
            x_new[0:fade_len] *= fade_curve

        return x_new


class mixAudio(_augmentation):
    """
    Mix two wavefiles at random or specified timestamps.

    Parameters
    ----------
    `ratio`:
        Float. Ratio by which the sounds are mixed. 
        `0 <= ratio <= 1`, 1 ignores the noise, 0 the main sound. 
        Default is `1`.
    `start_at`:
        Float. Second at which the mixed in sound should be used.
        If unspecified, a random time will be used. Default is `None`.     
    `sample_rate`:
        Int. Sample rate of audio file (used for resampling).
        Default is `22050`

    Notes
    -----
    Augmented sound is as long as the original sound of interest, 
    not the mixed-in sound    
    """

    def __init__(self, ratio=0.5, start_at=None, sample_rate=22050):
        self.ratio = ratio
        self.start_at = start_at
        super().__init__(sample_rate=sample_rate,
                         function=self._mix,
                         ratio=ratio,
                         start_at=start_at)
        self.descriptor = descriptors[__all__[4]]

    def _mix(self, y, f_mix, ratio, start_at):
        y_mix, _ = lr.load(f_mix, sr=self.sample_rate)
        y_len = len(y)
        y_mix_len = len(y_mix)
        start = int(start_at * self.sample_rate)

        # use value of center sample as seed
        if start_at == None:
            rd_value = int(1000*y[int(y_len/2)])
            rd.seed(rd_value)

        if y_len < y_mix_len:
            if start_at == None:
                start = rd.randint(0, y_mix_len-y_len)
            return y * ratio + y_mix[start:start+y_len] * (1-ratio)
        else:
            if start_at == None:
                start = rd.randint(0, y_len-y_mix_len)
                y_mix_pad = np.append(np.zeros(start), y_mix)
                y_mix_pad = np.append(
                    y_mix_pad, np.zeros(y_len-start-y_mix_len))

            return y * ratio + y_mix_pad * (1-ratio)
