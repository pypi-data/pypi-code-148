import logging
from .base_utils import *

def setup_logger():
    '''
    Dont set logging in setup.cfg or it will conflict with this
    setup.cfg logging overwrites log file.

    filename=None: in production
    '''
    logging.basicConfig(
        filename=settings.LOG_FILE_PATH,
        format='%(asctime)s-%(process)d-%(levelname)s-%(funcName)s-%(message)s', 
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.INFO)
    log = logging.getLogger(settings.WHICH_LOGGER)
    return log

logger = setup_logger()
