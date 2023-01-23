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
import os
from pathlib import Path

import numpy as np
import paddle
import soundfile as sf
import yaml
from paddlespeech.cli.vector import VectorExecutor
from paddlespeech.resource import CommonTaskResource
from paddlespeech.t2s.exps.syn_utils import get_am_inference, get_frontend
from paddlespeech.t2s.exps.syn_utils import get_voc_inference
from paddlespeech.vector.exps.ge2e.audio_processor import SpeakerVerificationPreprocessor
from paddlespeech.vector.models.lstm_speaker_encoder import LSTMSpeakerEncoder
from yacs.config import CfgNode


def gen_random_embed(use_ecapa: bool = False):
    if use_ecapa:
        # Randomly generate numbers of -25 ~ 25, 192 is the dim of spk_emb
        random_spk_emb = (-1 + 2 * np.random.rand(192)) * 25

    # GE2E
    else:
        # Randomly generate numbers of 0 ~ 0.2, 256 is the dim of spk_emb
        random_spk_emb = np.random.rand(256) * 0.5
    random_spk_emb = paddle.to_tensor(random_spk_emb, dtype='float32')
    return random_spk_emb


def voice_cloning(args):
    # Init body.
    if args.am_ckpt is None or args.am_config is None or args.am_stat is None or args.phones_dict is None:
        use_pretrained_am = True
    else:
        use_pretrained_am = False

    task_resource = CommonTaskResource(task='tts')
    task_resource.set_task_model(
        model_tag=args.am + '-en',
        model_type=0,  # am
        skip_download=not use_pretrained_am,
        version=None,  # default version
    )

    if use_pretrained_am:
        am_res_path = task_resource.res_dir
        am_config = os.path.join(am_res_path, task_resource.res_dict['config'])
        am_ckpt = os.path.join(am_res_path,
                               task_resource.res_dict['ckpt'])
        am_stat = os.path.join(
            am_res_path, task_resource.res_dict['speech_stats'])
        phones_dict = os.path.join(
            am_res_path, task_resource.res_dict['phones_dict']) if task_resource.res_dict.get('phones_dict') else None
    else:
        raise NotImplementedError

    tones_dict = None
    if 'tones_dict' in task_resource.res_dict:
        tones_dict = os.path.join(
            am_res_path, task_resource.res_dict['tones_dict'])
        if tones_dict:
            tones_dict = tones_dict

    # for multi speaker fastspeech2
    speaker_dict = None
    if 'speaker_dict' in task_resource.res_dict:
        speaker_dict = os.path.join(am_res_path, task_resource.res_dict['speaker_dict'])

    if args.voc_ckpt is None or args.voc_config is None or args.voc_stat is None:
        use_pretrained_voc = True
    else:
        use_pretrained_voc = False

    task_resource.set_task_model(
        model_tag=args.voc + '-en',
        model_type=1,  # vocoder
        skip_download=not use_pretrained_voc,
        version=None,  # default version
    )

    if use_pretrained_voc:
        voc_res_path = task_resource.voc_res_dir
        voc_config = os.path.join(voc_res_path, task_resource.voc_res_dict['config'])
        voc_ckpt = os.path.join(voc_res_path, task_resource.voc_res_dict['ckpt'])
        voc_stat = os.path.join(voc_res_path, task_resource.voc_res_dict['speech_stats'])
    else:
        raise NotImplementedError()

    with open(am_config) as f:
        am_config = CfgNode(yaml.safe_load(f))
    with open(voc_config) as f:
        voc_config = CfgNode(yaml.safe_load(f))

    output_path = Path(args.output_path)
    input_path = Path(args.input_path)

    frontend = get_frontend(lang='en', phones_dict=phones_dict, tones_dict=tones_dict)

    ############
    sentence = args.text
    input_ids = frontend.get_input_ids(sentence, merge_sentences=False)
    phone_ids = input_ids["phone_ids"][0]
    ###############
    # acoustic model
    am_inference = get_am_inference(
        am=args.am,
        am_config=am_config,
        am_ckpt=am_ckpt,
        am_stat=am_stat,
        phones_dict=phones_dict)

    # vocoder
    voc_inference = get_voc_inference(
        voc=args.voc,
        voc_config=voc_config,
        voc_ckpt=voc_ckpt,
        voc_stat=voc_stat
    )

    if args.use_ecapa:
        vec_executor = VectorExecutor()
        spk_emb = vec_executor(audio_file=input_path, force_yes=True)
        spk_emb = paddle.to_tensor(spk_emb)
    # GE2E
    else:
        p = SpeakerVerificationPreprocessor(
            sampling_rate=16000,
            audio_norm_target_dBFS=-30,
            vad_window_length=30,
            vad_moving_average_width=8,
            vad_max_silence_length=6,
            mel_window_length=25,
            mel_window_step=10,
            n_mels=40,
            partial_n_frames=160,
            min_pad_coverage=0.75,
            partial_overlap_ratio=0.5)

        speaker_encoder = LSTMSpeakerEncoder(n_mels=40, num_layers=3, hidden_size=256, output_size=256)
        speaker_encoder.set_state_dict(paddle.load(args.ge2e_params_path))
        speaker_encoder.eval()
        mel_sequences = p.extract_mel_partials(
            p.preprocess_wav(input_path))
        with paddle.no_grad():
            spk_emb = speaker_encoder.embed_utterance(
                paddle.to_tensor(mel_sequences))
    with paddle.no_grad():
        wav = voc_inference(am_inference(phone_ids, spk_emb=spk_emb))

    sf.write(output_path, wav.numpy(), samplerate=am_config.fs)
