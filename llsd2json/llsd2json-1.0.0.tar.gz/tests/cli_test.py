import io
import json
import sys
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

import llsd

from llsd2json import cli

LLSD_XML = """<?xml version="1.0" encoding="UTF-8"?>
<llsd>
  <map>
    <key>uuid</key>
    <uuid>67153d5b-3659-afb4-8510-adda2c034649</uuid>
    <key>date</key>
    <date>2006-02-01T14:29:53.43Z</date>
    <key>uri</key>
    <uri>https://example.com</uri>
    <key>binary</key>
    <binary>dGhlIHF1aWNrIGJyb3duIGZveA==</binary>
    <key>real</key>
    <real>1.0</real>
    <key>integer</key>
    <integer>1</integer>
    <key>boolean</key>
    <boolean>1</boolean>
    <key>undefined</key>
    <undef />
    <key>string</key>
    <string>s</string>
  </map>
</llsd>
"""

LLSD_JSON = {
    "uuid": "67153d5b-3659-afb4-8510-adda2c034649",
    "date": "2006-02-01T14:29:53.430000",
    "uri": "https://example.com",
    "binary": "dGhlIHF1aWNrIGJyb3duIGZveA==",
    "real": 1.0,
    "integer": 1,
    "boolean": True,
    "undefined": None,
    "string": "s",
}

# preserve original stdout.buffer.write to use as side effect during tests
stdout_write = sys.stdout.buffer.write


def test_llsd2json():
    with redirect_stdout(io.StringIO()) as stdout:
        cli.llsd2json([LLSD_XML])
    assert json.loads(stdout.getvalue()) == LLSD_JSON


@patch("sys.stdin")
def test_llsd2json_no_input(mock_stdin):
    # workaround for sys.stdin = DontReadFromInput when running under pytest
    mock_stdin.buffer = None
    try:
        cli.llsd2json([])
    except SystemExit as e:
        assert e.code == 2


@patch("sys.stdout")
def test_json2llsd(mock_stdout: MagicMock):
    mock_write: MagicMock = mock_stdout.buffer.write
    mock_write.side_effect = stdout_write
    cli.json2llsd([json.dumps(LLSD_JSON)])
    mock_write.assert_called()
    assert llsd.parse_xml(mock_write.mock_calls[0].args[0]) == LLSD_JSON


@patch("sys.stdin")
def test_json2llsd_no_input(mock_stdin):
    # workaround for sys.stdin = DontReadFromInput when running under pytest
    mock_stdin.buffer = None
    try:
        cli.json2llsd([])
    except SystemExit as e:
        assert e.code == 2


@patch("sys.stdout")
def test_json2llsd_notation(mock_stdout: MagicMock):
    mock_write: MagicMock = mock_stdout.buffer.write
    mock_write.side_effect = stdout_write
    cli.json2llsd([json.dumps(LLSD_JSON), "--format", "notation"])
    mock_write.assert_called()
    assert llsd.parse_notation(mock_write.mock_calls[0].args[0]) == LLSD_JSON


@patch("sys.stdout")
def test_json2llsd_binary(mock_stdout: MagicMock):
    mock_write: MagicMock = mock_stdout.buffer.write
    mock_write.side_effect = stdout_write
    cli.json2llsd([json.dumps(LLSD_JSON), "--format", "binary"])
    mock_write.assert_called()
    assert llsd.parse_binary(mock_write.mock_calls[0].args[0]) == LLSD_JSON


def test_json2llsd_decode_err():
    try:
        cli.json2llsd([""])
    except SystemExit as e:
        assert "JSON decode error:" in str(e)


def test_llsd2json_decode_err():
    try:
        cli.llsd2json(["{"])
    except SystemExit as e:
        assert "LLSD decode error:" in str(e)