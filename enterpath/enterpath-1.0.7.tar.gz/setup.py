from setuptools import setup, find_packages

setup(
    name='enterpath',
    version='1.0.7',
    description="Auto enter path function",
    long_description=open('README.md').read(),
    include_package_data=True,
    author='Lucy Situ',
    author_email='lucy.situ@byd.com',
    maintainer='Lucy Situ',
    maintainer_email='lucy.situ@byd.com',
    license='MIT License',
    url='',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
    install_requires=[''],
    entry_points={
        'console_scripts': [
            ''
        ],
    },
)