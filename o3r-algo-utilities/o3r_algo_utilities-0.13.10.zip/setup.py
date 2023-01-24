# needed only for an editable install (pip install -e <dir>)
import setuptools
from pathlib import Path

version = Path(__file__).parent / "VERSION.txt"
if not version.is_file():
    version.write_text("0.0.0")

setuptools.setup()
