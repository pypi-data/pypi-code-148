from datetime import datetime, timedelta
from typing import Dict, Union


from ..helpers.timeconverter import TimeConverter
from ..helpers.dotnet.datetimeconverter import DateTimeConverter

import pandas as pd

from ..native.Python.QuixSdkStreaming.Models.EventData import EventData as edi
from ..native.Python.InteropHelpers.ExternalTypes.System.Dictionary import Dictionary as di
from ..native.Python.InteropHelpers.InteropUtils import InteropUtils as iu
import ctypes
from ..helpers.nativedecorator import nativedecorator


@nativedecorator
class EventData(object):
    """
    Represents a single point in time with event value and tags attached to it
    """

    def __init__(self, event_id: str = None, time: Union[int, str, datetime, pd.Timestamp] = None, value: str = None, net_pointer: ctypes.c_void_p = None):
        """
            Initializes a new instance of EventData.

            Parameters:
            :param event_id: the unique id of the event the value belongs to
            :param time: the time at which the event has occurred in nanoseconds since epoch or as a datetime
            :param value: the value of the event
            :param net_pointer: Pointer to an instance of a .net EventData
        """
        if net_pointer is None:
            if event_id is None:
                raise Exception("event_id must be set")
            if time is None:
                raise Exception("time must be set")
            converted_time = EventData.__convert_time(time)
            self.__interop = edi(edi.Constructor(eventId=event_id, timestampNanoseconds=converted_time, eventValue=value))
        else:
            self.__interop = edi(net_pointer)

    @staticmethod
    def __convert_time(time):
        if isinstance(time, datetime):
            if isinstance(time, pd.Timestamp):
                time = time.to_pydatetime()
            return TimeConverter.to_unix_nanoseconds(time)
        if isinstance(time, str):
            return TimeConverter.from_string(time)
        return time

    def __str__(self):
        text = "Time: " + str(self.timestamp_nanoseconds)
        text += "\r\n  Tags: " + str(self.tags)
        text += "\r\n  Value: " + str(self.value)
        return text

    @property
    def id(self) -> str:
        """Gets the globally unique identifier of the event"""
        return self.__interop.get_Id()

    @id.setter
    def id(self, value: str) -> None:
        """Sets the globally unique identifier of the event"""
        self.__interop.set_Id(value)

    @property
    def value(self) -> str:
        """Gets the value of the event"""
        return self.__interop.get_Value()

    @value.setter
    def value(self, value: str) -> None:
        """Sets the value of the event"""
        self.__interop.set_Value(value)

    @property
    def tags(self) -> Dict[str, str]:
        """
        Tags for the timestamp. When key is not found, returns None
        The dictionary key is the tag id
        The dictionary value is the tag value
        """

        tags_hptr = self.__interop.get_Tags()
        try:
            return di.ReadStringStringDictionary(tags_hptr)
        finally:
            iu.free_hptr(tags_hptr)

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

        dt_hptr = self.__interop.get_Timestamp()
        return DateTimeConverter.datetime_to_python(dt_hptr)

    @property
    def timestamp_as_time_span(self) -> timedelta:
        """Gets the timestamp in timespan format"""

        ts_uptr = self.__interop.get_TimestampAsTimeSpan()
        return DateTimeConverter.timespan_to_python(ts_uptr)

    def clone(self):
        """ Clones the event data """
        cloned_pointer = self.__interop.Clone()
        return EventData(net_pointer=cloned_pointer)

    def add_tag(self, tag_id: str, tag_value: str) -> 'EventData':
        """
            Adds a tag to the event
            :param tag_id: The id of the tag to the set the value for
            :param tag_value: the value to set

        :return: EventData
        """
        hptr = self.__interop.AddTag(tag_id, tag_value)
        iu.free_hptr(hptr)
        return self

    def add_tags(self, tags: Dict[str, str]) -> 'EventData':
        """
            Adds the tags from the specified dictionary. Conflicting tags will be overwritten
            :param tags: The tags to add

        :return: EventData
        """

        if tags is None:
            return self

        for key, val in tags.items():
            self.__interop.AddTag(key, val)
        return self

    def remove_tag(self, tag_id: str) -> 'EventData':
        """
            Removes a tag from the event
            :param tag_id: The id of the tag to remove

        :return: EventData
        """
        hptr = self.__interop.RemoveTag(tag_id)
        iu.free_hptr(hptr)
        return self

    """
    Get associated .net object pointer
    """
    def get_net_pointer(self):
        return self.__interop._get_interop_ptr()
