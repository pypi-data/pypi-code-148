import setuptools

from WeiLanZouCloud.api import version

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="weilanzou-api",
    version=version,
    author="Acloudtwei",
    author_email="1559295172@qq.com",
    description="Fixed the old version of LanZouCloud API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acloudtwei/WeiLanZouCloud-API",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests==2.28.1",
        "requests_toolbelt==0.9.1",
        "fake_useragent==0.1.11"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
