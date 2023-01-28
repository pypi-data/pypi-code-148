from setuptools import setup

setup(
    name="fmz",
    version = "2.2.0",
    python_requires='>=3.6.0',
    author='fu-mingzhe',
    author_email='2372769798@qq.com',
    packages=["multi_function"],
    install_requires=[
        "requests",
        "tqdm",
        "retrying",
        "qrcode",
        "pillow",
        "jieba",
        "numpy",
        "wordcloud",
        "pypinyin",
        "pycryptodome",
        "easygui"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
