from setuptools import setup, find_packages

setup(
    name='pbandplot',
    version='0.0.1.1',
    author='kan',
    author_email='luokan@hrbeu.edu.cn',
    python_requires=">=3.6",
    license='MIT',
    license_files=('LICENSE.txt',),
    platforms=['Unix', 'Windows'],
    keywords='phonopy band structure plot',
    description='pbandplot: phonon band structure plot from phonopy result.',
    url='https://github.com/lkccrr/pbandplot',
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
        'console_scripts': ['pbandplot=pbandplot.wrapper:main']
    },
    packages=find_packages(),
    include_package_data=True
)