from setuptools import setup

setup(
    name='SoAuth',
    version='1.0.1',
    description='Flask middleware for SoAuth',
    url='https://github.com/sojs-coder/SoAuth-Py',
    author='SoJS',
    author_email='sojs_coder@protonmail.com',
    license='ISC',
    packages=['soauth'],
    install_requires=[
        'requests',
        'flask'
    ],
    zip_safe=False
)