import sys
import logging
from pathlib import Path
from string import Template
import inspect
import os

class Importer:
    def __init__(self):
        self.import_msg = Template('appending folder $folder')
        frame = inspect.stack()[1]
        pframe = frame[0].f_code.co_filename
        self.current_folder = str(Path(pframe).parent.resolve())
        self.parent_folder = str(Path(pframe).parent.resolve().parent.resolve())
    
    def levelup(self):
        logging.info(self.import_msg.substitute(folder=self.parent_folder))
        sys.path.append(self.parent_folder)
        
    def get_current_folder(self):
        return self.current_folder


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s",handlers=[logging.StreamHandler()])
    im = Importer()
    im.levelup()
    cur_folder = im.get_current_folder()
    logging.info(cur_folder)
    