from setuptools import setup

setup(
    name='excelart',
    version='0.1',
    packages=['excelart'],
    install_requires=[
        'openpyxl',
        'Pillow'
    ],
    author='Ujwal Rajeev',
    author_email='ujwalrajeev@gmail.com',
    description='A package that converts excel data to image',
    url='https://github.com/ujwalrajeev/excelart',
    download_url='https://github.com/ujwalrajeev/excelart/archive/0.1.tar.gz',
    keywords=['excel', 'image', 'conversion'],
    classifiers=[],
)
