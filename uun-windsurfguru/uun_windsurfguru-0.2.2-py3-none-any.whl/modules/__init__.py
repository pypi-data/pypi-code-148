import http.client
import json
import logging
from .WindSurfGuru import WindSurfGuru


def init(config, uuclient):

  def uucmd_get_last_data(code):
    json_data = {
        'code': code
    }
    uucmd = config['uuApp']['uuCmdList']['weatherConditionsGetLast']
    return uuclient.get_request(uucmd, json_data, http_error_level=logging.DEBUG)

  return WindSurfGuru(config["gateway"], uucmd_get_last_data)
