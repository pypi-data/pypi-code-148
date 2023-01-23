from say import __version__

from TTS.utils.manage import ModelManager

import os
import asyncio
import urllib.request
import re
import json
import toml
import logging
import threading


from pathlib import Path
from python_shell import Shell
from python_shell.util.streaming import decode_stream

from say import *

def get_config_or_default():
    # Check if conf exist

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as cfg:
            CONFIG = toml.loads(cfg.read())
    else:
        CONFIG = {
            'service': {
                'host': '0.0.0.0',
                'port': '5067'
            },
            'tts': {
                'models': "tts_models/multilingual/multi-dataset/your_tts",
                'language': "fr-fr" if I18N == "fr" else I18N,
                'speaker_wav': f"{ASSISTANT_PATH}/data/{I18N}/TTS/styles/default.wav",
                'is_allowed': False
            }
        }
        Path.mkdir(Path(CONFIG_PATH).parent, exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            f.write(toml.dumps(CONFIG))
    
    return CONFIG

def download_speaker(output_file, lang="en", gender="male", name="default"):
    default_speaker = f"https://gitlab.com/waser-technologies/data/tts/{lang}/voices/-/raw/master/{gender}/{name}.wav"
    urllib.request.urlretrieve(default_speaker, output_file)
    return output_file

def get_speaker(idx=None, wav=None, conf=get_config_or_default()):
    # Get a speaker id or speaker wav
    speaker_id = None
    speaker_wav = None

    if idx:
        speaker_id = idx[0]
    elif wav:
        speaker_wav = wav[0]
    elif conf.get('tts'):
        speaker_id = conf['tts'].get('speaker_id', None)
        speaker_wav = conf['tts'].get('speaker_wav', None)
    
    return speaker_id, speaker_wav

def get_models_name(model_name=None, conf=get_config_or_default()):
    """
    Makes sure Config represent loaded models name.
    """
    _tts_conf = conf.get('tts', None)
    if _tts_conf:
        _tts_models_name = _tts_conf.get('models', None)
        if _tts_models_name:
            if model_name != _tts_models_name:
                conf['tts']['models'] = model_name
                Path.mkdir(Path(CONFIG_PATH).parent, exist_ok=True)
                with open(CONFIG_PATH, 'w') as f:
                    f.write(toml.dumps(conf))
    return model_name

def is_allowed_to_speak(conf=get_config_or_default()):
    _tts_conf = conf.get('tts', False)
    if _tts_conf:
        return _tts_conf.get('is_allowed', False)
    return False

def get_loc_model_path():
	"""
    Get localised models path.
    """
	return Path(__TTS_file__).parent / ".models.json"

manager = ModelManager()

def echo(text="", show_version=False, enable_interpretation=False, disable_interpretation=True, no_newline=False, end="\n"):
    if text:
        if enable_interpretation:
            e = Shell.echo('-e', text)
        else:
            e = Shell.echo(text)
    
        p = decode_stream(e.output)
        print(str(p), end="")
        return p

def get_available_cpu_count():
    """Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    See this https://stackoverflow.com/a/1006301/13561390"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r"(?m)^Cpus_allowed:\s*(.*)$", open("/proc/self/status").read())
        if m:
            res = bin(int(m.group(1).replace(",", ""), 16)).count("1")
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil

        return psutil.cpu_count()  # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf("SC_NPROCESSORS_ONLN"))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ["NUMBER_OF_PROCESSORS"])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime

        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(["sysctl", "-n", "hw.ncpu"], stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open("/proc/cpuinfo").read().count("processor\t:")

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir("/devices/pseudo/")
        res = 0
        for pd in pseudoDevices:
            if re.match(r"^cpuid@[0-9]+$", pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open("/var/run/dmesg.boot").read()
        except IOError:
            dmesgProcess = subprocess.Popen(["dmesg"], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while "\ncpu" + str(res) + ":" in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception("Can not determine number of CPUs on this system")

