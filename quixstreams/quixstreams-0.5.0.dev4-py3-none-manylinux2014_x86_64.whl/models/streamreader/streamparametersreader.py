from typing import List

from ...eventhook import EventHook

from ..parameterdefinition import ParameterDefinition
from ...models.parameterdataraw import ParameterDataRaw
from ...models.parameterdata import ParameterData
from ...models.parametersbufferconfiguration import ParametersBufferConfiguration
from ...models.streamreader.parametersbufferreader import ParametersBufferReader


from ...native.Python.QuixSdkStreaming.Models.StreamReader.StreamParametersReader import StreamParametersReader as spri
from ...native.Python.InteropHelpers.InteropUtils import InteropUtils
from ...native.Python.InteropHelpers.ExternalTypes.System.Enumerable import Enumerable as ei
from ...native.Python.InteropHelpers.ExternalTypes.System.Array import Array as ai
import ctypes
from ...helpers.nativedecorator import nativedecorator


@nativedecorator
class StreamParametersReader(object):

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
            Initializes a new instance of StreamParametersReader.
            NOTE: Do not initialize this class manually, use StreamReader.parameters to access an instance of it

            Parameters:

            net_pointer (.net object): Pointer to an instance of a .net StreamParametersReader
        """
        if net_pointer is None:
            raise Exception("StreamParametersReader is none")

        #TODOTEMP self.__weakref = weakref.ref(self, lambda x: print("De-referenced StreamParametersReader " + str(net_pointer)))
        self.__cfuncrefs = []  # exists to hold onto the references created by the interop layer to avoid GC'ing them
        self.__interop = spri(net_pointer)
        self.__buffers = []

        def __on_definitions_changed_net_handler():
            self.on_definitions_changed.fire()

        def __on_first_definitons_sub():
            ref = self.__interop.add_OnDefinitionsChanged(__on_definitions_changed_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_definitons_unsub():
            # TODO fix unsub
            self.__interop.remove_OnDefinitionsChanged(__on_definitions_changed_net_handler)

        self.on_definitions_changed = EventHook(__on_first_definitons_sub, __on_last_definitons_unsub, name="StreamParametersReader.on_definitions_changed")
        """
        Raised when the definitions have changed for the stream. Access "definitions" for latest set of parameter definitions 

        Has no arguments
        """

        def __on_read_net_handler(arg):
            self.on_read.fire(ParameterData(arg))

        def __on_first_sub():
            ref = self.__interop.add_OnRead(__on_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_unsub():
            # TODO fix unsub
            self.__interop.remove_OnRead(__on_read_net_handler)

        self.on_read = EventHook(__on_first_sub, __on_last_unsub, name="StreamParametersReader.on_read")
        """
        Event raised when data is available to read (without buffering) 
        This event does not use Buffers and data will be raised as they arrive without any processing.

        Has one argument of type ParameterData
        """


        def __on_read_raw_net_handler(arg):
            converted = ParameterDataRaw(arg)
            self.on_read_raw.fire(converted)

        def __on_first_raw_sub():
            ref = self.__interop.add_OnReadRaw(__on_read_raw_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_raw_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnReadRaw(__on_read_raw_net_handler)

        self.on_read_raw = EventHook(__on_first_raw_sub, __on_last_raw_unsub, name="StreamParametersReader.on_read_raw")
        """
        Event raised when data is available to read (without buffering) in raw transport format 
        This event does not use Buffers and data will be raised as they arrive without any processing. 

        Has one argument of type ParameterDataRaw 
        """

        def __on_read_df_net_handler(arg):
            with (pdrw := ParameterDataRaw(arg)):
                converted = pdrw.to_panda_frame()
            self.on_read_pandas.fire(converted)

        def __on_first_df_sub():
            ref = self.__interop.add_OnReadRaw(__on_read_df_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_df_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnReadRaw(__on_read_df_net_handler)

        self.on_read_pandas = EventHook(__on_first_df_sub, __on_last_df_unsub, name="StreamParametersReader.on_read_pandas")
        """
        Event raised when data is available to read (without buffering) in raw transport format 
        This event does not use Buffers and data will be raised as they arrive without any processing. 

        Has one argument of type ParameterDataRaw 
        """

    def __finalizerfunc(self):
        [buffer.dispose() for buffer in self.__buffers]
        self.__cfuncrefs = None

    @property
    def definitions(self) -> List[ParameterDefinition]:
        """ Gets the latest set of parameter definitions """

        try:
            defs = self.__interop.get_Definitions()

            asarray = ei.ReadReferences(defs)

            return [ParameterDefinition(hptr) for hptr in asarray]
        finally:
            InteropUtils.free_hptr(defs)

    def create_buffer(self, *parameter_filter: str, buffer_configuration: ParametersBufferConfiguration = None) -> ParametersBufferReader:
        """
        Creates a new buffer for reading data according to the provided parameter_filter and buffer_configuration
        :param parameter_filter: 0 or more parameter identifier to filter as a whitelist. If provided, only these
            parameters will be available through this buffer
        :param buffer_configuration: an optional ParameterBufferConfiguration.

        :returns: a ParametersBufferReader which will raise new parameters read via .on_read event
        """

        actual_filters_ptr = None
        if parameter_filter is not None:
            filters = []
            for param_filter in parameter_filter:
                if isinstance(param_filter, ParametersBufferConfiguration):
                    buffer_configuration = param_filter
                    break
                filters.append(param_filter)
            if len(filters) > 0:
                actual_filters_ptr = ai.ParseStrings(filters)

        buffer = None
        if buffer_configuration is not None:
            buffer_config_ptr = buffer_configuration.get_net_pointer()
            buffer = ParametersBufferReader(self.__interop.CreateBuffer(actual_filters_ptr, buffer_config_ptr))
        else:
            buffer = ParametersBufferReader(self.__interop.CreateBuffer2(actual_filters_ptr))

        if actual_filters_ptr is not None:
            InteropUtils.free_hptr(actual_filters_ptr)

        self.__buffers.append(buffer)
        return buffer

    def get_net_pointer(self) -> ctypes.c_void_p:
        return self.__interop._get_interop_ptr()
