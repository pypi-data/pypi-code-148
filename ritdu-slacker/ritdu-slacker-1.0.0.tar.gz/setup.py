from setuptools import setup, find_packages
from distutils.util import convert_path

with open("README.md", "r") as fh:
    long_description = fh.read()

main_ns = {}
ver_path = convert_path("ritdu_slacker/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

# automatically captured required modules for install_requires in requirements.txt
with open(convert_path("requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")
    install_requires = [
        x.strip()
        for x in all_reqs
        if ("git+" not in x) and (not x.startswith("#")) and (not x.startswith("-"))
    ]
    dependency_links = [
        x.strip().replace("git+", "") for x in all_reqs if "git+" not in x
    ]

setup(
    name="ritdu-slacker",
    version=main_ns["__version__"],
    author="Ringier Tech",
    author_email="tools@ringier.co.za",
    description="Simple internal Slack API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RingierIMU/ritdu-slacker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        "console_scripts": [
            "ritdu-slacker=ritdu_slacker.__main__:main",
        ],
    },
)
