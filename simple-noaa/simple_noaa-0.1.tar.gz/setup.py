from setuptools import setup, find_packages

# package information
setup(
    name='simple_NOAA',
    version='0.1',
    author='Devin Shaw',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/mypackage',
    description='simple_NOAA allows for streamlined access to NOAA datasets',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pandas',
        'requests',
        'io',
        'shapely'
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='NOAA Climate Data'
)
