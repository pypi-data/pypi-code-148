import os.path
import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

setuptools.setup(
    name="chemspace_vis",
    version="0.1.2",
    author="Olivier Mailhot",
    description="Chemspace visualizer",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gregorpatof/chemspace_vis_package",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['rdkit', 'numpy', 'matplotlib', 'scikit-learn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
