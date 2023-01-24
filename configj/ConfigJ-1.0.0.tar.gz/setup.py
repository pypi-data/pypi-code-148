from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ConfigJ",
    version="1.0.0",
    author="DancingSnow",
    author_email="1121149616@qq.com",
    description="A json base config lib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DancingSnow0517/ConfigJ",
    project_urls={
        "Bug Tracker": "https://github.com/DancingSnow0517/ConfigJ/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
)