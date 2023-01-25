from typing import List

from ...eventhook import EventHook

from ...models.eventdefinition import EventDefinition
from ...models.eventdata import EventData

from ...native.Python.QuixSdkStreaming.Models.StreamReader.StreamEventsReader import StreamEventsReader as seri
from ...native.Python.InteropHelpers.InteropUtils import InteropUtils
from ...native.Python.InteropHelpers.ExternalTypes.System.Enumerable import Enumerable as ei
from ...native.Python.InteropHelpers.ExternalTypes.System.Array import Array as ai
import ctypes
from ...helpers.nativedecorator import nativedecorator


@nativedecorator
class StreamEventsReader(object):

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
            Initializes a new instance of StreamEventsReader.
            NOTE: Do not initialize this class manually, use StreamReader.events to access an instance of it

            Parameters:

            net_pointer (.net object): Pointer to an instance of a .net StreamEventsReader
        """
        if net_pointer is None:
            raise Exception("StreamEventsReader is none")

        self.__cfuncrefs = []  # exists to hold onto the references created by the interop layer to avoid GC'ing them
        self.__interop = seri(net_pointer)

        def __on_read_net_handler(arg):
            self.on_read.fire(EventData(net_pointer=arg))

        def __on_first_read_sub():
            ref = self.__interop.add_OnRead(__on_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_read_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnRead(__on_read_net_handler)

        self.on_read = EventHook(__on_first_read_sub, __on_last_read_unsub, name="StreamEventsReader.on_read")
        """
        Raised when an event data package is read for the stream

        Has one argument of type EventData
        """

        def __on_def_net_handler():
            self.on_definitions_changed.fire()

        def __on_first_def_sub():
            ref = self.__interop.add_OnDefinitionsChanged(__on_def_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_def_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnDefinitionsChanged(__on_def_net_handler)

        self.on_definitions_changed = EventHook(__on_first_def_sub, __on_last_def_unsub, name="StreamEventsReader.on_definitions_changed")
        """
        Raised when the definitions have changed for the stream. Access "definitions" for latest set of event definitions 

        Has no arguments
        """

    def __finalizerfunc(self):
        self.__cfuncrefs = None

    @property
    def definitions(self) -> List[EventDefinition]:
        """ Gets the latest set of event definitions """

        try:
            defs = self.__interop.get_Definitions()

            asarray = ei.ReadReferences(defs)

            return [EventDefinition(hptr) for hptr in asarray]
        finally:
            InteropUtils.free_hptr(defs)
