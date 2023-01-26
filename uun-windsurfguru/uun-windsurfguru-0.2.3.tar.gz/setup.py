import setuptools
import shutil
import os
import re

name = "uun-windsurfguru"
name_=name.replace('-', '_')

# version from exported binary
pkg_path = os.path.abspath(os.path.dirname(__file__))
with open(f"{pkg_path}/bin/{name}", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setuptools.setup(
    name=name,
    version=version,
    author="(UUN) Tomáš Faikl & Marek Beránek",
    author_email="tomas.faikl@unicornuniversity.net",
    description="Display wind surf conditions on a colorful LED strip.",
    url="https://uuapp.plus4u.net/uu-bookkit-maing01/c145b7fe6d754775b71e196b3fbb9a6a/book/page?code=64720442",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
    install_requires=[
        "uun-iot >= 0.8.2",
        "uun-iot-libledstrip >= 0.2.3"
    ],
    extras_require={
        "neopixel": [
            "uun-iot-libledstrip[neopixel] >= 0.2.3",
        ],
        "gpio": [
            "uun-iot-libledstrip[gpio] >= 0.2.3",
        ],
        "dev": [
            "uun-iot-libledstrip[dev] >= 0.2.3",
        ]
    },
    scripts=[
        "bin/" + name,
        "bin/" + name + "-install",
        "bin/" + name + "-setup"
    ],
    package_data={
        name_: ["data/*"]
    }
)
