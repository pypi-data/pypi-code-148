from setuptools import setup, find_packages

setup(
    name='excelart',
    version='0.1.1',
    packages=find_packages(),
    author='Ujwal Rajeev',
    author_email='ujwalrajeev@gmail.com',
    url='https://github.com/ujwalrajeev/excelart',
    description='A package to convert excel data to image',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    install_requires=[
        'openpyxl',
        'Pillow'
    ]
)
