# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional, List
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer

from .HeroData import HeroData
from .HeroStruct import HeroStruct
from .HeroDataType import HeroDataType
from .Contour import Contour

class HeroContour(HeroData):

    def __init__(self, contour_set: List[Contour], name: str = "", metadata=None):
        HeroData.__init__(self)

        if self._validate_contour_set(contour_set):
            self._contour_set = contour_set
        else:
            raise ValueError("The contour set must be a list of Contours.")

        if self._validate_name(name):
            self._name = name
        else:
            raise ValueError("The name must be a string.")

        if metadata is None:
            self._metadata = dict()
        else:
            if self._validate_metadata(metadata):
                self._metadata = metadata
            else:
                raise ValueError("The metadata must be a dictionary of Hero data types.")

    def __repr__(self):
        string = "HeroContours("
        string += f"name={self._name}, "
        string += f"contour_set={{n = {len(self._contour_set)}}}"
        string += ")"
        return string
    
    def __str__(self):
        string = f'HeroContours: \n'
        string += f'  ----------------------------------\n'
        string += f'  Name: {self._name}\n'
        string += f'  Number of contours: {len(self._contour_set)}\n'
        string += f'  ----------------------------------\n'
        return string

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value):
        if self._validate_name(value):
            self._name = value
        else:
            raise ValueError("The name must be a string.")

    @Name.deleter
    def Name(self):
        raise AttributeError("Attribute 'name' is not deletable.")

    @property
    def ContourSet(self):
        return self._contour_set

    @ContourSet.setter
    def ContourSet(self, value):
        if self._validate_contour_set(value):
            self._contour_set = value
        else:
            raise ValueError("The contour set must be a list of Contours.")

    @ContourSet.deleter
    def ContourSet(self):
        raise AttributeError("Attribute 'contour_set' is not deletable.")

    @property
    def Metadata(self):
        return self._metadata

    @Metadata.setter
    def Metadata(self, value):
        if self._validate_metadata(value):
            self._metadata = value
        else:
            raise ValueError("The metadata must be a dictionary of Hero data types.")

    @Metadata.deleter
    def Metadata(self):
        raise AttributeError("Attribute 'metadata' is not deletable.")
            
    @staticmethod
    def _validate_contour_set(cs):
        if not isinstance(cs, list):
            return False
        for item in cs:
            if not isinstance(item, Contour):
                return False
        return True

    @staticmethod
    def _validate_name(name):
        return isinstance(name, str)

    @staticmethod
    def _validate_metadata(md):
        try:
            # See if it can be a hero struct.
            HeroStruct(md)
        except:
            return False
        return True

    @staticmethod
    def create_from_dict(data: dict):
        return HeroContour(data["_contour_set"], data["_name"], data["_metadata"])

    def __eq__(self, other: HeroContour):
        if not super(HeroContour, self).__eq__(other):
            return False
        if self._name != other._name:
            return False
        if not self._compare_lists(self._contour_set, other._contour_set):
            return False
        if not self._equal_meta_data(self._metadata, other._metadata):
            return False
        return True

    @staticmethod
    def _compare_lists(l1: list, l2: list):
        if len(l1) != len(l2):
            return False
        for i in range(len(l1)):
            if l1[i] != l2[i]:
                return False
        return True

    @staticmethod
    def _equal_meta_data(m1, m2):
        if isinstance(m1, dict):
            m1 = HeroStruct(m1)
        if isinstance(m2, dict):
            m2 = HeroStruct(m2)
        return m1 == m2

    def get_container_id(self):
        return id(self)

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "HeroContour"

    # Datatype attributes.
    _attributes = Attributes("HCs", version=0, member_count=3)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(HeroContour, self).serialize(writer_fun)
        writer_fun(self._contour_set, "Contour{}", "ContourSet", None)
        writer_fun(self._metadata, "HeroStruct", "Metadata", None)
        writer_fun(self._name, "String", "Name", None)

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(HeroContour, HeroContour).deserialize(reader_fun)
        data["_contour_set"], _ = reader_fun("Contour{}", None)
        data["_metadata"], _ = reader_fun("HeroStruct", None)
        data["_name"], _ = reader_fun("String", None)
        return data
