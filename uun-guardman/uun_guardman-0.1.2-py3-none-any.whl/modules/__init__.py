import http.client
import json
import logging
from .GuardMan import GuardMan

def init(config, uuclient):
    
    def uucmd_get_progress_data(code):
        json_data = {
            'code': code
        }
        uucmd = config['uuApp']['uuCmdList']['guardManProgressGet']
        return uuclient.get_request(uucmd, json_data, http_error_level=logging.DEBUG)

    return GuardMan(config["gateway"], uucmd_get_progress_data)
