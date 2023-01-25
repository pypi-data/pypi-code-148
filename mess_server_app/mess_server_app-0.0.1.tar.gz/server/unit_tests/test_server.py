import os
import sys
sys.path.append(os.path.join(os.getcwd(), '../../HW'))
import unittest
from common.variables import RESPONSE, ERROR
from pack_server.server import process_client_message


class TestServer(unittest.TestCase):
    """тестируем функцию process_client_message модуля server.py"""

    err = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok = {RESPONSE: 200}

    def test_no_action(self):
        """ошибка если не указан ACTION"""
        self.assertEqual(process_client_message({'time': 15.1, 'user': {'account_name': 'Guest'}}), self.err)

    def test_no_time(self):
        """ошибка если не указано время"""
        self.assertEqual(process_client_message({'ACTION': 'presence', 'user': {'account_name': 'Guest'}}), self.err)

    def test_no_user(self):
        """ошибка если не указан пользователь"""
        self.assertEqual(process_client_message({'ACTION': 'presence', 'time': 15.1}), self.err)

    def test_user_is_not_guest(self):
        """ошибка если пользователь не Guest"""
        self.assertEqual(process_client_message({'ACTION': 'presence', 'user': {'account_name': 'NotGuest'}}), self.err)

    def test_not_presense(self):
        """ошибка если action не presence"""
        self.assertEqual(process_client_message({'ACTION': 'not_presence', 'user': {'account_name': 'Guest'}}), self.err)


if __name__ == '__main__':
    unittest.main()
