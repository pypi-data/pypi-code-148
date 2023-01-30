from setuptools import setup, find_packages

setup(
    name='victorexample',
    version=0.1,
    license="MIT",
    description="Paquete que contiene funciones utiles para selección de instancias",
    author='Victor Martinez Santiago @vicbox01',
#    author_email='victor.santiago@cimat.mx',
    url='https://github.com/VicBoxMS/SeleccionDeInstancias',
    install_requires=['numpy'],
    packages=find_packages()
)
