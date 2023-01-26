from setuptools import setup

name = "types-flake8-docstrings"
description = "Typing stubs for flake8-docstrings"
long_description = '''
## Typing stubs for flake8-docstrings

This is a PEP 561 type stub package for the `flake8-docstrings` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-docstrings`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-docstrings. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `99ea07a46369adce63ea632575a8b6a4c3f26d2d`.
'''.lstrip()

setup(name=name,
      version="1.7.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-docstrings.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['flake8_docstrings-stubs'],
      package_data={'flake8_docstrings-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
