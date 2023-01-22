from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_Kunal_102053007",version="0.2",
description="This is a topsis package of version 0.2",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Kunal Madan",
author_email="kmadan_bemba20@thapar.edu",
packages=['Topsis_Kunal_102053007'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Kunal_102053007.Kunal_102053007:main",
        ]
    }
)

