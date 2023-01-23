# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer

from .SettingsValueArray import SettingsValueArray


class SettingsBoolArray(SettingsValueArray):

    def __init__(self, value, min_number_of_elements = 0, max_number_of_elements = 64, read_only=False, visible=True, description="", can_be_input=False, is_input=False, full_input_name=True):

        SettingsValueArray.__init__(self, min_number_of_elements, max_number_of_elements, read_only, visible, description, can_be_input, is_input, full_input_name)
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        raise AttributeError("Attribute is not writable.")

    @value.deleter
    def value(self):
        raise AttributeError("Attribute is not deletable.")

    @staticmethod
    def create_from_dict(data: dict):
        s = SettingsBoolArray(data["_value"], data["_min_number_of_elements"], data["_max_number_of_elements"], data["_read_only"], data["_visible"], data["_description"], data["_can_be_input"], 
                     data["_is_input"], data["_full_input_name"])
        s._id = data["_id"]
        return s

    def __eq__(self, other):
        return super(SettingsBoolArray, self).__eq__(other) and self._compare_lists(self._value, other._value)

    def __repr__(self) -> str:
        return f'BoolList: [value: {self.value}, ' + super().__repr__()

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "SettingsBoolArray"

    # Datatype attributes.
    _attributes = Attributes("SettingsBoolArray", version=0, member_count=10)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(SettingsBoolArray, self).serialize(writer_fun)
        writer_fun(self._value, "Boolean[]", "V", None)

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(SettingsBoolArray, SettingsBoolArray).deserialize(reader_fun)
        data["_value"], _ = reader_fun("Boolean[]", None)
        return data
