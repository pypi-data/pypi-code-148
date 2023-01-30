from setuptools import setup

name = "types-whatthepatch"
description = "Typing stubs for whatthepatch"
long_description = '''
## Typing stubs for whatthepatch

This is a PEP 561 type stub package for the `whatthepatch` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`whatthepatch`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/whatthepatch. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `398bd90b8e3b04d7c07d8a2eb16a55a1ca6f9729`.
'''.lstrip()

setup(name=name,
      version="1.0.2.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/whatthepatch.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['whatthepatch-stubs'],
      package_data={'whatthepatch-stubs': ['__init__.pyi', 'apply.pyi', 'exceptions.pyi', 'patch.pyi', 'snippets.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
