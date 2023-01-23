# pylint: disable=missing-docstring
import unittest
from unittest.mock import patch, Mock, call
from soil.finder import _upload_modules


def _mock_file_generator(file_name: str, folder: str = "") -> Mock:
    mock = Mock(name=file_name)
    mock.read_text.return_value = file_name
    mock.__str__ = lambda _: f"{folder}/{file_name}"
    return mock


class TestFinder(unittest.TestCase):
    @patch("soil.finder.api")
    @patch("soil.finder.Path")
    def test_upload_modules(self, mock_path: Mock, mock_api: Mock):

        mock_api.get_modules.return_value = [
            {"name": "apis.test1", "hash": "1111"},
            {"name": "apis.test2", "hash": "2222"},
            {
                "name": "apis.test.apis_file1",
                "hash": "e836da06f84039b439725d2dc461aa21a75daa06852f41505c21ae9cfd46bec3",
            },
            {"name": "arum.arum_file1", "hash": "5555"},
        ]
        venv = Mock()
        venv.name = ".venv"
        venv.is_dir.return_value = True
        venv.rglob.return_value = [_mock_file_generator("venv_file1.py")]
        test = Mock()
        test.name = "test"
        test.is_dir.return_value = True
        test.rglob.return_value = [_mock_file_generator("test_file1.py")]
        file_py = Mock()
        file_py.name = "abc.py"
        file_py.is_dir.return_value = False
        apis = Mock()
        apis.name = "apis"
        apis.is_dir.return_value = True
        apis.rglob.return_value = [_mock_file_generator("apis_file1.py", "apis/test")]
        arum = Mock()
        arum.name = "arum"
        arum.is_dir.return_value = True
        arum.rglob.return_value = [_mock_file_generator("arum_file1.py", "arum")]

        mock_path().glob.return_value = [venv, test, file_py, apis, arum]

        _upload_modules()

        self.assertListEqual(
            mock_api.upload_module.call_args_list,
            [
                call(
                    module_name="arum.arum_file1",
                    code="arum_file1.py",
                    is_package=False,
                )
            ],
        )
