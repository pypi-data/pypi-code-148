from dataclasses import dataclass
from functools import cached_property
from types import MappingProxyType
from typing import Mapping, Sequence, Tuple


@dataclass(frozen=True)
class Node:
    staggered_along_ax: Tuple[bool, bool, bool]

    def is_staggered_along(self, axis: int, ndim: int) -> bool:
        assert 1 <= ndim <= 3
        assert 0 <= axis <= 2
        last_axis = ndim - 1
        if axis > last_axis:
            # A node is never staggered along a non-existing dimension
            return False
        else:
            return self.staggered_along_ax[axis]

    def num_staggered_axes(self, ndim: int) -> int:
        assert 1 <= ndim <= 3
        return sum(self.staggered_along_ax[:ndim])


# Define some nodes
NODE_CENTER = Node(staggered_along_ax=(False, False, False))

NODE_FACE_1 = Node(staggered_along_ax=(True, False, False))
NODE_FACE_2 = Node(staggered_along_ax=(False, True, False))
NODE_FACE_3 = Node(staggered_along_ax=(False, False, True))


@dataclass(frozen=True)
class Variable:
    name: str
    legacy_name: str
    node: Node


@dataclass(frozen=True)
class KnownMusicVariables:
    named_scalars: Sequence[str] = ()

    @cached_property
    def _vars(self) -> Sequence[Variable]:
        return [
            Variable(name="density", legacy_name="rho", node=NODE_CENTER),
            Variable(name="e_spec_int", legacy_name="e", node=NODE_CENTER),
            # --
            Variable(name="vel_1", legacy_name="v_r", node=NODE_FACE_1),
            Variable(name="vel_2", legacy_name="v_t", node=NODE_FACE_2),
            Variable(name="vel_3", legacy_name="v_p", node=NODE_FACE_3),
            # --
            Variable(name="magfield_1", legacy_name="b_r", node=NODE_FACE_1),
            Variable(name="magfield_2", legacy_name="b_t", node=NODE_FACE_2),
            Variable(name="magfield_3", legacy_name="b_p", node=NODE_FACE_3),
            # --
            *[
                Variable(
                    name=name,
                    legacy_name=f"Scalar{i}",
                    node=NODE_CENTER,
                )
                for i, name in enumerate(self.named_scalars, 1)
            ],
        ]

    @cached_property
    def _legacy_names_dict(self) -> Mapping[str, Variable]:
        return MappingProxyType({v.legacy_name: v for v in self._vars})

    @cached_property
    def _names_dict(self) -> Mapping[str, Variable]:
        return MappingProxyType({v.name: v for v in self._vars})

    def legacy(self, name: str) -> Variable:
        """Get a variable by its legacy name."""
        if name in self._legacy_names_dict:
            return self._legacy_names_dict[name]
        if not self.named_scalars and name.startswith("Scalar"):
            try:
                iscalar = int(name[6:])
                return Variable(
                    name=f"scalar_{iscalar}",
                    legacy_name=name,
                    node=NODE_CENTER,
                )
            except ValueError:
                pass
        raise KeyError(
            f"Variable with legacy name '{name}' unknown to KnownMusicVariables"
        )

    def __getitem__(self, name: str) -> Variable:
        """Get a variable by its name."""
        if name in self._names_dict:
            return self._names_dict[name]
        if not self.named_scalars and name.startswith("scalar_"):
            try:
                iscalar = int(name[7:])
                return Variable(
                    name=name,
                    legacy_name=f"Scalar{iscalar}",
                    node=NODE_CENTER,
                )
            except ValueError:
                pass
        raise KeyError(f"Variable with name '{name}' unknown to KnownMusicVariables")

    def __contains__(self, name: str) -> bool:
        """Check whether a variable is known."""
        try:
            self[name]
        except KeyError:
            return False
        return True
