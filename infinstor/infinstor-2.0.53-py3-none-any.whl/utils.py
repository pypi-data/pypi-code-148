import logging
import json
import os

###############
#  This is a leaf module in this python package.  So do not depend on (import) any other modules from this package here, to avoid a module circular dependency
##############

def _read_infinstor_config_json_key(jsonkey:str):
    infin_token_dir:str = None
    if 'INFINSTOR_TOKEN_FILE_DIR' in os.environ:
        infin_token_dir = os.environ['INFINSTOR_TOKEN_FILE_DIR']
    else:
        if 'MLFLOW_CONCURRENT_URI' in os.environ:
            infin_token_dir= os.path.join(os.path.expanduser("~"), ".concurrent")
        else:
            infin_token_dir = os.path.join(os.path.expanduser("~"), ".infinstor")
    
    keyval = None
    # if token file is stored in memory (PARALLELS_REFRESH_TOKEN or INFINSTOR_REFRESH_TOKEN), then we pretend as if config.json doesn't exist: always return None value for any key
    if infin_token_dir:
        config_json_path = os.path.join(infin_token_dir,'config.json')
        if os.path.exists(config_json_path): 
            with open(config_json_path, 'r') as fh:
                config_json:dict = json.load(fh)
                keyval = config_json.get(jsonkey, None)
    return keyval

def _get_log_level_from_config_json(module_name:str) -> int:
    """
    Get the loglevel (integer) that correpsonds to the specified module_name, by looking into ~/.infinstor/config.json
    """
    
    loglevel_str:str = _read_infinstor_config_json_key('loglevel.' + module_name)
    
    loglevel_int = logging.INFO
    # if config.json has loglevel defined for the specified module    
    if loglevel_str:
        loglevel_int:int = getattr(logging, loglevel_str.upper(), None)
    
    return loglevel_int

def get_logger(name:str) -> logging.Logger:
    loglevel_int:int = _get_log_level_from_config_json(name)
    #print(f"logger={name} --> loglevel_int={loglevel_int}", flush=True)
    
    # if it is the root logger, initialize it 
    if name == 'root': 
        # do not use force=True since it is only supported in Python 3.8 and higher.  Python 3.7 does not support it.
        logging.basicConfig(level=loglevel_int, format="%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s")
        if loglevel_int == logging.DEBUG:
            from http.client import HTTPConnection
            HTTPConnection.debuglevel = 1
            
    logger = logging.getLogger(name)
    if loglevel_int:
        logger.setLevel(loglevel_int)
    
    return logger
