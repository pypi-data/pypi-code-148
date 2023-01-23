
from ..sequencer.sequencer_data import Wave, AcquisitionBins, AcquisitionWeight
from ..lang.exceptions import Q1TypeError

class GeneratorData:
    def __init__(self):
        self.waveforms = {}
        self.weights = {}
        self.acquisitions = {}

    def translate_wave(self, wave):
        if not isinstance(wave, Wave):
            raise Q1TypeError(f'Unsupported type for wave: {wave}')

        if wave.name not in self.waveforms:
            self.waveforms[wave.name] = {
                    'data':list(wave.data),
                    'index':len(self.waveforms)
                    }

        return self.waveforms[wave.name]['index']

    def translate_acquisition(self, acquisition):
        if not isinstance(acquisition, AcquisitionBins):
            raise Q1TypeError(f'Unsupported type for acquisition: {acquisition}')

        if acquisition.name not in self.acquisitions:
            self.acquisitions[acquisition.name] = {
                    'num_bins': acquisition.num_bins,
                    'index': len(self.acquisitions),
                    }

        return self.acquisitions[acquisition.name]['index']

    def translate_weight(self, weight):
        if not isinstance(weight, AcquisitionWeight):
            raise Q1TypeError(f'Unsupported type for weight: {weight}')

        if weight.name not in self.weights:
            self.weights[weight.name] = {
                    'data': list(weight.data),
                    'index': len(self.weights),
                    }

        return self.weights[weight.name]['index']

    def get_data_dict(self):
        return {
                'waveforms': self.waveforms,
                'weights': self.weights,
                'acquisitions': self.acquisitions,
                }
