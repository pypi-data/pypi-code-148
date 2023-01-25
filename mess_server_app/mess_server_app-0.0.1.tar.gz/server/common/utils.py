"""Утилиты"""

import json
import sys
sys.path.append('../../HW/')
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from common.decos import log


@log
def get_message(client_sock):
    """
    Утилита приёма и декодирования сообщения. Принимает аргументом объект абстрактного сокета.
    принимает сообщение максимальной длины, проверяет байты ли это. Если байты - переводит в строку json,
    а из нее - словарь, если принято что-то другое отдаёт ошибку значения
    """
    encoded_response = client_sock.recv(MAX_PACKAGE_LENGTH)
    # if isinstance(encoded_response, bytes):
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения. Принимает целевой сокет и словарь.
    Словарь перводит в json, потом в байты и отправляет его в целевой сокет.
    """
    # if not isinstance(message, dict):
    #     raise ValueError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
