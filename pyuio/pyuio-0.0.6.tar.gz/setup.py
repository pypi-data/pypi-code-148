from setuptools import setup, Extension
from pathlib import Path

root= Path(__file__).parent
long_description = (root / "README.md").read_text()

setup(
	name="pyuio",
	version="0.0.6",
	description="A package to expose the Linux Userspace IO to python",
	url="https://github.com/GOcontroll/pyuio",
	author="Maud Spierings",
	author_email="maud_spierings@hotmail.com",
	license="GLP V2.0",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=["pyuio"],
	ext_modules=[Extension("pyuiolib", ["pyuio/pyuiolib.c"])],
	install_requires=[],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python :: 3",
	],
)