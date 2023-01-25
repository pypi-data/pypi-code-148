from sonusai.mixture.truth_functions.data import Data
from sonusai.mixture.types import Truth


def target_f(data: Data) -> Truth:
    import numpy as np

    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.target_fft.bins:
        raise SonusAIError(f'Invalid num_classes for target_f truth: {data.config.num_classes}')

    for offset in data.offsets:
        target_f = np.complex64(data.target_fft.execute(data.target_audio[offset:offset + data.frame_size]))

        indices = slice(offset, offset + data.frame_size)
        for index in data.zero_based_indices:
            start = index
            stop = start + data.target_fft.bins
            data.truth[indices, start:stop] = np.real(target_f)

            start = stop
            stop = start + data.target_fft.bins
            data.truth[indices, start:stop] = np.imag(target_f)

    return data.truth


def target_mixture_f(data: Data) -> Truth:
    import numpy as np

    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.target_fft.bins + 2 * data.noise_fft.bins:
        raise SonusAIError(f'Invalid num_classes for target_mixture_f truth: {data.config.num_classes}')

    for offset in data.offsets:
        target_f = np.complex64(data.target_fft.execute(data.target_audio[offset:offset + data.frame_size]))
        noise_f = np.complex64(data.noise_fft.execute(data.noise_audio[offset:offset + data.frame_size]))
        mixture_f = target_f + noise_f

        indices = slice(offset, offset + data.frame_size)
        for index in data.zero_based_indices:
            start = index
            stop = start + data.target_fft.bins
            data.truth[indices, start:stop] = np.real(target_f)

            start = stop
            stop = start + data.target_fft.bins
            data.truth[indices, start:stop] = np.imag(target_f)

            start = stop
            stop = start + data.noise_fft.bins
            data.truth[indices, start:stop] = np.real(mixture_f)

            start = stop
            stop = start + data.noise_fft.bins
            data.truth[indices, start:stop] = np.imag(mixture_f)

    return data.truth


def target_swin_f(data: Data) -> Truth:
    import numpy as np

    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.target_fft.bins:
        raise SonusAIError(f'Invalid num_classes for target_swin_f truth: {data.config.num_classes}')

    for offset in data.offsets:
        target_f = np.complex64(
            data.target_fft.execute(np.multiply(data.target_audio[offset:offset + data.frame_size], data.swin)))

        indices = slice(offset, offset + data.frame_size)
        for index in data.zero_based_indices:
            start = index
            stop = start + data.target_fft.bins
            data.truth[indices, start:stop] = np.real(target_f)

            start = stop
            stop = start + data.target_fft.bins
            data.truth[indices, start:stop] = np.imag(target_f)

    return data.truth
