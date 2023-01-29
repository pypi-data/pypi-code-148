from setuptools import setup

name = "types-python-slugify"
description = "Typing stubs for python-slugify"
long_description = '''
## Typing stubs for python-slugify

This is a PEP 561 type stub package for the `python-slugify` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`python-slugify`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-slugify. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `25e02db42cdf3146d658b07015d31660e153ff06`.
'''.lstrip()

setup(name=name,
      version="8.0.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-slugify.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['slugify-stubs'],
      package_data={'slugify-stubs': ['__init__.pyi', '__version__.pyi', 'slugify.pyi', 'special.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
