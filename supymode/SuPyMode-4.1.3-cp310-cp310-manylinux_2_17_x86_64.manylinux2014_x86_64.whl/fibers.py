#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy
from dataclasses import dataclass, field
from FiberFusing import Circle
from PyOptik import ExpData

__all__ = ['DCF1300S_20',
           'DCF1300S_33',
           'NewA',
           'NewB',
           'NewC',
           'NewD',
           'F2028M24',
           'F2028M21',
           'F2028M12',
           'SMF28',
           'HP630']


def get_silica_index(wavelength: float):
    return ExpData('FusedSilica').GetRI(wavelength)[0]


@dataclass
class GenericFiber():
    wavelength: float
    position: tuple = (0, 0)
    _polygones: tuple = field(default=tuple(), repr=False)

    def __post_init__(self):
        ...

    @property
    def silica_index(self):
        return ExpData('FusedSilica').GetRI(self.wavelength)[0]

    def NA_to_core_index(self, NA: float, index_clad: float):
        return numpy.sqrt(NA**2 + index_clad**2)

    def core_index_to_NA(self, index_core: float, index_clad: float):
        return numpy.sqrt(index_core**2 - index_clad**2)

    @property
    def polygones(self):
        if not self._polygones:
            self.initialize_polygones()
        return self._polygones

    def __repr__(self):
        kws = [f"{key}={value!r}" for key, value in self.__dict__.items()]
        return "{}({})".format(type(self).__name__, ", ".join(kws))


@dataclass
class DCF1300S_20(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.11, self.silica_index)
        self.core_index = self.NA_to_core_index(0.12, self.clad_index)
        self.clad_radius = 19.9 / 2
        self.core_radius = 4.6

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class DCF1300S_33(GenericFiber):
    wavelength: float
    position: tuple = (0, 0)
    _polygones: tuple = field(default=tuple(), repr=False)

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.11, self.silica_index)
        self.core_index = self.NA_to_core_index(0.125, self.clad_index)
        self.clad_radius = 33 / 2
        self.core_radius = 4.5

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class NewA(GenericFiber):
    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.11, self.silica_index)
        self.core_index = self.NA_to_core_index(0.13, self.clad_index)
        self.clad_radius = 33 / 2
        self.core_radius = 4.5

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class NewB(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.11, self.silica_index)
        self.core_index = self.NA_to_core_index(0.115, self.clad_index)
        self.clad_radius = 33 / 2
        self.core_radius = 4.5

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class F2028M24(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.19, self.silica_index)
        self.core_index = self.NA_to_core_index(0.11, self.clad_index)
        self.clad_radius = 14.1 / 2
        self.core_radius = 2.3 / 2

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class F2028M21(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.19, self.silica_index)
        self.core_index = self.NA_to_core_index(0.11, self.clad_index)
        self.clad_radius = 17.6 / 2
        self.core_radius = 2.8 / 2

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class NewC(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.11, self.silica_index)
        self.core_index = self.NA_to_core_index(0.115, self.clad_index)
        self.clad_radius = 30 / 2
        self.core_radius = 9.1 / 2

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class NewD(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.11, self.silica_index)
        self.core_index = self.NA_to_core_index(0.13, self.clad_index)
        self.clad_radius = 28 / 2
        self.core_radius = 9.3 / 2

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class F2058L1(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.117, self.silica_index)
        self.core_index = self.NA_to_core_index(0.13, self.clad_index)
        self.clad_radius = 19.6 / 2
        self.core_radius = 9.0 / 2

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class F2058G1(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.115, self.silica_index)
        self.core_index = self.NA_to_core_index(0.124, self.clad_index)
        self.clad_radius = 32.3 / 2
        self.core_radius = 9.0 / 2

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class F2028M12(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.clad_index = self.NA_to_core_index(0.19, self.silica_index)
        self.core_index = self.NA_to_core_index(0.11, self.clad_index)
        self.clad_radius = 25.8 / 2
        self.core_radius = 4.1 / 2

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.clad_radius, index=self.clad_index),
                           Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class SMF28(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.NA = 0.12
        self.clad_index = self.silica_index
        self.core_index = self.clad_index + 0.005  # NA_to_core_index( 0.14, self.clad_index )
        self.clad_radius = 62.5
        self.core_radius = 4.1

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.core_radius, index=self.core_index)]


class HP630(GenericFiber):
    wavelength: float

    def __post_init__(self):
        self.NA = 0.12
        self.clad_index = self.silica_index
        self.core_index = self.NA_to_core_index(0.13, self.clad_index)
        self.clad_radius = 62.5
        self.core_radius = 3.5 / 2.

    def initialize_polygones(self):
        self._polygones = [Circle(position=self.position, radius=self.core_radius, index=self.core_index)]

# -
