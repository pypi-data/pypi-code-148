from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name= "supervisedML",
    version= "0.0.1",
    description= "machine learning supervised models for python with accuracy metrics",
    url= "",
    author= "Mohga Emam",
    author_email= "mohgasolimanemam@gmail.com",
    license= "MIT",
    classifiers=classifiers,
    keywords= ['machine learning', 'regression', 'classification', 'supervised learning'],
    install_requires= ['numpy', 'scikit-learn']
)