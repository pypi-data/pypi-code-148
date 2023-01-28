#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
from dataclasses import dataclass

# Local imports
from FiberFusing.buffer import Circle, Point


@dataclass
class FiberRing():
    angle_list: list
    fusion_degree: float
    fiber_radius: float

    def __post_init__(self):
        self.n_fiber = len(self.angle_list)

        self._fibers = None
        self._core_shift = None
        self._centers = None
        self._max_distance = None

    @property
    def MaxDistance(self):
        if self._max_distance is None:
            self.compute_max_distance()
        return self._max_distance

    @property
    def Fibers(self):
        if self._fibers is None:
            self.compute_fibers()
        return self._fibers

    @property
    def centers(self):
        if self._centers is None:
            self.compute_centers()
        return self._centers

    @property
    def core_shift(self):
        if self._core_shift is None:
            self.compute_core_shift()
        return self._core_shift

    def compute_fibers(self):
        self._fibers = []

        for n, point in enumerate(self.centers):
            fiber = Circle(radius=self.fiber_radius, position=point, name=f' Fiber {n}')
            self._fibers.append(fiber)

    def compute_core_shift(self):
        if self.fusion_degree == 0:
            self._core_shift = 0
        else:
            alpha = (2 - self.n_fiber) * numpy.pi / (2 * self.n_fiber)

            self._core_shift = (1 + numpy.cos(alpha)) - numpy.sqrt(self.n_fiber) * numpy.cos(alpha)

            self._core_shift = (self.fiber_radius - (self._core_shift * self.fiber_radius) * self.fusion_degree)

            self._core_shift *= 1 / (numpy.cos(alpha))

    def compute_centers(self):
        self._centers = [Point(position=[0, self.core_shift]).rotate(angle=angle, origin=[0, 0]) for angle in self.angle_list]

    def compute_max_distance(self):
        x, y = self.Fibers[0].exterior.xy
        x = numpy.asarray(x)
        y = numpy.asarray(y)

        self._max_distance = numpy.sqrt(x**2 + y**2).max()
