from setuptools import setup, find_packages

setup(
    name='Topsis-Yashasvi-102053031',
    version='1.0.1',
    packages=find_packages(),
    py_modules=['102053031'],
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'Topsis-Yashasvi-102053031 = 102053031:main'
        ]
    },
)
