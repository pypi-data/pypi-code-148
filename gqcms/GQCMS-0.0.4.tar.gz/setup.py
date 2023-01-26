import setuptools

setuptools.setup(
    name="GQCMS",
    version="0.0.4",
    author="ruvdsti and xwieme",
    description="A computational chemistry package",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "numpy==1.21.0", "pandas==1.5.1", "matplotlib==3.6.2", "scipy==1.9.3", "plotly==5.11.0", "seaborn==0.12.1", "nbformat", "ipython", "jupyter"
    ],
    package_dir={"": "."},
    packages=setuptools.find_namespace_packages(where="."),
    python_requires=">= 3.6",
)
