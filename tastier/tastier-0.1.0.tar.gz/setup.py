from setuptools import setup


with open('README.md', 'r') as description_file:
    long_description = description_file.read()


setup(
    name='tastier',
    version='0.1.0',
    description='A human-readable format for nested data serialization',
    url='https://github.com/zeionara/tasty',
    author='Zeio Nara',
    author_email='zeionara@gmail.com',
    packages=[
        'tasty',
        'tasty/util'
    ],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)
