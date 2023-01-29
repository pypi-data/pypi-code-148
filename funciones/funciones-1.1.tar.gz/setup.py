from distutils.core import setup

setup(
  # Se especifica el nombre de la librería
  name = 'funciones',
  # Se especifica el nombre del paquete
  packages = ['funciones'],
  # Se especifica la versión, que va aumentando con cada actualización
  version = '1.1',
  # Se especifica la licencia escogida
  license='MIT',
  # Breve descripción de la librería
  description = 'Libreria de mates',
  # Nombre del autor
  author = 'Roberto Corona Escamilla',
  # Email del autor
  author_email = 'xxx@gmail.com',
  # Enlace al repositorio de git de la librería
  url = 'https://github.com/RobertoCoronaEscamilla/libreria_rc',
  # Enlace de descarga de la librería
  download_url = 'https://github.com/RobertoCoronaEscamilla/libreria_rc.git',
  # Palabras claves de la librería
  keywords = ['mates', 'par', 'impar'],
  # Librerías externas que requieren la librería
  install_requires=[
          'pytest',
      ],
  classifiers=[
    # Se escoge entre "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    # según el estado de consolidación del paquete
    'Development Status :: 3 - Alpha',
    # Se define el público de la librería
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    # Se indica de nuevo la licencia
    'License :: OSI Approved :: MIT License',
    #Se definen las versiones de python compatibles con la librería
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
'''
afl-3.0              Licencia gratuita académica v3.0	
apache-2.0           Licencia de Apache 2.0
artistic-2.0         Licencia artística 2.0	
bsl-1.0              Licencia de Boost Software 1.0	
bsd-2-clause         Licencia "simplificada" de la cláusula 2 de BSD	
bsd-3-clause         Licencia "nueva" o "revisada" de la cláusula 3 de BSD	
bsd-3-clause-clear   Licencia Clear de la cláusula 3 de BSD	
cc                   Familia de licencias de Creative Commons	
cc0-1.0              Creative Commons Zero v1.0 Universal	
cc-by-4.0            Creative Commons Attribution 4.0	
cc-by-sa-4.0         Creative Commons Attribution Share Alike 4.0	
wtfpl                Licencia pública Do What The F*ck You Want To	
ecl-2.0              Educational Community License v2.0	
epl-1.0              Eclipse Public License 1.0	
epl-2.0              Eclipse Public License 2.0	
eupl-1.1             Licencia pública de la Unión Europea 1.1	
agpl-3.0             Licencia pública general de GNU Affero v3.0	
gpl                  Familia de licencias públicas generales de GNU	
gpl-2.0              Licencia pública general de GNU v2.0	
gpl-3.0              Licencia pública general de GNU v3.0	
lgpl                 Licencia Pública General Menor de GNU	
lgpl-2.1             Licencia Pública General Menor de GNU v2.1	
lgpl-3.0             Licencia Pública General Menor de GNU v3.0	
isc                  ISC	
lppl-1.3c            Licencia pública de LaTeX Project v1.3c	
ms-pl                Licencia pública de Microsoft	
mit                  MIT	
mpl-2.0              Licencia pública de Mozilla 2.0	
osl-3.0              Licencia de Open Software 3.0	
postgresql           Licencia de PostgreSQL	
ofl-1.1              Licencia de SIL Open Font 1.1	
ncsa                 Licencia de código abierto de la Universidad de Illinois/NCSA	
unlicense            The Unlicense	
zlib                 Licencia de zLib	

'''
