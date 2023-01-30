from setuptools import setup


def get_version():
    with open('kaninipycs.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in 'README.rst', 'CHANGES.txt':
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='kaninipycs',
    version="1.0.0",
    description="Python style guide checker",
    long_description=get_long_description(),
    keywords='kaninipycs',
    author='Kanini',
    author_email='rakesh.manjunath21@gmail.com',
    license='Expat license',
    py_modules=['kaninipycs'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'kaninipycs = kaninipycs:_main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
    },
)
