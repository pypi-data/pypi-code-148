from setuptools import setup
from setuptools import find_packages

setup(
    name="emojipasta-cli",
    description="Generate emojipasta from text.",
    readme="./README.md",
    version="1.1.0",
    url="https://github.com/MbBrainz/EmojipastaCLI",
    author="Kevin Galligan",
    author_email="galligankevinp@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    package_data={'': ["*.txt", "*.json"]},
    include_package_data=True,
    install_requires=[
        "emoji",
        "praw>=5.0.0,<6.0.0"
    ],
    entry_points={
    'console_scripts': [
      'emojipasta = emojipasta.__main__:main'
    ]
  }
)

