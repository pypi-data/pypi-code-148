from setuptools import setup, find_packages

setup(
    name='TfIdfTransformer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn'
    ],
    author='Oytun',
    author_email='oytunakdeniz@gmail.com',
    description='A Tf-Idf transformer package',
    url='https://github.com/Oytunkdnz/TfIdfTransformer',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)