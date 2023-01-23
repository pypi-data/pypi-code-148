

import os

config_dir = os.path.join(os.environ['HOME'], '.xbridge')

class Config:
    config_dir = config_dir
    files_dir = '.'
    rename_save = True # rename file or dir when save
    
