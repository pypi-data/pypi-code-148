from setuptools import setup

setup(
    name='tickstore-python-client',
    version='1.0.4',
    packages=['tickstore', 'tickstore/db', 'tickstore/query', 'tickstore/writers'],
    url='https://gitlab.com/alphaticks/tickstore-python-client',
    license='copyright',
    author='Alphaticks',
    description='client to communicate with tickstore',
    install_requires=[
        'protobuf==4.21.12',
        'tickstore-grpc==1.0.2',
    ]
)
