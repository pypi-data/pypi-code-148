# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer

from .SettingsValue import SettingsValue


class SettingsBool(SettingsValue):

    def __init__(self, value=False, readOnly=False, visible=True, description="", canBeInput=False, isInput=False, fullInputName=True):

        SettingsValue.__init__(self, readOnly, visible, description, canBeInput, isInput, fullInputName)
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
        s = SettingsBool(data["_value"], data["_read_only"], data["_visible"], data["_description"], data["_can_be_input"], 
                     data["_is_input"], data["_full_input_name"])
        s._id = data["_id"]
        return s

    def __eq__(self, other):
        return super(SettingsBool, self).__eq__(other) and self._value == other._value
    
    def __repr__(self) -> str:
        return f'Bool: [value: {self.value}, ' + super().__repr__()
    

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "SettingsBool"

    # Datatype attributes.
    _attributes = Attributes("SettingsBool", version=0, member_count=8)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(SettingsBool, self).serialize(writer_fun)
        writer_fun(self._value, "Boolean", "V", None)

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(SettingsBool, SettingsBool).deserialize(reader_fun)
        data["_value"], _ = reader_fun("Boolean", None)
        return data
