from typing import Callable, List, Tuple, Optional

from math import isnan
from .expr import exmat
from .mesh import Mesh, Group
from .pane import Nexus


class Dom:
    __nexus: Nexus

    def __init__(self, mesh: Mesh):
        self.__nexus = Nexus(mesh.pts, mesh.edges, mesh.cells)

    def plot_sys(self) -> Tuple[List[float], List[float]]:
        return self.__nexus.plot_sys()

    def set_boundary(self, *groups):
        for group in groups:
            self.__nexus.set_boundary(group.nodes, group.edges)
        self.__nexus.set_dofs()
        self.__nexus.set_solver()

    def dofs(self) -> Tuple[int, int]:
        return self.__nexus.tot_dofs()

    def embed_bcond(self, bcond: Callable[[float, float], List[float]], group):
        arena, vec = exmat(bcond)
        self.__nexus.embed_bcond(list(group.nodes), list(group.edges), arena, vec)

    def set_force(self, force: Callable[[float, float], List[float]], group: Optional[Group] = None):
        if group is None:
            arena, vec = exmat(force)
            self.__nexus.set_force(0, set(), arena, vec)
        else:
            arena, vec = exmat(force)
            self.__nexus.set_force(group.id, group.cells, arena, vec)

    def set_consts(self, consts: List[List[float]]):
        self.__nexus.set_consts(consts)

    def solve(self, tol: float = 1e-10):
        self.__nexus.assemble()
        self.__nexus.solve(tol)

    def set_vals(self):
        self.__nexus.set_vals()

    def plot_curves(self, res: int, group: Group = None) -> Tuple[List[float], List[float], List[float]]:
        if group is None:
            x, y = self.__nexus.plot_curves(res, set())
            z = [0. if not isnan(v) else v for v in x]
            return x, y, z
        else:
            x, y = self.__nexus.plot_curves(res, group.edges)
            z = [0. if not isnan(v) else v for v in x]
            return x, y, z

    def plot_disp(self, res: int, group: Group = None) -> \
            Tuple[List[float], List[float], List[float], List[float], List[Tuple[int, int, int]]]:
        if group is None:
            (x, y, w), cells = self.__nexus.plot_disp(res, set())
            z = [0. for _ in range(len(x))]
            return x, y, z, w, cells
        else:
            (x, y, w), cells = self.__nexus.plot_disp(res, group.cells)
            z = [0. for _ in range(len(x))]
            return x, y, z, w, cells

    def plot_von_mises(self, group: Group = None) -> Tuple[
        List[float], List[float], List[float], List[float]]:
        if group is None:
            x, y, s = self.__nexus.plot_von_mises(set())
            z = [0. for _ in range(len(x))]
            return x, y, z, s
        else:
            x, y, s = self.__nexus.plot_von_mises(group.cells)
            z = [0. for _ in range(len(x))]
            return x, y, z, s

    def disp_err(self, exact: Callable[[float, float], List[float]]):
        arena, vec = exmat(exact)
        return self.__nexus.err(arena, vec)

    def energy(self) -> float:
        return self.__nexus.energy()
