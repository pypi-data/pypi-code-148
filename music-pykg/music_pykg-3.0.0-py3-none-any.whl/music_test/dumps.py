from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any, Callable, Dict, Sequence, Tuple, Union

import h5py
import numpy as np
from music_pykg.format1 import MusicFormat1DumpFile
from music_pykg.format2 import MusicNewFormatDumpFile
from music_pykg.known_variables import KnownMusicVariables, Node

from .utils import RelativePath


class Dump(ABC):
    """Base class for dump definition without knowing its concrete location."""

    @abstractmethod
    def with_path(self, path: Path) -> ConcreteDump:
        """Return a concrete dump relative to the provided location."""

    def __sub__(self, other: Dump) -> Dump:
        """Represent the difference between two dumps."""
        return DiffDump(self, other)


class ConcreteDump(ABC):
    """Dump knowing its concrete location."""

    @abstractmethod
    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        """Return a tuple (header, data) of two dictionaries,
        which map entry names to numerical values for the dump
        (typically of type `int`, `float` or `numpy.ndarray`).
        """


class FileDump(Dump, ABC):
    """A dump which corresponds to an actual file on disk"""

    filename: Union[str, PathLike, RelativePath]

    @abstractmethod
    def with_path(self, path: Path) -> ConcreteFileDump:
        ...


class ConcreteFileDump(ConcreteDump, ABC):

    fdump: FileDump
    path: Path

    @property
    def full_filename(self) -> Path:
        return self.path / self.fdump.filename


@dataclass(frozen=True)
class MusicDump1(FileDump):
    """Old-style MUSIC dump (output_method=1)"""

    filename: Union[str, PathLike, RelativePath]
    ndim: int
    idump: int = -1
    trim_last_cell: bool = True

    def with_path(self, path: Path) -> ConcreteDump1:
        return ConcreteDump1(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDump1(ConcreteFileDump):
    fdump: MusicDump1
    path: Path

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        with MusicFormat1DumpFile(self.full_filename, self.fdump.ndim) as dump:
            header, data = dump.read(self.fdump.idump)

        def trim(arr: np.ndarray) -> np.ndarray:
            for ax in range(arr.ndim):
                arr = np.take(arr, range(arr.shape[ax] - 1), axis=ax)
            return arr

        if self.fdump.trim_last_cell:
            data = {k: trim(arr) for k, arr in data.items()}
        return header, data


@dataclass(frozen=True)
class MusicDump2(FileDump):
    """New-style MUSIC dump (output_method=2)"""

    filename: Union[str, PathLike, RelativePath]

    def with_path(self, path: Path) -> ConcreteDump2:
        return ConcreteDump2(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDump2(ConcreteFileDump):
    fdump: MusicDump2
    path: Path

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        music_vars = KnownMusicVariables()
        hdr, data = MusicNewFormatDumpFile(self.full_filename).read()
        data = {music_vars.legacy(name).name: vals for name, vals in data.items()}
        return hdr.as_dict(), data


@dataclass(frozen=True)
class MusicDumpH5(FileDump):
    """MUSIC dump in HDF5 format."""

    filename: Union[str, PathLike, RelativePath]

    def with_path(self, path: Path) -> ConcreteDumpH5:
        return ConcreteDumpH5(fdump=self, path=path)


@dataclass(frozen=True)
class ConcreteDumpH5(ConcreteFileDump):
    fdump: MusicDumpH5
    path: Path

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        data = {}
        with h5py.File(self.full_filename) as h5f:
            for name, values in h5f["fields"].items():
                data[name] = values[()].squeeze().T
        return {}, data


@dataclass(frozen=True)
class DiffDump(Dump):
    """A dump formed by selecting the header of either `dump_left` or `dump_right`,
    and taking the differences of the data arrays.
    """

    dump_left: Dump
    dump_right: Dump
    which_header: str = "left"  # select header from dump_left or dump_right

    def with_path(self, path: Path) -> ConcreteDiffDump:
        return ConcreteDiffDump(
            self.dump_left.with_path(path),
            self.dump_right.with_path(path),
            which_header=self.which_header,
        )


@dataclass(frozen=True)
class ConcreteDiffDump(ConcreteDump):

    dump_left: ConcreteDump
    dump_right: ConcreteDump
    which_header: str = "left"  # select header from dump_left or dump_right

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        header_left, data_left = self.dump_left.header_and_data()
        header_right, data_right = self.dump_right.header_and_data()
        if self.which_header == "left":
            header = header_left
        elif self.which_header == "right":
            header = header_right
        else:
            raise ValueError(
                f"DiffDumpData: expected which_header to be "
                f"either 'left' or 'right', got '{self.which_header}'"
            )

        if not set(data_left.keys()) == set(data_right.keys()):
            raise ValueError(
                "DiffDumpData: non-identical data keys, got "
                f"keys_left={list(data_left.keys())}, "
                f"keys_right={list(data_right.keys())}"
            )

        return header, {k: data_left[k] - data_right[k] for k in data_left}


def _beg(x: np.ndarray) -> np.ndarray:
    return x[:-1]


def _end(x: np.ndarray) -> np.ndarray:
    return x[1:]


def _mid(x: np.ndarray) -> np.ndarray:
    return 0.5 * (_beg(x) + _end(x))


def _mgrid(xfs: Sequence[np.ndarray], node: Node) -> Sequence[np.ndarray]:
    ndim = len(xfs)
    xps = [
        _beg(xf) if node.is_staggered_along(ax, ndim) else _mid(xf)
        for ax, xf in enumerate(xfs)
    ]
    return np.meshgrid(*xps, indexing="ij")


@dataclass(frozen=True)
class AnalyticalSolution(Dump):
    func: Callable
    ref_dump: Dump

    def with_path(self, path: Path) -> ConcreteAnalyticalSolution:
        return ConcreteAnalyticalSolution(self.func, self.ref_dump.with_path(path))


@dataclass(frozen=True)
class ConcreteAnalyticalSolution(ConcreteDump):
    func: Callable
    ref_dump: ConcreteDump

    def header_and_data(self) -> Tuple[Dict[str, Any], Dict[str, np.ndarray]]:
        header, data = self.ref_dump.header_and_data()

        music_vars = KnownMusicVariables()
        unknown_vars = set(name for name in data.keys() if name not in music_vars)
        if unknown_vars:
            raise ValueError(
                f"{self.ref_dump} has variables {sorted(unknown_vars)}"
                " whose mesh centering cannot be inferred"
            )

        ndim = data["density"].ndim

        xfs = [header[f"face_loc_{i+1}"] for i in range(ndim)]
        time = header["time"]

        def sol(var: str) -> np.ndarray:
            xps = _mgrid(xfs, music_vars[var].node)
            fields = self.func(time, *xps)
            if var not in fields:
                raise ValueError(
                    f"field '{var}' is present in '{self.ref_dump}' but not in analytical solution"
                )
            return fields[var]

        return header, {k: sol(k) for k in data}
