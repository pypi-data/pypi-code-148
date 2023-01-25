from .eventhook import EventHook
from .models import *
from datetime import datetime
from .models.streamwriter import *

import ctypes

from .native.Python.InteropHelpers.InteropUtils import InteropUtils
from .native.Python.QuixSdkStreaming.IStreamWriter import IStreamWriter as swi
from .native.Python.QuixSdkProcess.Models.StreamEndType import StreamEndType as StreamEndTypeInterop
from .helpers.enumconverter import EnumConverter as ec
from .helpers.dotnet.datetimeconverter import DateTimeConverter as dtc
from .helpers.nativedecorator import nativedecorator


@nativedecorator
class StreamWriter(object):
    """
        Handles writing stream to a topic
    """

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
            Initializes a new instance of StreamWriter.
            NOTE: Do not initialize this class manually, use StreamingClient.create_stream to write streams

            Parameters:

            net_object (.net object): The .net object representing a StreamWriter
        """

        if net_pointer is None:
            raise Exception("StreamWriter is none")

        self.__cfuncrefs = []  # exists to hold onto the references created by the interop layer to avoid GC'ing them
        self.__interop = swi(net_pointer)
        self.__streamParametersWriter = None  # Holding reference to avoid GC
        self.__streamEventsWriter = None  # Holding reference to avoid GC
        self.__streamPropertiesWriter = None  # Holding reference to avoid GC

        def __on_write_exception_net_handler(sender: ctypes.c_void_p, arg: ctypes.c_void_p):
            # TODO fix arg to be handled as exception
            self.on_write_exception.fire(self, BaseException(arg.Message, type(arg)))
            InteropUtils.free_hptr(sender)

        def __on_first_sub_on_write_exception_net():
            ref = self.__interop.add_OnWriteException(__on_write_exception_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_unsub_on_write_exception_net():
            # TODO do unsign with previous handler
            self.__interop.remove_OnWriteException(__on_write_exception_net_handler)

        self.on_write_exception = EventHook(__on_first_sub_on_write_exception_net, __on_last_unsub_on_write_exception_net, name="StreamWriter.on_write_exception")
        """Raised when an exception occurred during the writing processes
         Parameters:     
            exception (BaseException): The occurred exception
        """

    def __finalizerfunc(self):
        if self.__streamParametersWriter is not None:
            self.__streamParametersWriter.dispose()
        if self.__streamEventsWriter is not None:
            self.__streamEventsWriter.dispose()
        if self.__streamPropertiesWriter is not None:
            self.__streamPropertiesWriter.dispose()
        self.__cfuncrefs = None

    @property
    def stream_id(self) -> str:
        """Gets the unique id the stream being written"""
        return self.__interop.get_StreamId()

    @property
    def epoch(self) -> datetime:
        """Gets the default Epoch used for Parameters and Events"""

        ptr = self.__interop.get_Epoch()
        value = dtc.datetime_to_python(ptr)
        return value

    @epoch.setter
    def epoch(self, value: datetime):
        """Set the default Epoch used for Parameters and Events"""
        dotnet_value = dtc.datetime_to_dotnet(value)
        self.__interop.set_Epoch(dotnet_value)

    @property
    def properties(self) -> StreamPropertiesWriter:
        """Properties of the stream. The changes will automatically be sent after a slight delay"""
        if self.__streamPropertiesWriter is None:
            self.__streamPropertiesWriter = StreamPropertiesWriter(self.__interop.get_Properties())
        return self.__streamPropertiesWriter

    @property
    def parameters(self) -> StreamParametersWriter:
        """Helper for doing anything related to parameters of the stream. Use to send parameter definitions,
        groups or values """

        if self.__streamParametersWriter is None:
            self.__streamParametersWriter = StreamParametersWriter(self.__interop.get_Parameters())
        return self.__streamParametersWriter

    @property
    def events(self) -> StreamEventsWriter:
        """Helper for doing anything related to events of the stream. Use to send event definitions, groups or
        values. """
        if self.__streamEventsWriter is None:
            self.__streamEventsWriter = StreamEventsWriter(self.__interop.get_Events())
        return self.__streamEventsWriter

    def close(self, end_type: StreamEndType = StreamEndType.Closed):
        """
            Close the stream and flush the pending data to stream
        """

        dotnet_end_type = ec.enum_to_another(end_type, StreamEndTypeInterop)

        self.__interop.Close(dotnet_end_type)
        self.dispose()

