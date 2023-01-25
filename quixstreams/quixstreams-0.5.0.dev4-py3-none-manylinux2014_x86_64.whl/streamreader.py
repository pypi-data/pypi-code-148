from .eventhook import EventHook

from .models.streampackage import StreamPackage
from .models.streamreader.streampropertiesreader import StreamPropertiesReader
from .models.streamreader.streamparametersreader import StreamParametersReader
from .models.streamreader.streameventsreader import StreamEventsReader

from .models.streamendtype import StreamEndType
from .native.Python.InteropHelpers.InteropUtils import InteropUtils
from .native.Python.QuixSdkStreaming.IStreamReader import IStreamReader as sri
from .helpers.enumconverter import EnumConverter as ec
import ctypes
from .helpers.nativedecorator import nativedecorator


@nativedecorator
class StreamReader(object):
    """
        Handles reading stream from a topic
    """

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
        Initializes a new instance of StreamReader.
        NOTE: Do not initialize this class manually, use StreamingClient.on_stream_received to read streams
        :param net_pointer: Pointer to an instance of a .net StreamReader
        """
        self.__cfuncrefs = []  # exists to hold onto the references created by the interop layer to avoid GC'ing them
        self.__interop = sri(net_pointer)
        self.__streamParametersReader = None  # Holding reference to avoid GC
        self.__streamEventsReader = None  # Holding reference to avoid GC
        self.__streamPropertiesReader = None  # Holding reference to avoid GC

        def __on_stream_closed_read_net_handler(sender, end_type):
            converted = ec.enum_to_another(end_type, StreamEndType)
            self.on_stream_closed.fire(converted)
            self.dispose()
            InteropUtils.free_hptr(sender)  # another pointer is assigned to the same object as current, we don't need it

        def __on_stream_closed_first_sub():
            ref = self.__interop.add_OnStreamClosed(__on_stream_closed_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_stream_closed_last_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnStreamClosed(__on_stream_closed_read_net_handler)

        self.on_stream_closed = EventHook(__on_stream_closed_first_sub, __on_stream_closed_last_unsub, name="StreamReader.on_stream_closed")
        """Raised when stream close is read.       
         Parameters:
            sender (StreamReader): The StreamReader to which the event belongs to.            
            end_type (StreamEndType): The StreamEndType value read from the message.
        """

        def __on_package_received_net_handler(sender, package):
            self.on_package_received.fire(self, StreamPackage(package))
            InteropUtils.free_hptr(sender)   # another pointer is assigned to the same object as current, we don't need it

        def __on_first_sub_on_package_received():
            # TODO
            raise Exception("StreamReader.on_package_received is not yet fully implemented")
            ref = self.__interop.add_OnPackageReceived(__on_package_received_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_unsub_on_package_received():
            # TODO do unsign with previous handler
            self.__interop.remove_OnPackageReceived(__on_package_received_net_handler)

        self.on_package_received = EventHook(__on_first_sub_on_package_received, __on_last_unsub_on_package_received, name="StreamReader.on_package_received")
        """Raised when stream package has been received.       
         Parameters:
            sender (StreamReader): The StreamReader to which the event belongs to.            
            package (StreamPackage): The Package received.
        """

        self.__streamId = None

    def __finalizerfunc(self):
        if self.__streamParametersReader is not None:
            self.__streamParametersReader.dispose()
        if self.__streamEventsReader is not None:
            self.__streamEventsReader.dispose()
        if self.__streamPropertiesReader is not None:
            self.__streamPropertiesReader.dispose()
        self.__cfuncrefs = None

    @property
    def stream_id(self) -> str:
        """Get the id of the stream being read"""

        if self.__streamId is None:
            self.__streamId = self.__interop.get_StreamId()
        return self.__streamId

    @property
    def properties(self) -> StreamPropertiesReader:
        """ Gets the reader for accessing the properties and metadata of the stream """
        if self.__streamPropertiesReader is None:
            self.__streamPropertiesReader = StreamPropertiesReader(self.__interop.get_Properties())
        return self.__streamPropertiesReader

    @property
    def events(self) -> StreamEventsReader:
        """
        Gets the reader for accessing event related information of the stream such as definitions and event values
        """
        if self.__streamEventsReader is None:
            self.__streamEventsReader = StreamEventsReader(self.__interop.get_Events())
        return self.__streamEventsReader

    @property
    def parameters(self) -> StreamParametersReader:
        """
        Gets the reader for accessing parameter related information of the stream such as definitions and parameter values
        """
        if self.__streamParametersReader is None:
            self.__streamParametersReader = StreamParametersReader(self.__interop.get_Parameters())
        return self.__streamParametersReader

    def get_net_pointer(self) -> ctypes.c_void_p:
        return self.__interop._get_interop_ptr()
