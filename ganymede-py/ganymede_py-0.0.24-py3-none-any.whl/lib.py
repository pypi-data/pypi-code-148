import hashlib
import os
import time
import tomli

from IPython.display import display, Javascript


def config():
    home_dir = os.path.expanduser('~')

    # Check if file is in new location, use old location if not
    configFileLocation = home_dir + '/configs/config.toml'
    file_exists = os.path.exists(configFileLocation)
    if not file_exists:
        configFileLocation = home_dir + '/config.toml'

    with open(configFileLocation, "rb") as f:
        c = tomli.load(f)
    return c


def save_notebook(file_path):
    start_md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    display(Javascript('IPython.notebook.save_checkpoint();'))
    current_md5 = start_md5

    while start_md5 == current_md5:
        time.sleep(1)
        current_md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
