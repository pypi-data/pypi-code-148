"""
Author: Calixte Mayoraz (https://gitlab.com/calixtemayoraz)
Created: 2023-01-23

Quite simple code to hold all these values, make them easily readable, and iterable.
"""
from enum import Enum


class _GrafanaColor(Enum):
    """
    Basic enumeration for all the Grafana Colors
    """
    RED = ("#AD0317", "#C4162A", "#E02F44", "#F2495C", "#FF7383")
    ORANGE = ("#E55400", "#FA6400", "#FF780A", "#FF9830", "#FFB357")
    YELLOW = ("#CC9D00", "#E0B400", "#F2CC0C", "#FADE2A", "#FFEE52")
    GREEN = ("#19730E", "#37872D", "#56A64B", "#73BF69", "#96D98D")
    BLUE = ("#1250B0", "#1F60C4", "#3274D9", "#5794F2", "#8AB8FF")
    PURPLE = ("#7C2EA3", "#8F3BB8", "#A352CC", "#B877D9", "#CA95E5")


class classproperty:
    """
    Thanks to this answer from stackoverflow for the hint:
    https://stackoverflow.com/a/5192374
    """
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class GrafanaColor(str):
    _GRAFANA_COLOR_NAMES = [color.name for color in _GrafanaColor]

    def __iter__(self):
        # we start the color at the first color
        self.__color_index = 0
        # but we start the shade at the middle (normal)
        self.__shade_index = round(len(_GrafanaColor.RED.value) / 2)
        return self

    def __next__(self) -> str:
        # set the color and shade indices...
        c = self.__color_index
        s = self.__shade_index
        self.__color_index += 1
        # check color index rollback
        if self.__color_index >= len(_GrafanaColor.__members__.values()):
            self.__color_index = 0
            # increment shade index
            self.__shade_index += 1
            # check shade index rollback
            if self.__shade_index >= len(_GrafanaColor.RED.value):
                self.__shade_index = 0
        # return the correct color and shade.
        return _GrafanaColor[self._GRAFANA_COLOR_NAMES[c]].value[s]

    @classproperty
    def iterator(cls):
        """Grafana Red colors"""
        return iter(cls('RED'))

    @classproperty
    def RED(cls):
        """Grafana Red colors"""
        return cls('RED')

    @classproperty
    def ORANGE(cls):
        """Grafana Orange colors"""
        return cls('ORANGE')

    @classproperty
    def YELLOW(cls):
        """Grafana Yellow colors"""
        return cls('YELLOW')

    @classproperty
    def GREEN(cls):
        """Grafana Green colors"""
        return cls('GREEN')

    @classproperty
    def BLUE(cls):
        """Grafana Blue colors"""
        return cls('BLUE')

    @classproperty
    def PURPLE(cls):
        """Grafana Purple colors"""
        return cls('PURPLE')

    @property
    def darker(self) -> str:
        """Darker shade"""
        return self.__color.value[0]

    @property
    def dark(self) -> str:
        """Dark shade"""
        return self.__color.value[1]

    @property
    def normal(self) -> str:
        """Normal shade"""
        return self.__color.value[2]

    @property
    def light(self) -> str:
        """Light shade"""
        return self.__color.value[3]

    @property
    def lighter(self) -> str:
        """Lighter shade"""
        return self.__color.value[4]

    def __repr__(self) -> str:
        """
        Default string representation is "normal"
        """
        return self.normal

    def __str__(self) -> str:
        """
        Default string representation is "normal"
        """
        return self.normal

    def __init__(self, name: str):
        self.__color = _GrafanaColor[name]

