import os.path
import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

setuptools.setup(
    name="chemspace_vis",
    version="1.1.0",
    author="Olivier Mailhot",
    description="Chemspace visualizer",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gregorpatof/chemspace_vis_package",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['rdkit', 'numpy>=1.20.0', 'matplotlib', 'scikit-learn>=1.2.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
