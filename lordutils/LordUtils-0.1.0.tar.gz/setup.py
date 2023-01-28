from setuptools import setup, find_packages

setup(
    name='LordUtils',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/BexWorld/LordUtils.git',
    license='',
    author='lordbex',
    author_email='lordibex@protonmail.com',
    description='Helper Package for other Lord packages',
    long_description='Helper Package for other Lord packages',
    include_package_data=True,
    install_requires=[
        'regex',
        'validators',
        'rich'
    ],
)
