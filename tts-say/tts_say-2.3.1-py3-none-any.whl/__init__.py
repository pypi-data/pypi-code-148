import os

__version__ = "2.3.1"

I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))

USERNAME = os.environ.get("USERNAME", 'root')
HOME = f"/home/{USERNAME}" if USERNAME != "root" else "/root"
ASSISTANT_PATH = f"{HOME}/.assistant" if USERNAME != "root" else "/usr/share/assistant"
CONFIG_PATH = f"{ASSISTANT_PATH}/tts.toml"