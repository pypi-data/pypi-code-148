import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="alvonOnvif",
    version="0.0.5",
    author="Deepak Singh",
    description="Custom Onvif",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["alvonOnvif"],
    download_url="",
    keywords=["opencv", "onvif", "alvon", "stream", "logging", "onvif-stream"],
    install_requires=["onvif-zeep", "opencv-python"]
)