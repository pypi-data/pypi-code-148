import unittest
from pathlib import Path
from oceansoundscape.raven import BLEDParser
from oceansoundscape.spectrogram import conf, utils, denoise
from oceansoundscape import testdata
import soundfile as sf
import tempfile

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

class TestSpectrogram(unittest.TestCase):

    def test_blue_a(self):
        blue_conf = conf.CONF_DICT['blueA']
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with pkg_resources.path(testdata, "MARS-20150910T000000Z-2kHz.wav") as w:
                with pkg_resources.path(testdata, "MARS-20150910T000000Z-2kHz.wav.Table01.txt") as b:
                    x, sample_rate = sf.read(w, dtype='float32')
                    print(f"Found {sample_rate} {len(x)} samples")
                    self.assertEqual(len(x), 1201200)
                    parser = BLEDParser(b, blue_conf, len(x), sample_rate)
                    print(f'Denoising {b}')
                    cache = denoise.PCENSmooth(temp_path / 'MARS-20150910T000000Z-2kHz.wav.Table01.txt.hdf', parser, blue_conf, x, sample_rate)
                    call_width = int(blue_conf['duration_secs'] * sample_rate)
                    num_fft = blue_conf['num_fft']
                    hop_length = round(num_fft * (1 - conf.OVERLAP))
                    num_processed = 1

                    for row, item in sorted(parser.data.iterrows()):
                        try:
                            if item.has_label:
                                data = cache.get_data(item.Selection)
                                start = int(call_width / hop_length)
                                end = int(2 * call_width / hop_length)

                                # subset the call, leaving off the padding for PCEN
                                subset_data = data[:, start:end]

                                # save to a denoised color image
                                utils.ImageUtils.colorizeDenoise(subset_data, temp_path / Path(item.image_filename))

                                print(f'Processed row {row} total processed {num_processed} {item.image_filename} ')
                                num_processed += 1
                        except Exception as ex:
                            print(ex)
                            continue
                    self.assertEqual(num_processed, 3)
        print('Done')

if __name__ == '__main__':
    unittest.main()
