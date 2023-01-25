from typing import Callable

from .eventhook import EventHook
from .native.Python.InteropHelpers.InteropUtils import InteropUtils
from .streamwriter import StreamWriter
import ctypes

from .native.Python.QuixSdkStreaming.OutputTopic import OutputTopic as oti
from .helpers.nativedecorator import nativedecorator


@nativedecorator
class OutputTopic(object):
    """
        Interface to operate with the streaming platform for reading or writing
    """

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
            Initializes a new instance of OutputTopic.
            NOTE: Do not initialize this class manually, use StreamingClient.create_output to create it

            Parameters:

            net_object (.net object): The .net object representing a StreamingClient
        """

        self.__cfuncrefs = []  # exists to hold onto the references created by the interop layer to avoid GC'ing them
        self.__interop = oti(net_pointer)

        def __on_disposed_read_net_handler(sender):
            self.on_disposed.fire(self)
            InteropUtils.free_hptr(sender)

        def __on_disposed_first_sub():
            ref = self.__interop.add_OnDisposed(__on_disposed_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_disposed_last_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnDisposed(__on_disposed_read_net_handler)

        self.on_disposed = EventHook(__on_disposed_first_sub, __on_disposed_last_unsub, name="OutputTopic.on_disposed")
        """
        Raised when the resource finished disposing       
         Parameters:
            topic (OutputTopic): The OutputTopic which raises the event
        """

    def __finalizerfunc(self):
        self.__cfuncrefs = None

    def create_stream(self, stream_id: str = None) -> StreamWriter:
        """
           Create new stream and returns the related stream writer to operate it.

           Parameters:

           stream_id (string): Optional, provide if you wish to overwrite the generated stream id. Useful if you wish
           to always stream a certain source into the same stream
       """
        if stream_id is None:
            return StreamWriter(self.__interop.CreateStream())
        return StreamWriter(self.__interop.CreateStream2(stream_id))

    def get_stream(self, stream_id: str) -> StreamWriter:
        """
           Retrieves a stream that was previously created by this instance, if the stream is not closed.

           Parameters:

           stream_id (string): The id of the stream
       """
        if stream_id is None:
            return None
        result_hptr = self.__interop.GetStream(stream_id)
        if result_hptr is None:
            return None
        # TODO retrieving same stream constantly might result in weird behaviour here
        return StreamWriter(result_hptr)

    def get_or_create_stream(self, stream_id: str, on_stream_created: Callable[[StreamWriter], None] = None) -> StreamWriter:
        """
           Retrieves a stream that was previously created by this instance, if the stream is not closed, otherwise creates a new stream.

           Parameters:

           stream_id (string): The Id of the stream you want to get or create
           on_stream_created (Callable[[StreamWriter], None]): A void callback taking StreamWriter
       """

        if stream_id is None:
            return None

        callback = None
        if on_stream_created is not None:
            def on_create_callback(streamwriter_hptr: ctypes.c_void_p):
                if type(streamwriter_hptr) is not ctypes.c_void_p:
                    streamwriter_hptr = ctypes.c_void_p(streamwriter_hptr)
                wrapped = StreamWriter(streamwriter_hptr)
                on_stream_created(wrapped)
            callback = on_create_callback

        return StreamWriter(self.__interop.GetOrCreateStream(stream_id, callback)[0])

