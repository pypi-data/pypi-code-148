from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

from .cmake_builder import Target
from .comparison_checks import CompareDumps
from .dumps import AnalyticalSolution, MusicDump2
from .runs import MusicRun
from .self_checks import CheckTimeOfDump, ReportNorms
from .test import Test
from .utils import LastFileNameInGlob


@dataclass(frozen=True)
class RotatedFrame2D:
    """A 2D rotated frame of reference"""

    angle: float

    def frame_to_global(
        self, xloc: np.float64, yloc: np.float64
    ) -> Tuple[np.float64, np.float64]:
        """Transform local frame coordinates to global"""
        s, c = np.sin(self.angle), np.cos(self.angle)
        xglob = c * xloc - s * yloc
        yglob = s * xloc + c * yloc
        assert np.allclose(xglob**2 + yglob**2, xloc**2 + yloc**2)
        return xglob, yglob

    def global_to_frame(
        self, xglob: np.float64, yglob: np.float64
    ) -> Tuple[np.float64, np.float64]:
        """Transform global coordinates into local frame"""
        return RotatedFrame2D(-self.angle).frame_to_global(xglob, yglob)


@dataclass(frozen=True)
class CircularAlfvenWave2D:
    """Circularly polarized Aflven wave setup in 2D"""

    alpha: float
    v0: np.float64
    gamma: float = 5.0 / 3.0
    rho0: float = 1.0
    press0: float = 0.1
    b0: np.float64 = np.float64(1.0)
    eps: float = 0.1

    @property
    def v_alfven(self) -> np.float64:
        """Bulk Alfven velocity"""
        return self.b0 / np.sqrt(self.rho0)

    def _state_t0(self, x: np.float64, y: np.float64) -> Dict:
        """Compute the state at time t=0 at given (x, y) coordinate(s)"""
        wave_frame = RotatedFrame2D(self.alpha)  # Rotated frame of reference
        x_para, x_perp = wave_frame.global_to_frame(x, y)

        phi = 2 * np.pi * x_para
        cos_phi, sin_phi = np.cos(phi), np.sin(phi)

        (vx, vy), vz = (
            wave_frame.frame_to_global(self.v0, self.eps * sin_phi),
            self.eps * cos_phi,
        )

        (bx, by), bz = (
            wave_frame.frame_to_global(self.b0, self.eps * sin_phi),
            self.eps * cos_phi,
        )

        return {
            "density": self.rho0,
            "e_spec_int": self.press0 / self.rho0 / (self.gamma - 1.0),
            "vel_1": vx,
            "vel_2": vy,
            "vel_3": vz,
            "magfield_1": bx,
            "magfield_2": by,
            "magfield_3": bz,
        }

    def state_at(self, t: np.float64, x: np.float64, y: np.float64) -> Dict:
        """Compute the state at time t at given (x, y) coordinate(s)"""
        delta_v = self.v0 - self.v_alfven
        return self._state_t0(
            x - delta_v * t * np.cos(self.alpha),
            y - delta_v * t * np.sin(self.alpha),
        )


def make_circular_alfven_2d_test_config(
    ny: int, nprocs: Tuple[int, int] = (1, 1)
) -> Test:

    output_dump = MusicDump2(filename=LastFileNameInGlob("output/*.music"))

    test_pb = CircularAlfvenWave2D(alpha=np.arctan(2.0), v0=np.float64(0.0))
    exact_sol = AnalyticalSolution(test_pb.state_at, output_dump)

    report_diff_with_sol = ReportNorms(
        dump=output_dump - exact_sol,
        label="(final)-(exact)",
    )

    nx = 2 * ny

    return Test(
        description=f"2D MHD Alfvén wave setup, {nx}x{ny}",
        tags=("long", "scaled_up") if ny > 64 else ("medium",),
        build_targets=Target("2.5dim"),
        run=MusicRun(
            namelist="params.nml",
            start_dump=MusicDump2("alfven_wave.music"),
        ),
        self_check=CheckTimeOfDump(output_dump, 1.0) & report_diff_with_sol,
        comparison_check=CompareDumps(output_dump),
    )
