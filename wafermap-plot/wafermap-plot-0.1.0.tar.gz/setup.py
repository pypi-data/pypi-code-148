from setuptools import setup

version = "0.1.0"

setup(
    name="wafermap-plot",
    version=version,
    packages=["wafermap_plot"],
    install_requires=["numpy", "matplotlib"],
    license="MIT",
    author="Maxime MARTIN",
    author_email="maxime.martin02@hotmail.fr",
    description="A project to plot wafermaps",
    url="https://github.com/Impro02/wafermap-plot",
    download_url="https://github.com/Impro02/wafermap-plot/archive/refs/tags/%s.tar.gz"
    % version,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
