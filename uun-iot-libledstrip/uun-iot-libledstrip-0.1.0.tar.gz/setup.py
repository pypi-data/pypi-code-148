import setuptools
import shutil
import os
import re

version = "0.1.0"
name = "uun-iot-libledstrip"
name_=name.replace('-', '_')

setuptools.setup(
    name=name,
    version=version,
    author="Tomáš Faikl",
    author_email="tomas.faikl@unicornuniversity.net",
    description="Library for managing LED strips for infographic purposes.",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    install_requires=[
        ## default: [dev]
        #"colored",
    ],
    extras_require={
        "neopixel": [
             "rpi_ws281x",
             "adafruit-circuitpython-neopixel",
             "adafruit-blinka"
         ],
        "gpio": [
            "RPi.GPIO"
        ],
        "i2c": [
            "smbus2"
        ],
        "dev": [
            "colored",
        ]
    },
    package_data={
        name_: ["data/*"]
    }
)
