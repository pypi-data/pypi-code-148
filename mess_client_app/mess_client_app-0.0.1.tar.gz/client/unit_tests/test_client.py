import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
import unittest
from pack_client.client import create_presence, process_ans
from common.variables import RESPONSE, ERROR, ACTION, TIME, USER, ACCOUNT_NAME


class TestClient(unittest.TestCase):
    """тестируем функции create_presence и process_ans модуля client.py"""

    err = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok = {RESPONSE: 200}
    value_err = {}

    def test_create_presence(self):
        """ошибка если был сгенерирован некорректный запрос"""
        out = create_presence()
        out[TIME] = 5
        print(out)
        self.assertEqual(out, {ACTION: 'presence', TIME: 5, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_process_ans_400(self):
        """проверяет разбор сгенерированного сервером ответа 400. """
        self.assertEqual(process_ans(self.err), '400 : Bad Request')

    def test_process_ans_200(self):
        """проверяет разбор сгенерированного сервером ответа 200"""
        self.assertEqual(process_ans(self.ok), '200 : OK')

    def test_process_err(self):
        """проверяет разбор сгенерированного сервером исключения ValueError"""
        with self.assertRaises(Exception):
            process_ans(self.value_err)
