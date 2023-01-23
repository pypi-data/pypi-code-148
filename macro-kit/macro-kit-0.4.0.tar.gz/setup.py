from setuptools import setup, find_packages
import os
import sys
from distutils.command import build_ext

# Modified from https://github.com/tlambert03/psygnal
if os.name == "nt":

    # fix LINK : error LNK2001: unresolved external symbol PyInit___init__
    # Patch from: https://bugs.python.org/issue35893

    def get_export_symbols(self, ext):  # type: ignore
        """
        Slightly modified from:
        https://github.com/python/cpython/blob/8849e5962ba481d5d414b3467a256aba2134b4da\
        /Lib/distutils/command/build_ext.py#L686-L703
        """
        parts = ext.name.split(".")
        suffix = parts[-2] if parts[-1] == "__init__" else parts[-1]
        # from here on unchanged
        try:
            # Unicode module name support as defined in PEP-489
            # https://www.python.org/dev/peps/pep-0489/#export-hook-name
            suffix.encode("ascii")
        except UnicodeEncodeError:
            suffix = "U" + suffix.encode("punycode").replace(b"-", b"_").decode("ascii")

        initfunc_name = "PyInit_" + suffix
        if initfunc_name not in ext.export_symbols:
            ext.export_symbols.append(initfunc_name)
        return ext.export_symbols

    build_ext.build_ext.get_export_symbols = get_export_symbols  # type: ignore


with open("macrokit/__init__.py", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            VERSION = line.strip().split()[-1][1:-1]
            break

with open("README.md") as f:
    readme = f.read()

ext_modules = None
if (
    all(arg not in sys.argv for arg in ["clean", "check"])
    and "SKIP_CYTHON" not in os.environ
):
    try:
        from Cython.Build import cythonize
    except ImportError:
        pass
    else:
        # For cython test coverage install with `make build-trace`
        compiler_directives = {}
        if "CYTHON_TRACE" in sys.argv:
            compiler_directives["linetrace"] = True
        # Set CFLAG to all optimizations (-O3)
        # Any additional CFLAGS will be appended.
        # Only the last optimization flag will have effect
        os.environ["CFLAGS"] = "-O3 " + os.environ.get("CFLAGS", "")
        ext_modules = cythonize(
            module_list=[
                "macrokit/_symbol.py",
                "macrokit/_validator.py",
                "macrokit/ast.py",
                "macrokit/expression.py",
                "macrokit/head.py",
            ],
            nthreads=int(os.getenv("CYTHON_NTHREADS", 0)),
            language_level=3,
            compiler_directives=compiler_directives,
        )


setup(
    name="macro-kit",
    version=VERSION,
    description="Macro recording and metaprogramming in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Hanjin Liu",
    author_email="liuhanjin-sc@g.ecc.u-tokyo.ac.jp",
    license="BSD 3-Clause",
    download_url="https://github.com/hanjinliu/macro-kit",
    install_requires=["typing_extensions"],
    packages=find_packages(exclude=["tests", "examples"]),
    package_data={"macrokit": ["py.typed"]},
    ext_modules=ext_modules,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
