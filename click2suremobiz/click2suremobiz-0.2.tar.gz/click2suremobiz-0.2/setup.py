from setuptools import setup, find_packages

setup(
    name='click2suremobiz',
    version='0.2',
    author='Khaled Yasser',
    author_email='khaled.yasser@click2sure.co.za',
    packages=find_packages(),
    install_requires=['requests', 'Django'],
    include_package_data=True,
)
