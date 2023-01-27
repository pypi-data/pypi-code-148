from setuptools import setup

setup(
    name='bip32utility',
    version='0.1.0',    
    description='Simple Bip32 Calculator',
    url='https://github.com/shuds13/bip32',
    author='Stephen Hudson',
    author_email='shudson@anl.gov',
    license='BSD 2-clause',
    packages=['bip32utility'],
    install_requires=['hdwallet',
                      'firebase_admin','datetime','time'                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)