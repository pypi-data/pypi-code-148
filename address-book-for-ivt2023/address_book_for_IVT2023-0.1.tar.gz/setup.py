from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='address_book_for_IVT2023',  # package name
    version='0.1',  # version
    description='address book',  # short description
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.1',
        'Topic :: Text Processing :: Linguistic',
    ],
    url='http://example.com',  # package URL
    author='P_Ihor',
    author_email='igoamigo2000@gmail.com',
    license='MIT',
    install_requires=[
        'Jinja2==2.11.2',
        'MarkupSafe==1.1.1',
        'SQLAlchemy==1.3.19'
    ],  # list of packages this package depends
    packages=find_packages(),  # List of module names that installing
    # this package will provide.
)
