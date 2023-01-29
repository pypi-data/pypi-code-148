import unittest
import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)
from win32path.win32path import Win32Path


class TestWin32Path(unittest.TestCase):
    def setUp(self):
        self.win32path = Win32Path()
        self.test_path = 'C:\\Users\\testuser\\Desktop'
        self.test_key = 'test'

    def test_list(self):
        self.win32path.set_path(self.test_key, self.test_path)
        paths = self.win32path.list_paths()
        self.assertIn(self.test_path, paths.values())

    def test_get_path(self):
        self.win32path.set_path(self.test_key, self.test_path)
        self.assertEqual(self.win32path.get_path(self.test_key), self.test_path)

    def test_set_path(self):
        self.win32path.set_path(self.test_key, self.test_path)
        self.assertEqual(self.win32path.get_path(self.test_key), self.test_path)

    def test_update_path(self):
        self.win32path.set_path(self.test_key, self.test_path)
        new_path = 'C:\\Users\\testuser\\Downloads'
        self.win32path.update_path(self.test_key, new_path)
        self.assertEqual(self.win32path.get_path(self.test_key), new_path)

    def test_delete_path(self):
        self.win32path.set_path(self.test_key, self.test_path)
        self.win32path.delete_path(self.test_key)
        self.assertIsNone(self.win32path.get_path(self.test_key))

    def tearDown(self):
        if os.path.exists(self.win32path.paths_file):
            os.remove(self.win32path.paths_file)

if __name__ == '__main__':
    unittest.main()
