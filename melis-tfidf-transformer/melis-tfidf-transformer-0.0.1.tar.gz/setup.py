import setuptools

setuptools.setup(
    name = 'melis-tfidf-transformer',
    version = '0.0.1',
    author = 'Melis Kızıldemir',
    description = 'A package for doing tf-idf transformations.',
    packages = ['tfidf'],
    install_requires=['numpy', 'bs4']
    )