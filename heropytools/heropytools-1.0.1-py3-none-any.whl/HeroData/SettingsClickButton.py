# *************************************************************** #
#               Copyright © Hero Imaging AB 2022. 				  #
#  					  All Rights Reserved.						  #
# *************************************************************** #

from __future__ import annotations
from typing import Callable, Any, Optional
from heropytools.Serialization.Attributes import Attributes
from heropytools.Serialization.CustomSerializer import CustomSerializer

from .SettingsValue import SettingsValue


class SettingsClickButton(SettingsValue):

    def __init__(self, value=False, name="Ok", read_only=False, visible=True, description="", can_be_input=False, is_input=False, full_input_name=True):

        SettingsValue.__init__(self, read_only, visible, description, can_be_input, is_input, full_input_name)
        self._value = value
        self._name = name

    @staticmethod
    def create_from_dict(data: dict):
        s = SettingsClickButton(data["_value"], data["_name"], data["_read_only"], data["_visible"], data["_description"], data["_can_be_input"], 
                     data["_is_input"], data["_full_input_name"])
        s._id = data["_id"]
        return s

    def __eq__(self, other):
        return super(SettingsClickButton, self).__eq__(other) and self._value == other._value and self._name == other._name

    # --- Autogenerated --- #

    # Name of the type.
    _type_str = "SettingsClickButton"

    # Datatype attributes.
    _attributes = Attributes("SettingsClickButton", version=0, member_count=9)

    # Serialization.
    def serialize(self, writer_fun: Callable[[Any, str, str, Optional[CustomSerializer]], None]):
        super(SettingsClickButton, self).serialize(writer_fun)
        writer_fun(self._name, "String", "Name", None)
        writer_fun(self._value, "Boolean", "V", None)

    # Deserialization.
    @staticmethod
    def deserialize(reader_fun: Callable[[str, Optional[CustomSerializer]], Any]):
        data = super(SettingsClickButton, SettingsClickButton).deserialize(reader_fun)
        data["_name"], _ = reader_fun("String", None)
        data["_value"], _ = reader_fun("Boolean", None)
        return data
