import setuptools

import pypandoc
pypandoc.download_pandoc()
long_description = pypandoc.convert_file('README.md', 'rst')

setuptools.setup(
    name="pyroadd",
    version="0.0.4",
    autor="nimmadev",
    description="module to add members to telegam group",
    long_description=long_description,
    pakages=["pyrogram", "tgcrypto", "readchar"]
)