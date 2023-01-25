from typing import Union, Dict
from datetime import datetime, timedelta
from ..models.parametervalue import ParameterValue, ParameterValueType
import ctypes

from ..native.Python.InteropHelpers.InteropUtils import InteropUtils as iu
from ..native.Python.InteropHelpers.ExternalTypes.System.Array import Array as ai
from ..native.Python.InteropHelpers.ExternalTypes.System.Dictionary import Dictionary as di
from ..helpers.dotnet.datetimeconverter import DateTimeConverter as dtc
from ..native.Python.QuixSdkStreaming.Models.ParameterDataTimestamp import ParameterDataTimestamp as pdti

from ..helpers.nativedecorator import nativedecorator


@nativedecorator
class ParameterDataTimestamp:
    """
    Represents a single point in time with parameter values and tags attached to that time
    """

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
            Initializes a new instance of ParameterDataTimestamp.

            Parameters:

            net_pointer: Pointer to an instance of a .net ParameterDataTimestamp.
        """
        if net_pointer is None:
            raise Exception("ParameterDataTimestamp constructor should not be invoked without a .net pointer")

        self.__interop = pdti(net_pointer)
        self.__parameters = None  # to cache whatever is read from .net
        self.__tags = None  # to cache whatever is read from .net

    def __finalizerfunc(self):
        self.__clear_parameters()

    def __clear_parameters(self):
        if self.__parameters is None:
            return
        [pval.dispose() for (pname, pval) in self.__parameters.items()]
        self.__parameters = None

    def __str__(self):
        text = "Time:" + str(self.timestamp_nanoseconds)
        text += "\r\n  Tags: " + str(self.tags)
        text += "\r\n  Params:"
        for param_id, param_val in self.parameters.items():
            if param_val.type == ParameterValueType.Numeric:
                text += "\r\n    " + str(param_id) + ": " + str(param_val.numeric_value)
                continue
            if param_val.type == ParameterValueType.String:
                text += "\r\n    " + str(param_id) + ": " + str(param_val.string_value)
                continue
            if param_val.type == ParameterValueType.Binary:
                text += "\r\n    " + str(param_id) + ": byte[" + str(len(param_val.binary_value)) + "]"
                continue
            if param_val.type == ParameterValueType.Empty:
                text += "\r\n    " + str(param_id) + ": Empty"
                continue
            text += "\r\n    " + str(param_id) + ": ???"
        return text

    @property
    def parameters(self) -> Dict[str, ParameterValue]:
        """
        Parameter values for the timestamp. When a key is not found, returns empty ParameterValue
        The dictionary key is the parameter id
        The dictionary value is the value (ParameterValue)
        """

        if self.__parameters is None:
            def _value_converter_to_python(net_hptr: ctypes.c_void_p):
                if net_hptr is None:
                    return None
                return ParameterValue(net_hptr)


            try:
                parameters_hptr = self.__interop.get_Parameters()
                self.__parameters = di.ReadAnyStringReferenceDictionary(parameters_hptr, _value_converter_to_python)
            finally:
                iu.free_hptr(parameters_hptr)

        return self.__parameters

    @property
    def tags(self) -> Dict[str, str]:
        """
        Tags for the timestamp.
        The dictionary key is the tag id
        The dictionary value is the tag value
        """

        if self.__tags is None:
            try:
                tags_hptr = self.__interop.get_Tags()
                if tags_hptr is None:
                    self.__tags = {}
                else:
                    self.__tags = di.ReadAnyStringStringDictionary(tags_hptr)
            finally:
                iu.free_hptr(tags_hptr)

        return self.__tags

    @property
    def timestamp_nanoseconds(self) -> int:
        """Gets timestamp in nanoseconds"""

        return self.__interop.get_TimestampNanoseconds()

    @property
    def timestamp_milliseconds(self) -> int:
        """Gets timestamp in milliseconds"""

        return self.__interop.get_TimestampMilliseconds()

    @property
    def timestamp(self) -> datetime:
        """Gets the timestamp in datetime format"""
        return dtc.datetime_to_python(self.__interop.get_Timestamp())

    @property
    def timestamp_as_time_span(self) -> timedelta:
        """Gets the timestamp in timespan format"""
        return dtc.timespan_to_python(self.__interop.get_TimestampAsTimeSpan())

    def add_value(self, parameter_id: str, value: Union[float, str, int, bytearray, bytes]) -> 'ParameterDataTimestamp':
        """
            Adds a new value for the parameter
            :param parameter_id: The parameter to add the value for
            :param value: the value to add. Can be float or string

        :return: ParameterDataTimestamp
        """

        if type(value) is int:
            value = float(value)

        val_type = type(value)
        if val_type is float:
            new = pdti(self.__interop.AddValue(parameter_id, value))
            if new != self.__interop:
                self.__interop._dispose_ptr()
                self.__interop = new
        elif val_type is str:
            new = pdti(self.__interop.AddValue2(parameter_id, value))
            if new != self.__interop:
                self.__interop._dispose_ptr()
                self.__interop = new
        elif val_type is bytearray or val_type is bytes:
            uptr = ai.WriteBytes(value)
            try:
                new = pdti(self.__interop.AddValue3(parameter_id, uptr))
            finally:
                iu.free_uptr(uptr)
            if new != self.__interop:
                self.__interop._dispose_ptr()
                self.__interop = new

        return self

    def remove_value(self, parameter_id: str) -> 'ParameterDataTimestamp':
        """
            Removes the value for the parameter
            :param parameter_id: The parameter to remove the value for

        :return: ParameterDataTimestamp
        """
        new = pdti(self.__interop.RemoveValue(parameter_id))
        if new != self.__interop:
            self.__interop._dispose_ptr()
            self.__interop = new
        return self

    def add_tag(self, tag_id: str, tag_value: str) -> 'ParameterDataTimestamp':
        """
            Adds a tag to the values
            :param tag_id: The id of the tag to the set the value for
            :param tag_value: the value to set

        :return: ParameterDataTimestamp
        """
        tags = self.tags  # force evaluation of the local cache
        tags[tag_id] = tag_value
        self.__interop.AddTag(tag_id, tag_value)
        return self

    def remove_tag(self, tag_id: str) -> 'ParameterDataTimestamp':
        """
            Removes a tag from the values
            :param tag_id: The id of the tag to remove

        :return: ParameterDataTimestamp
        """
        tags = self.tags  # force evaluation of the local cache
        tags.pop(tag_id)
        self.__interop.RemoveTag(tag_id)
        return self

    def add_tags(self, tags: Dict[str, str]) -> 'ParameterDataTimestamp':
        """
            Copies the tags from the specified dictionary. Conflicting tags will be overwritten
            :param tags: The tags to add

        :return: ParameterDataTimestamp
        """

        if tags is None:
            return self

        existing_tags = self.tags

        for key, val in tags.items():
            existing_tags[key] = val

        #self.__interop.AddTags() # TODO
        return self

    def get_net_pointer(self) -> ctypes.c_void_p:
        return self.__interop._get_interop_ptr()
