# pylint: disable=missing-docstring,line-too-long

from typing import Any, Dict, Optional
import unittest
from unittest.mock import MagicMock, patch
from json import dumps
from soil.dictionary import dictionary


TEST_DICT = {
    "_id": "609bdfe9f5e2c907fa353bca99",
    "content": {"a": "b"},
    "created_at": 1620828137994,
    "language": "es",
    "name": "testdicaaddt",
}

TEST_CONTENT = {"a": "b"}


class MockResponse:  # pylint: disable=too-few-public-methods
    def __init__(self, text: str, status_code: int):
        self.text = text
        self.status_code = status_code

    # def text(self):
    #     return self._text


def mocked_requests_get(
    url: str, *, headers: Optional[Dict[str, str]] = None, timeout: int
) -> MockResponse:
    # pylint: disable=unused-argument
    name = url.split("/")[-2]
    if name == "testdicaaddt":
        return MockResponse(dumps(TEST_DICT), 200)
    return MockResponse("Not found", 404)


def mocked_requests_post(*_args: Any, **kwargs: Any) -> MockResponse:
    assert "json" in kwargs
    assert "language" in kwargs["json"]
    assert "name" in kwargs["json"]
    assert "content" in kwargs["json"]
    return MockResponse(dumps({"status": "created"}), 200)


# Our test case class
class TestDictionary(unittest.TestCase):
    @patch("soil.api.session.get", side_effect=mocked_requests_get)
    def test_get_dictionary(self, mock_get: MagicMock) -> None:

        response = dictionary("testdicaaddt", "ca")
        self.assertEqual(response, TEST_DICT)
        response = dictionary("testdicaaddt", "en")
        self.assertEqual(response, TEST_DICT)

        self.assertEqual(len(mock_get.call_args_list), 2)

    @patch("soil.api.session.patch", side_effect=mocked_requests_post)
    @patch("soil.api.session.post", side_effect=mocked_requests_post)
    @patch("soil.api.session.get", side_effect=mocked_requests_get)
    def test_create_existing_dictionary_no_lang(
        self, mock_get: MagicMock, mock_post: MagicMock, mock_patch: MagicMock
    ) -> None:
        response = dictionary("testdicaaddt", "ca", TEST_CONTENT)
        assert response == {"status": "created"}
        self.assertEqual(len(mock_get.call_args_list), 1)
        self.assertEqual(len(mock_post.call_args_list), 1)
        self.assertEqual(len(mock_patch.call_args_list), 0)

    @patch("soil.api.session.patch", side_effect=mocked_requests_post)
    @patch("soil.api.session.post", side_effect=mocked_requests_post)
    @patch("soil.api.session.get", side_effect=mocked_requests_get)
    def test_create_existing_dictionary_lang(
        self, mock_get: MagicMock, mock_post: MagicMock, mock_patch: MagicMock
    ) -> None:
        response = dictionary("testdicaaddt", "es", TEST_CONTENT)
        assert response == {"status": "created"}
        self.assertEqual(len(mock_get.call_args_list), 1)
        self.assertEqual(len(mock_post.call_args_list), 0)
        self.assertEqual(len(mock_patch.call_args_list), 1)

    @patch("soil.api.session.patch", side_effect=mocked_requests_post)
    @patch("soil.api.session.post", side_effect=mocked_requests_post)
    @patch("soil.api.session.get", side_effect=mocked_requests_get)
    def test_create_nonexisting_dictionary(
        self, mock_get: MagicMock, mock_post: MagicMock, mock_patch: MagicMock
    ) -> None:
        response = dictionary("testdicaaddtaaa", "es", TEST_CONTENT)
        assert response == {"status": "created"}
        self.assertEqual(len(mock_get.call_args_list), 1)
        self.assertEqual(len(mock_post.call_args_list), 1)
        self.assertEqual(len(mock_patch.call_args_list), 0)
