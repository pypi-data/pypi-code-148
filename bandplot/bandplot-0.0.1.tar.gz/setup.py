from setuptools import setup, find_packages

setup(
    name='bandplot',
    version='0.0.1',
    author='kan',
    author_email='luokan@hrbeu.edu.cn',
    python_requires=">=3.6",
    license='MIT',
    license_files=('LICENSE.txt',),
    platforms=['Unix', 'Windows'],
    keywords='band structure plot',
    description='bandplot: band structure plot from vaspkit result.',
    url='https://github.com/lkccrr/bandplot',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    install_requires=[
        'numpy>=1.22.0',
        'matplotlib>=3.4.0'
    ],
    entry_points={
        'console_scripts': ['bandplot=bandplot.wrapper:main']
    },
    packages=find_packages(),
    include_package_data=True
)