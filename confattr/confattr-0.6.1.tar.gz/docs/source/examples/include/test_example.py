#!../../../../venv/bin/pytest -s

import os
from .example import App

def test__output() -> None:
	app = App()
	path = os.path.dirname(__file__)
	fn = os.path.join(path, 'output.txt')
	with open(fn, 'rb') as f:
		expected = f.read().splitlines()
		assert app.frame.render((51,5)).text == expected
