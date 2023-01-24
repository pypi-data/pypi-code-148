from setuptools import setup, find_packages


# Set up paquetes
setup(
    name = 'Mensajes-Armando_Rosas_Balderas',
    version= '6.0',
    description= 'Un paquete para saludar y despedir',
    long_description= open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author= 'Jose Armando Rosas Balderas',
    author_email= 'armando.rosas133@gmail.com',
    url= 'https://www.linkedin.com/in/josearmandorosas',
    license_files = ['LICENSE'],
    packages= find_packages(),
    scripts= [],
    test_suite = 'tests',
    install_requires = [paquete.strip()
                        for paquete in open('requirements.txt').readlines()],
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
    ]
)

# Para ejecutar el setup
# Generar el distribuible

# Cargar los paquetes en python o actaulizarlo
'''
py setup.py sdist

cd dist

pip install fileName.tar.gz

EN CASO DE ACTUALIZAR 
pip install newFileName.tar.gz --upgrade

pip list 

'''

# PARA DESINSTALAR

'''
pip uninstall nombrePaquete
'''

# Para subirlo a internet

'''
py -m build
py -m twine check dist /*
py -m twine upload -r testpypi dist/*
'''