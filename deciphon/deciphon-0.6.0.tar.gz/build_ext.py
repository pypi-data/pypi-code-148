import os
import shutil
import sys
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from subprocess import check_call

RPATH = "$ORIGIN" if sys.platform.startswith("linux") else "@loader_path"

PWD = Path(os.path.dirname(os.path.abspath(__file__)))
TMP = PWD / ".build_ext"
PKG = PWD / "deciphon"
INTERFACE = PKG / "interface.h"

LIB = str(Path(PKG) / "lib")
INCL = str(Path(PKG) / "include")
EXTRA = f"-Wl,-rpath,{RPATH}/lib"
SHARE = str(Path(PKG) / "share")

CMAKE_OPTS = [
    "-DCMAKE_BUILD_TYPE=Release",
    "-DBUILD_SHARED_LIBS=ON",
    f"-DCMAKE_INSTALL_RPATH={RPATH}",
]

CPM_OPTS = ["-DCPM_USE_LOCAL_PACKAGES=ON"]


@dataclass
class Ext:
    user: str
    project: str
    version: str
    cmake_opts: list[str]


EXTS = [
    Ext("horta", "logaddexp", "2.1.14", CMAKE_OPTS),
    Ext("horta", "elapsed", "3.1.2", CMAKE_OPTS),
    Ext("EBI-Metagenomics", "lip", "0.5.0", CMAKE_OPTS),
    Ext("EBI-Metagenomics", "hmr", "0.6.0", CMAKE_OPTS),
    Ext("EBI-Metagenomics", "imm", "2.1.10", CMAKE_OPTS + CPM_OPTS),
    Ext("EBI-Metagenomics", "deciphon", "0.4.1", CMAKE_OPTS + CPM_OPTS),
]


def rm(folder: Path, pattern: str):
    for filename in folder.glob(pattern):
        filename.unlink()


def build_ext(ext: Ext):
    from cmake import CMAKE_BIN_DIR

    prj_dir = TMP / f"{ext.project}-{ext.version}"
    bld_dir = prj_dir / "build"
    os.makedirs(bld_dir, exist_ok=True)

    url = f"https://github.com/{ext.user}/{ext.project}/archive/refs/tags/v{ext.version}.tar.gz"

    tar_filename = f"{ext.project}-{ext.version}.tar.gz"

    with open(TMP / tar_filename, "wb") as lf:
        lf.write(urllib.request.urlopen(url).read())

    with tarfile.open(TMP / tar_filename) as tf:
        tf.extractall(TMP)

    cmake = [str(v) for v in Path(CMAKE_BIN_DIR).glob("cmake*")][0]
    check_call([cmake, "-S", str(prj_dir), "-B", str(bld_dir)] + ext.cmake_opts)
    check_call([cmake, "--build", str(bld_dir), "--config", "Release"])
    check_call([cmake, "--install", str(bld_dir), "--prefix", str(PKG)])


if __name__ == "__main__":
    from cffi import FFI

    ffibuilder = FFI()

    rm(PKG, "cffi.*")
    rm(PKG / "lib", "**/lib*")
    shutil.rmtree(TMP, ignore_errors=True)

    for ext in EXTS:
        build_ext(ext)

    ffibuilder.cdef(open(INTERFACE, "r").read())
    ffibuilder.set_source(
        "deciphon.cffi",
        """
        #include "deciphon/deciphon.h"
        """,
        language="c",
        libraries=["deciphon"],
        library_dirs=[LIB],
        include_dirs=[INCL],
        extra_link_args=[EXTRA],
    )
    ffibuilder.compile(verbose=True)

    shutil.rmtree(INCL, ignore_errors=True)
    shutil.rmtree(SHARE, ignore_errors=True)
    shutil.rmtree(Path(LIB) / "cmake", ignore_errors=True)

    find = ["/usr/bin/find", LIB, "-type", "l"]
    exec0 = ["-exec", "/bin/cp", "{}", "{}.tmp", ";"]
    exec1 = ["-exec", "/bin/mv", "{}.tmp", "{}", ";"]
    check_call(find + exec0 + exec1)
