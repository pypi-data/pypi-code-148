from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name='easy_m3u8',  # 项目名
    packages=['easy_m3u8'],  # 项目名
    version='2.0',  # 版本号
    install_requires=[  # 依赖列表
        "requests",
        "pycryptodome"
    ],
    description="下载m3u8视频，并转码为mp4。",
    long_description=readme,
    long_description_content_type="text/markdown",
    data_files=[("", ["README.md"])],
    entry_points={
        'console_scripts': [
            'm3u8 = easy_m3u8.core:cmd',
        ]
    }
)
