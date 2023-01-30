from setuptools import setup, find_packages
def read(filename):
    return [req.strip() for req in open(filename).readlines()]

setup(
    name='superlogica-conector',
    url='',
    version='0.0.1',
    author='crasdata',
    description='Data intake conector of API Superlogica for anywhere',
    long_description=open('README.md').read(),
    author_email='anderson.santana@crasdata.com.br',
    setup_requires=['easypkg'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_require={"dev": read("requirements-dev.txt")},
    license = 'MIT'
)