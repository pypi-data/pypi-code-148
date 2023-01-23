import os
import socket
import json
import websockets # not websocket!!!
import asyncio
from datetime import date
from pydub import AudioSegment
from pydub.playback import play
from num2words import num2words

from say import __version__
from say.TTS import utils

from TTS import __version__ as __TTS_version__

HOST, PORT = "localhost", "5067"
CONFIG = utils.get_config_or_default()

if CONFIG.get('service'):
    HOST = CONFIG['service'].get('host', HOST)
    PORT = CONFIG['service'].get('port', PORT)

def pronounce(wav):
	play(wav)

async def tts(text: str, language, speaker_idx="", style_wav="", host=HOST, port=PORT, save_output=None):
    async with websockets.connect(f"ws://{host}:{port}/api/v1/tts") as ws:
        try:
            j = {
                'text': text,
                'speaker_idx': speaker_idx,
                'style_wav': style_wav,
                'language': language
                }
            await ws.send(json.dumps(j).encode('utf-8', 'ignore'))
            wav = await ws.recv()
            try:
                _wav = AudioSegment(data=wav, sample_width=2, frame_rate=16000, channels=1)
                pronounce(_wav)
                if save_output:
                    _wav.export(save_output, format="wav")
            except Exception as e:
                raise Exception(e)
        except ConnectionRefusedError as e:
            pass
        except Exception as e:
            raise e
        finally:
            await ws.close()

async def _say(text: list[str], language: str, speaker_idx: str = "", style_wav: str = "", save_output: str = "", show_version: bool = False, enable_interpretation: bool = True, disable_interpretation: bool = False, no_newline: bool = False) -> list[str]:
    if style_wav and not os.path.exists(style_wav):
        utils.download_speaker(style_wav)
    
    for _text in text:
        utils.echo(text=_text, show_version=show_version, enable_interpretation=enable_interpretation, disable_interpretation=disable_interpretation, no_newline=no_newline)
        try:
            await tts([_text,], language, speaker_idx=speaker_idx, style_wav=style_wav, save_output=save_output)
        except (ConnectionRefusedError, OSError) as e:
            pass # Server is not active or something
        except Exception as e:
            raise e

    return text

def inflect_version(version, lang, dot="dot"):
    """
    Uses `num2words` to inflect version numbers to say.
    """
    Major, Minor, Bugs = version.split(".")
    _maj = num2words(int(Major), lang=lang)
    _min = num2words(int(Minor), lang=lang)
    _b = num2words(int(Bugs), lang=lang)

    return f"{_maj} {dot}, {_min} {dot}, {_b}"

def say_version(lang, speaker_idx="", style_wav=""):
    if lang == "en":
        _text = [
            f"Say, version {inflect_version(__version__, 'en', dot='dot')}.",
        ]
        language = "en"
    elif lang == "fr":
        _text = [
            f"Dit, version {inflect_version(__version__, 'fr', dot='point')}.",
        ]
        language = "fr-fr"
    else:
        raise NotImplementedError(f"Language {lang} not implemented.")
    
    _show_version = True
    _enable_interpretation = True
    _disable_interpretation = False
    _no_newline = False

    asyncio.run(_say(_text, language, speaker_idx=speaker_idx, style_wav=style_wav, show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline))
    utils.echo(f"Say: version {str(__version__)}", show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline)
    utils.echo(f"Copyright © {str(date.today().year)}, Danny Waser", show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline)
    utils.echo(f"TTS version {__TTS_version__}", show_version=False, enable_interpretation=_enable_interpretation, disable_interpretation=_disable_interpretation, no_newline=_no_newline)
    os.system("/usr/bin/echo --version")