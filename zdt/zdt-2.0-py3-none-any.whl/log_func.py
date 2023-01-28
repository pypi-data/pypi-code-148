import logging
import os

def log_it(*args):

    '''

    Example usage:  log1 = log_it('a','_b')
    log1.info(f'{ctry} succed')

    '''

    if not os.path.isdir("./logs"):
        os.makedirs("./logs")

    str1 = ''

    for x in args:
        str1+=x

    logging.basicConfig(level=logging.INFO)

    log1 = logging.getLogger(str1)
    #log1.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s -> %(message)s"
    )
    
    file_handler = logging.FileHandler("logs/" + f"{str1}.log")
    file_handler.setFormatter(formatter)
    log1.addHandler(file_handler)

    return log1