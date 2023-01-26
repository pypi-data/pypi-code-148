# coding: utf-8
import setuptools

#try:
#    import pyhdbpp
#    version = '.'.join(map(str,pyhdbpp.RELEASE))
#except:
#    import traceback
#    traceback.print_exc()
#    version = '0.0.0'

description = "hdb++ python3 API"

if __name__ == "__main__":
    setuptools.setup(
    name="pyhdbpp",
#    version=version,
    license='LGPL-3+',
    packages=setuptools.find_packages(),
    description=description,
    long_description="Extract data from HDB++ Tango Archiving Systems, using either "
    "MariaDB or TimeScaleDB",
    author="Sergi Rubio, Damien Lacoste",
    author_email="info@tango-controls.org",
    )
