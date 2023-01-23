import os
import io
import glob
import logging
import json
import re

import numpy as np

#import TTS Model

from timeit import default_timer as timer
from num2words import num2words

from say.TTS import audio, utils
from TTS.utils.synthesizer import Synthesizer

def load_models(
        model_path,
        config_path,
        speakers_file_path,
        vocoder_path,
        vocoder_config_path,
        use_cuda,
        tts_languages_file=None,
        encoder_checkpoint="",
        encoder_config="",
    ):
    """
    Loads TTS models in memory.
    Returns: List[synthesizer, use_multi_speaker, speaker_manager, use_gst]
    """
    model_load_start = timer()
    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        tts_speakers_file=speakers_file_path,
        tts_languages_file=None,
        vocoder_checkpoint=vocoder_path,
        vocoder_config=vocoder_config_path,
        encoder_checkpoint="",
        encoder_config="",
        use_cuda=use_cuda,
    )
    model_load_end = timer() - model_load_start
    logging.debug("Loaded synthesizer in %0.3fs." % (model_load_end))

    speaker_manager_load_start = timer()
    use_multi_speaker = hasattr(synthesizer.tts_model, "num_speakers") and (
        synthesizer.tts_model.num_speakers > 1 or synthesizer.tts_speakers_file is not None
    )

    speaker_manager = getattr(synthesizer.tts_model, "speaker_manager", None)
    # TODO: set this from SpeakerManager
    use_gst = synthesizer.tts_config.get("use_gst", False)
    speaker_manager_load_end = timer() - speaker_manager_load_start
    logging.debug('Loaded speaker manager in %0.3fs.' % (speaker_manager_load_end))

    return [synthesizer, use_multi_speaker, speaker_manager, use_gst]


class TTS:

    def __init__(self, synthesizer, use_multi_speaker, speaker_manager, use_gst):
        self.synthesizer = synthesizer
        self.use_multi_speaker = use_multi_speaker
        self.speaker_manager = speaker_manager
        self.use_gst = use_gst
    
    def style_wav_uri_to_dict(self, style_wav):
        """Transform an uri style_wav, in either a string (path to wav file to be use for style transfer)
        or a dict (gst tokens/values to be use for styling)
        Args:
            style_wav (str): uri
        Returns:
            Union[str, dict]: path to file (str) or gst style (dict)
        """
        if style_wav:
            if os.path.isfile(style_wav) and style_wav.endswith(".wav"):
                return style_wav  # style_wav is a .wav file located on the server

            style_wav = json.loads(style_wav)
            return style_wav  # style_wav is a gst dictionary with {token1_id : token1_weigth, ...}
        return None

    def fetch_floats_from_str(self, text):
        l = []
        for t in text.split():
            try:
                l.append(float(t))
            except ValueError:
                pass
        return l

    def convert_num2words(self, sentences: str, language):
        _sentences = sentences
        if re.search(r"[0-9]", _sentences) is not None:
            nums = self.fetch_floats_from_str(_sentences)
            for num in nums:
                n = str(num)
                w = num2words(num, lang=language)
                print(f"Found number: {n}")
                print(f"Replacing it with: {w}")
                _sentences = _sentences.replace(n, w)
                _sentences = _sentences.replace(str(int(num)), w)
        print(f"Converted {_sentences=}")
        return _sentences

    '''
    Run Inference on input audio
    '''
    def tts(self, text: str, language, speaker_idx, style_wav):
        # Run TTS
        style_wav = self.style_wav_uri_to_dict(style_wav)
        wavs = self.synthesizer.tts(text, language_name=language, speaker_wav=style_wav)
        out = io.BytesIO()
        self.synthesizer.save_wav(wavs, out)
        
        return out

    def run(self, text: list[str], language, speaker_idx, style_wav):
        _t = self.convert_num2words(" ".join(text), language.split("-")[0])
        if language.lower() == "fr":
            language = "fr-fr"
        
        return self.tts(_t, language, speaker_idx, style_wav)

class Response:
    def __init__(self, audio_bin):
        self.wav_bytes = audio_bin
    
    def to_bytes(self):
        return self.wav_bytes


class Error:
    def __init__(self, message):
        self.message = message
    
    def to_bytes(self):
        return self.message.encode('utf-8')

