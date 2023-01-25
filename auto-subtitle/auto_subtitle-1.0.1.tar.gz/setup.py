from setuptools import setup, find_packages

setup(
    version="1.0.1",
    name="auto_subtitle",
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    py_modules=["auto_subtitle"],
    author="Miguel Piedrafita",
    install_requires=[
        'openai-whisper',
    ],
    description="Automatically generate and embed subtitles into your videos",
    entry_points={
        'console_scripts': ['auto_subtitle=auto_subtitle.cli:main'],
    },
    include_package_data=True,
)
