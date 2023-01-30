from setuptools import setup

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name = 'recsagents23',
    version='1.0.1',
    description='some package',
    py_modules=["ragents"],
    install_requires = [
        'pandas',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'tqdm',
        'helperagent==4.0.0',
        'datetime',
        'xgboost',
        'statsmodels',
        'interpret',
        'shap',
        'entsoe-py'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev":[
            "pytest",
        ],
    },
)