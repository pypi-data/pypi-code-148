from setuptools import setup, find_packages



VERSION = '0.0.3'
DESCRIPTION = 'Streaming video data via networks'

# Setting up
setup(
	name="wrapperpkg",
	version=VERSION,
    	author="NeuralNine (Florian Dedov)",
    	author_email="<mail@neuralnine.com>",
    	description=DESCRIPTION,
    	packages=find_packages(),
    	install_requires=[],
        classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]
)
