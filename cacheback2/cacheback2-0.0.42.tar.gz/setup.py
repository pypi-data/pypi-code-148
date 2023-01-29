from setuptools import find_packages, setup

setup(
    name='cacheback2',
    version='0.0.42',
    packages=find_packages(include=['cacheback2']),
    url='',
    license='MIT',
    author='jeein',
    author_email='',
    description='',
    install_requires=[
        'SQLAlchemy==1.4.45',
        'numpy==1.23.5',
        'pandas==1.5.2',
        'psycopg2-binary==2.9.3',
        'wheel==0.38.4'
    ]

)
