from setuptools import setup, find_packages

setup(
    name='LordUtils',
    version='0.0.0.2',
    packages=find_packages(),
    url='https://git.lordbex.xyz/PipModule/LordUtils.git',
    license='',
    author='lordbex',
    author_email='lordibex@protonmail.com',
    description='Lord Utils',
    include_package_data=True,
    install_requires=[
        'regex',
        'validators',
        'rich'
    ],
)
