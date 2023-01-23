import os, sys
import asyncio
from say.main import main


USERNAME = os.environ.get('USERNAME', 'Unknown')
HOME = "/home/%s" % USERNAME
I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))

def run():
    import argparse

    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ("oui", "yes", "true", "t", "o", "y", "1"):
            return True
        if v.lower() in ("non", "no", "false", "f", "n", "0"):
            return False
        raise argparse.ArgumentTypeError("Boolean value expected.")

    parser = argparse.ArgumentParser(description="Same as echo but with Text-To-Speech.")

    # This is here so that you can alias echo to say in your favorite shell.
    # $ alias echo='say'
    parser.add_argument('-n', '--n', action="store_true", help="do not output the trailing newline")
    parser.add_argument('-e', '--e', action="store_true", help="enable interpretation of backslash escapes")
    parser.add_argument('-E', '--E', action="store_true", help="disable interpretation of backslash escapes (default)")
    parser.add_argument('-v', '--version', action='store_true', help="output version information and exit")
    # This is here for the TTS client
    parser.add_argument('-L', '--lang', type=str, help=("Language to be spoken (default: $LANG)"), default=I18N)
    parser.add_argument(
        "--out_path",
        type=str,
        required=False,
        help="Output wav file path.",
    )
    # This is here so you can choose the TTS and vocoder models for the server.
    parser.add_argument(
        "--list_models",
        type=str2bool,
        nargs="?",
        const=True,
        default=False,
        help="list available pre-trained tts and vocoder models.",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="tts_models/multilingual/multi-dataset/your_tts",
        help="Name of one of the pre-trained tts models in format <language>/<dataset>/<model_name>",
    )
    parser.add_argument("--vocoder_name", type=str, default=None, help="name of one of the released vocoder models.")

    # Args for running custom models
    parser.add_argument("--config_path", default=None, type=str, help="Path to model config file.")
    parser.add_argument(
        "--model_path",
        type=str,
        default=None,
        help="Path to model file.",
    )
    parser.add_argument(
        "--vocoder_path",
        type=str,
        help="Path to vocoder model file. If it is not defined, model uses GL as vocoder. Please make sure that you installed vocoder library before (WaveRNN).",
        default=None,
    )
    parser.add_argument("--vocoder_config_path", type=str, help="Path to vocoder model config file.", default=None)
    # parser.add_argument(
    #     "--language_idx",
    #     type=str,
    #     help="Target language ID for a multi-lingual TTS model.",
    #     default=None,
    # )
    # parser.add_argument(
    #     "--list_language_idxs",
    #     help="List available language ids for the defined multi-lingual model.",
    #     type=str2bool,
    #     nargs="?",
    #     const=True,
    #     default=False,
    # )
    parser.add_argument(
        "--speaker_idx",
        type=str,
        help="Target speaker ID for a multi-speaker TTS model.",
        default=None,
    )
    # parser.add_argument(
    #     "--list_speaker_idxs",
    #     help="List available speaker ids for the defined multi-speaker model.",
    #     type=str2bool,
    #     nargs="?",
    #     const=True,
    #     default=False,
    # )
    parser.add_argument(
        "--speaker_wav",
        nargs="+",
        help="wav file(s) to condition a multi-speaker TTS model with a Speaker Encoder. You can give multiple file paths. The d_vectors is computed as their average.",
        default=None,
    )
    parser.add_argument("--speakers_file_path", type=str, help="JSON file for multi-speaker model.", default=None)
    parser.add_argument("--use_cuda", type=str2bool, default=False, help="true to use CUDA.")
    parser.add_argument("--debug", type=str2bool, default=False, help="true to enable debug mode.")
    
    # This is really what we need.
    parser.add_argument('text', type=str, help="Text to be said.", nargs="*")
    ARGS = parser.parse_args()
    try:
        main(ARGS)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
   run()