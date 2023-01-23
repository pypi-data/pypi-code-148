# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import io
import os
import sys
from collections import OrderedDict
from typing import Union

import librosa
import numpy as np
import paddle
import soundfile
from paddlespeech.audio.transform.transformation import Transformation
from paddlespeech.cli.log import logger
from paddlespeech.cli.utils import stats_wrapper
from paddlespeech.resource import CommonTaskResource
from paddlespeech.s2t.frontend.featurizer.text_featurizer import TextFeaturizer
from paddlespeech.s2t.utils.utility import UpdateConfig
from yacs.config import CfgNode


class Speech2Text():
    def __init__(self):
        self._inputs = OrderedDict()
        self._outputs = OrderedDict()
        self.task_resource = CommonTaskResource(task='asr')

    def _init_from_path(self,
                        model_type: str = 'transformer_librispeech',
                        # ['transformer_librispeech-en-16k', 'deepspeech2offline_librispeech-en-16k']

                        lang: str = 'en',
                        sample_rate: int = 16000,
                        decode_method: str = 'attention_rescoring',
                        num_decoding_left_chunks: int = -1):
        """
        Init model and other resources from a specific path.
        """
        logger.debug("start to init the model")
        # default max_len: unit:second
        self.max_len = 50
        if hasattr(self, 'model'):
            logger.debug('Model had been initialized.')
            return

        sample_rate_str = '16k' if sample_rate == 16000 else '8k'
        tag = model_type + '-' + lang + '-' + sample_rate_str
        self.task_resource.set_task_model(tag, version=None)
        self.res_path = self.task_resource.res_dir

        self.cfg_path = os.path.join(
            self.res_path, self.task_resource.res_dict['cfg_path'])
        self.ckpt_path = os.path.join(
            self.res_path,
            self.task_resource.res_dict['ckpt_path'] + ".pdparams")
        logger.debug(self.res_path)

        logger.debug(self.cfg_path)
        logger.debug(self.ckpt_path)

        # Init body.
        self.config = CfgNode(new_allowed=True)
        self.config.merge_from_file(self.cfg_path)

        with UpdateConfig(self.config):
            if self.config.spm_model_prefix:
                self.config.spm_model_prefix = os.path.join(
                    self.res_path, self.config.spm_model_prefix)
            self.text_feature = TextFeaturizer(
                unit_type=self.config.unit_type,
                vocab=self.config.vocab_filepath,
                spm_model_prefix=self.config.spm_model_prefix)
            if "conformer" in model_type or "transformer" in model_type:
                self.config.decode.decoding_method = decode_method
                if num_decoding_left_chunks:
                    assert num_decoding_left_chunks == -1 or num_decoding_left_chunks >= 0, "num_decoding_left_chunks should be -1 or >=0"
                    self.config.num_decoding_left_chunks = num_decoding_left_chunks

            else:
                raise Exception("wrong type")
        model_name = model_type[:model_type.rindex(
            '_')]  # model_type: {model_name}_{dataset}
        model_class = self.task_resource.get_model_class(model_name)
        model_conf = self.config
        model = model_class.from_config(model_conf)
        self.model = model
        self.model.eval()

        # load model
        model_dict = paddle.load(self.ckpt_path)
        self.model.set_state_dict(model_dict)

        # compute the max len limit
        # in transformer like model, we may use the subsample rate cnn network
        subsample_rate = self.model.subsampling_rate()
        frame_shift_ms = self.config.preprocess_config.process[0][
                             'n_shift'] / self.config.preprocess_config.process[0]['fs']
        max_len = self.model.encoder.embed.pos_enc.max_len

        if self.config.encoder_conf.get("max_len", None):
            max_len = self.config.encoder_conf.max_len

        self.max_len = frame_shift_ms * max_len * subsample_rate
        logger.debug(
            f"The asr server limit max duration len: {self.max_len}")

    def preprocess(self, input: Union[str, os.PathLike]):
        """
        Input preprocess and return paddle.Tensor stored in self.input.
        Input content can be a text(tts), a file(asr, cls) or a streaming(not supported yet).
        """

        audio_file = input
        if isinstance(audio_file, (str, os.PathLike)):
            logger.debug("Preprocess audio_file:" + audio_file)
        elif isinstance(audio_file, io.BytesIO):
            audio_file.seek(0)

        # Get the object for feature extraction
        logger.debug("get the preprocess conf")
        preprocess_conf = self.config.preprocess_config
        preprocess_args = {"train": False}
        preprocessing = Transformation(preprocess_conf)
        logger.debug("read the audio file")
        audio, audio_sample_rate = soundfile.read(
            audio_file, dtype="int16", always_2d=True)
        if self.change_format:
            if audio.shape[1] >= 2:
                audio = audio.mean(axis=1, dtype=np.int16)
            else:
                audio = audio[:, 0]
            # pcm16 -> pcm 32
            assert (audio.dtype == np.int16)
            audio = audio.astype("float32")
            bits = np.iinfo(np.int16).bits
            audio = audio / (2 ** (bits - 1))

            audio = librosa.resample(
                audio,
                orig_sr=audio_sample_rate,
                target_sr=self.sample_rate)

            # pcm32 -> pcm 16
            assert (audio.dtype == np.float32)
            bits = np.iinfo(np.int16).bits
            audio = audio * (2 ** (bits - 1))
            audio = np.round(audio).astype("int16")
        else:
            audio = audio[:, 0]

        logger.debug(f"audio shape: {audio.shape}")
        # fbank
        audio = preprocessing(audio, **preprocess_args)

        audio_len = paddle.to_tensor(audio.shape[0])
        audio = paddle.to_tensor(audio, dtype='float32').unsqueeze(axis=0)

        self._inputs["audio"] = audio
        self._inputs["audio_len"] = audio_len
        logger.debug(f"audio feat shape: {audio.shape}")

        logger.debug("audio feat process success")

    @paddle.no_grad()
    def infer(self, model_type: str):
        """
        Model inference and result stored in self.output.
        """
        logger.debug("start to infer the model to get the output")
        cfg = self.config.decode
        audio = self._inputs["audio"]
        audio_len = self._inputs["audio_len"]
        logger.debug(f"we will use the transformer like model : {model_type}")
        try:
            result_transcripts = self.model.decode(
                audio,
                audio_len,
                text_feature=self.text_feature,
                decoding_method=cfg.decoding_method,
                beam_size=cfg.beam_size,
                ctc_weight=cfg.ctc_weight,
                decoding_chunk_size=cfg.decoding_chunk_size,
                num_decoding_left_chunks=cfg.num_decoding_left_chunks,
                simulate_streaming=cfg.simulate_streaming)
            self._outputs["result"] = result_transcripts[0][0]
        except Exception as e:
            logger.exception(e)

    def _check(self, audio_file: str, sample_rate: int, force_yes: bool = False):
        self.sample_rate = sample_rate
        if self.sample_rate != 16000 and self.sample_rate != 8000:
            logger.error(
                "invalid sample rate, please input --sr 8000 or --sr 16000")
            return False

        if isinstance(audio_file, (str, os.PathLike)):
            if not os.path.isfile(audio_file):
                logger.error("Please input the right audio file path")
                return False
        elif isinstance(audio_file, io.BytesIO):
            audio_file.seek(0)

        logger.debug("checking the audio file format......")
        try:
            audio, audio_sample_rate = soundfile.read(
                audio_file, dtype="int16", always_2d=True)
            audio_duration = audio.shape[0] / audio_sample_rate
            if audio_duration > self.max_len:
                logger.error(
                    f"Please input audio file less then {self.max_len} seconds.\n"
                )
                return False
        except Exception as e:
            logger.exception(e)
            logger.error(
                f"can not open the audio file, please check the audio file({audio_file}) format is 'wav'. \n \
                 you can try to use sox to change the file format.\n \
                 For example: \n \
                 sample rate: 16k \n \
                 sox input_audio.xx --rate 16k --bits 16 --channels 1 output_audio.wav \n \
                 sample rate: 8k \n \
                 sox input_audio.xx --rate 8k --bits 16 --channels 1 output_audio.wav \n \
                 ")
            return False
        logger.debug("The sample rate is %d" % audio_sample_rate)
        if audio_sample_rate != self.sample_rate:
            logger.warning("The sample rate of the input file is not {}.\n \
                            The program will resample the wav file to {}.\n \
                        ".format(self.sample_rate, self.sample_rate))
            self.change_format = True
        else:
            logger.debug("The audio file format is right")
            self.change_format = False

        return True

    @stats_wrapper
    def __call__(self,
                 audio_file: os.PathLike,
                 model: str = 'transformer_librispeech',
                 lang: str = 'en',
                 sample_rate: int = 16000,
                 config: os.PathLike = None,
                 ckpt_path: os.PathLike = None,
                 decode_method: str = 'attention_rescoring',
                 num_decoding_left_chunks: int = -1,
                 force_yes: bool = False,
                 rtf: bool = False,
                 device='cpu'):
        """
        Python API to call an executor.
        """
        audio_file = os.path.abspath(audio_file)
        paddle.set_device('cpu')
        self._init_from_path(model, lang, sample_rate, decode_method,
                             num_decoding_left_chunks)
        if not self._check(audio_file, sample_rate, force_yes):
            sys.exit(-1)

        self.preprocess(audio_file)
        self.infer(model)
        return self._outputs["result"]
