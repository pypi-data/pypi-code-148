from setuptools import setup

with open("description.md", "r", encoding='utf-8') as arq:
    long_description = arq.read()

setup(name='isitkbs',
    version='1.1.0',
    license='MIT License',
    author='Arthur de Melo, Arthur Grandão, Douglas Alves, Gabriel Campello, Paulo Victor, Rafael Ferreira, Sidney Fernando',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #author_email='',
    keywords='keyboard-smashing',
    description=u'Detect keyboard smashing',
    include_package_data=True,
    packages=['isitkbs', 'models'],
    testpakages =['pytest'],
    install_requires=['scikit-learn', 'nltk', 'matplotlib' , 'pandas'],)