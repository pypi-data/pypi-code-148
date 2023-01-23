import setuptools

setuptools.setup(
    name='dadeschools',
    version='1.0',
    author='Daniel Li',
    author_email='daniel.miami2005@gmail.com',
    description='The Ultimate Dadeschools CLI',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BananaApache/dadeschools',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
        'bs4',
    ],
    scripts=['./bin/main'],
    python_requires='>=3.6'
)