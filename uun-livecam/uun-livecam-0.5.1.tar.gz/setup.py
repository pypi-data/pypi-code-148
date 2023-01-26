import setuptools
import shutil
import os
import re
from distutils.dir_util import copy_tree

name="uun-livecam"
name_=name.replace('-', '_')

# version from exported binary
pkg_path = os.path.abspath(os.path.dirname(__file__))
with open(f"{pkg_path}/bin/{name}", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setuptools.setup(
    name=name,
    version=version,
    author="(UUN) Tomáš Faikl",
    author_email="tomas.faikl@unicornuniversity.net",
    description="Connect to ONVIF IP webcam, take snapshots and send them to uuApp.",
    url="https://uuapp.plus4u.net/uu-bookkit-maing01/4fa478cb275f4eff9c2c3386660452fd/book/page?code=home",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
    install_requires=[
        "uun-iot >= 0.7.3",
        "onvif-zeep"
    ],
    scripts=[
        "bin/" + name,
        "bin/" + name + "-install"
    ],
    package_data={
        name_: [
            "data/*",
            "data/camera-manual/*",
            "data/camera-manual/snapshots/*",
            "data/camera-manual/wsdl/*",
            "wsdl/*",
        ]
    }

)
