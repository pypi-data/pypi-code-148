from setuptools import setup, find_packages

long_description = open('README.md').read()

setup(
    name='mobizclick2sure',
    version='1.1',
    packages=find_packages(),
    url='',
    license='free for c2s',
    author='Khaled Yasser',
    author_email='khaledyasser@click2sure.co.za',
    description='A package for sending SMS messages using mobiz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'django',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
