from .eventhook import EventHook
from .native.Python.InteropHelpers.InteropUtils import InteropUtils
from .streamreader import StreamReader

import ctypes
from .native.Python.QuixSdkStreaming.InputTopic import InputTopic as iti
from .helpers.nativedecorator import nativedecorator


@nativedecorator
class InputTopic(object):
    """
        Interface to operate with the streaming platform for reading or writing
    """

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
            Initializes a new instance of StreamingClient.
            NOTE: Do not initialize this class manually, use StreamingClient.create_input to create it

            Parameters:

            net_pointer (.net pointer): The .net pointer to InputTopic instance
        """
        self.__cfuncrefs = []  # exists to hold onto the references created by the interop layer to avoid GC'ing them
        self.__active_streams = []  # To clean up when closing topic else could end up with references
        self.__interop = iti(net_pointer)


        def __on_stream_received_read_net_handler(sender, arg):
            stream = StreamReader(arg)
            self.__active_streams.append(stream)
            stream.on_stream_closed += lambda x: self.__active_streams.remove(stream)
            self.on_stream_received.fire(stream)
            InteropUtils.free_hptr(sender)  # another pointer is assigned to the same object as current, we don't need it

        def __on_stream_received_first_sub():
            ref = self.__interop.add_OnStreamReceived(__on_stream_received_read_net_handler)
            self.__cfuncrefs.append(ref)

        def _on_stream_received_last_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnStreamReceived(__on_stream_received_read_net_handler)

        self.on_stream_received = EventHook(__on_stream_received_first_sub, _on_stream_received_last_unsub, name="InputTopic.on_stream_received")
        """
        Raised when a new stream is received.       
         Parameters:
            reader (StreamReader): The StreamReader which raises new packages related to stream
        """

        def __on_streams_revoked_read_net_handler(sender, arg):
            # TODO
            # revoked_arg = list(map(lambda x: StreamReader(Quix.Sdk.Streaming.IStreamReader(x)), arg))
            # self.on_streams_revoked.fire(revoked_arg)
            InteropUtils.free_hptr(sender)  # another pointer is assigned to the same object as current, we don't need it

        def __on_streams_revoked_first_sub():
            ref = self.__interop.add_OnStreamsRevoked(__on_streams_revoked_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_streams_revoked_last_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnStreamsRevoked(__on_streams_revoked_read_net_handler)

        self.on_streams_revoked = EventHook(__on_streams_revoked_first_sub, __on_streams_revoked_last_unsub, name="InputTopic.on_streams_revoked")
        """
        Raised when the underlying source of data became unavailable for the streams affected by it       
         Parameters:
            readers (StreamReader[]): The StreamReaders revoked
        """

        def __on_revoking_read_net_handler(sender, arg):
            #TODO
            #self.on_revoking.fire()
            InteropUtils.free_hptr(sender)  # another pointer is assigned to the same object as current, we don't need it

        def __on_revoking_first_sub():
            ref = self.__interop.add_OnRevoking(__on_revoking_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_revoking_last_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnRevoking(__on_revoking_read_net_handler)

        self.on_revoking = EventHook(__on_revoking_first_sub, __on_revoking_last_unsub, name="InputTopic.on_revoking")
        """
        Raised when the underlying source of data will became unavailable, but depending on implementation commit might be possible at this point
        """

        def __on_committed_read_net_handler(sender, arg):
            # TODO
            #self.on_committed.fire()
            InteropUtils.free_hptr(sender)  # another pointer is assigned to the same object as current, we don't need it

        def __on_committed_first_sub():
            ref = self.__interop.add_OnCommitted(__on_committed_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_committed_last_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnCommitted(__on_committed_read_net_handler)

        self.on_committed = EventHook(__on_committed_first_sub, __on_committed_last_unsub, name="InputTopic.on_committed")
        """
        Raised when underlying source committed data read up to this point
        """

        def __on_committing_read_net_handler(sender, arg):
            # TODO
            #self.on_committing.fire()
            InteropUtils.free_hptr(sender)  # another pointer is assigned to the same object as current, we don't need it

        def __on_committing_first_sub():
            ref = self.__interop.add_OnCommitting(__on_committing_read_net_handler)
            self.__cfuncrefs.append(ref)

        def __on_committing_last_unsub():
            # TODO do unsign with previous handler
            self.__interop.remove_OnCommitting(__on_committing_read_net_handler)

        self.on_committing = EventHook(__on_committing_first_sub, __on_committing_last_unsub, name="InputTopic.on_committing")
        """
        Raised when underlying source is about to commit data read up to this point
        """

    def __finalizerfunc(self):
        self.__cfuncrefs = None

    def start_reading(self):
        """
           Starts reading streams
           Use 'on_stream_received' event to read incoming streams
        """
        self.__interop.StartReading()

    def commit(self):
        """
           Commit packages read up until now
        """
        self.__interop.Commit()

    def get_net_pointer(self) -> ctypes.c_void_p:
        return self.__interop._get_interop_ptr()
