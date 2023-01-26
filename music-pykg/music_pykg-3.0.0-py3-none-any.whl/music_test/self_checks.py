from __future__ import annotations

import operator
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from music_pykg.prof1d import Prof1d

from .term import CollectedMsgs, Message, err_msg, info_msg
from .validation import ValidationResult

if typing.TYPE_CHECKING:
    from typing import Callable, Mapping

    from numpy.typing import ArrayLike

    from .dumps import Dump, FileDump


class SelfCheck(ABC):
    @abstractmethod
    def check_run(self, run_dir: Path) -> ValidationResult:
        raise NotImplementedError

    def __and__(self, other: SelfCheck) -> SelfCheck:
        return CombinedSelfCheck(self, other, operator.and_)

    def __or__(self, other: SelfCheck) -> SelfCheck:
        return CombinedSelfCheck(self, other, operator.or_)


@dataclass(frozen=True)
class CombinedSelfCheck(SelfCheck):
    check1: SelfCheck
    check2: SelfCheck
    binary_op: Callable[[ValidationResult, ValidationResult], ValidationResult]

    def check_run(self, run_dir: Path) -> ValidationResult:
        return self.binary_op(
            self.check1.check_run(run_dir), self.check2.check_run(run_dir)
        )


def _mapping_norm_msg(mapping: Mapping[str, ArrayLike]) -> Message:
    def norm_1(x: ArrayLike) -> np.number:
        return np.mean(np.abs(x))

    def norm_2(x: ArrayLike) -> np.number:
        return np.sqrt(np.mean(np.abs(x) ** 2))

    def norm_inf(x: ArrayLike) -> np.number:
        return np.max(np.abs(x))

    q = "'"
    return CollectedMsgs(
        [
            info_msg(
                f"norms({q + k + q:10s}): "
                f"L1={norm_1(v):.4e}, "
                f"L2={norm_2(v):.4e}, "
                f"Linf={norm_inf(v):.4e}"
            )
            for k, v in mapping.items()
        ],
    )


@dataclass(frozen=True)
class ReportNorms(SelfCheck):
    """Report norms of input dump object to log messages, always returning a successful status.

    NOTE: the norms are computed pointwise naively, i.e. they are seen as norms on data arrays,
    not as proper integral norms e.g. on the sphere.
    """

    dump: Dump
    label: str = ""

    def check_run(self, run_dir: Path) -> ValidationResult:
        _, data = self.dump.with_path(run_dir).header_and_data()
        message = _mapping_norm_msg(data)

        return ValidationResult(True, message).with_header_msg(
            info_msg("ReportNorms" + (f"[{self.label}]" if self.label else "") + ":")
        )


@dataclass(frozen=True)
class ReportProf1dDiff(SelfCheck):
    """Report difference between two prof1d."""

    prof1d_left: str
    prof1d_right: str
    label: str = ""

    def check_run(self, run_dir: Path) -> ValidationResult:
        p1dl = Prof1d(run_dir / self.prof1d_left)
        p1dr = Prof1d(run_dir / self.prof1d_right)

        params = {k: p1dl.params[k] - rval for k, rval in p1dr.params.items()}
        message = _mapping_norm_msg(params)
        result = ValidationResult(True, message).with_header_msg(
            info_msg(
                "ReportProf1dDiff-params"
                + (f"[{self.label}]" if self.label else "")
                + ":"
            )
        )

        profs = p1dl.profs - p1dr.profs
        message = _mapping_norm_msg(profs)
        result &= ValidationResult(True, message).with_header_msg(
            info_msg(
                "ReportProf1dDiff-profs"
                + (f"[{self.label}]" if self.label else "")
                + ":"
            )
        )
        return result


@dataclass(frozen=True)
class CheckTimeOfDump(SelfCheck):
    dump: FileDump
    time: float

    def check_run(self, run_dir: Path) -> ValidationResult:
        dump = self.dump.with_path(run_dir)
        header, _ = dump.header_and_data()
        t = header["time"]
        if not np.isclose(t, self.time):
            return ValidationResult(
                False,
                message=err_msg(
                    f"dump '{dump.full_filename}': expected time={self.time} but found {t}"
                ),
            )
        return ValidationResult(
            True,
            info_msg(
                f"dump '{dump.full_filename}': expected time={self.time}, found {t}"
            ),
        )
