from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Streaming video data via networks'

# Setting up
setup(
	name="fflwkgblk",
	version=VERSION,
    	author="NeuralNine (Florian Dedov)",
    	author_email="<mail@neuralnine.com>",
    	description=DESCRIPTION,
    	packages=find_packages(),
    	install_requires=[],
    	keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    	classifiers=[
        	"Development Status :: 1 - Planning",
        	"Intended Audience :: Developers",
        	"Programming Language :: Python :: 3",
        	"Operating System :: Unix",
        	"Operating System :: MacOS :: MacOS X",
        	"Operating System :: Microsoft :: Windows",
    	]
)