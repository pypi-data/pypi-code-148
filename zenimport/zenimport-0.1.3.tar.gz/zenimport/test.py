from src.importer import Importer
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s",handlers=[logging.StreamHandler()])
im = Importer()
im.levelup()
cur_folder = im.get_current_folder()
logging.info(cur_folder)
    

