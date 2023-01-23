from setuptools import setup, find_packages

setup(
	name="Mensajes",
	version="3.0",
	description="Un paquete para saludar y despedir",
	author="Hector Alvarez Vazquez",
	author_email="hola@hector.dev",
	url="http://hectorav.info",
    packages=find_packages(),
	scripts=['test.py'],
	install_required=[paquete.strip() 
						for paquete in open("requirements.txt").readlines()]
)