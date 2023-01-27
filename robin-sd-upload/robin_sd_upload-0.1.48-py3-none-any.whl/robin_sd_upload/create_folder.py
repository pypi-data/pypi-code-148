import os
import logging

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        logging.info("Folder created: " + folder)
        logging.info("Folder path: " + os.path.abspath(folder))
        logging.info('try to run script again')
        exit()
    else:
        logging.info("Folder exists: " + folder)