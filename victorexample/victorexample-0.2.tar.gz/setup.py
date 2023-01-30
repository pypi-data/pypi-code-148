from setuptools import setup, find_packages

setup(
    name='victorexample',
    version=0.2,
    license="MIT",
    description="Paquete de prueba",
    author='Victor Martinez Santiago @vicbox01',
#    author_email='victor.santiago@cimat.mx',
    url='https://github.com/VicBoxMS/SeleccionDeInstancias',
    install_requires=['numpy'],
    packages=find_packages()
)
