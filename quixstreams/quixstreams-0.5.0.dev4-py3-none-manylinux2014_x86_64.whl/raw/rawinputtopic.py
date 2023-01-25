from ..eventhook import EventHook

from .rawmessage import RawMessage

from ..native.Python.QuixSdkStreaming.Raw.RawInputTopic import RawInputTopic as riti

import ctypes
from ..helpers.nativedecorator import nativedecorator


@nativedecorator
class RawInputTopic(object):

    def __init__(self, net_pointer: ctypes.c_void_p):
        """
        Initializes a new instance of StreamReader.
        NOTE: Do not initialize this class manually, use StreamingClient.on_stream_received to read streams

        :param net_pointer: Pointer to an instance of a .net RawInputTopic
        """

        if net_pointer is None:
            raise Exception("RawInputTopic is none")

        self.__interop = riti(net_pointer)
        self.__cfuncrefs = []  # exists to hold onto the references created by the interop layer to avoid GC'ing them


        def __on_message_read_handler(arg_hptr):
            # the type passed in will be an int, but RawMessage only takes pointer or forms of byte[]
            raw_message = RawMessage(ctypes.c_void_p(arg_hptr))
            self.on_message_read.fire(raw_message)

        def __on_first_message__sub():
            ref = self.__interop.add_OnMessageRead(__on_message_read_handler)
            self.__cfuncrefs.append(ref)

        def __on_last_message_unsub():
            # TODO fix unsub
            self.__interop.remove_OnMessageRead(__on_message_read_handler)

        self.on_message_read = EventHook(__on_first_message__sub, __on_last_message_unsub, name="RawInputTopic.on_message_read")

        def __on_error_occured_handler(sender_hptr, exception_hptr):
            # TODO
            raise Exception("NOT IMPLEMENTED")
            self.on_error_occurred.fire()

        def __on_error_first_sub():
            ref = self.__interop.add_OnErrorOccurred(__on_error_occured_handler)
            self.__cfuncrefs.append(ref)

        def __on_error_last_unsub():
            # TODO fix unsub
            self.__interop.remove_OnMessageRead(__on_error_occured_handler)

        self.on_error_occurred = EventHook(__on_error_first_sub, __on_error_last_unsub, name="RawInputTopic.on_error_occured")

    def __finalizerfunc(self):
        self.__cfuncrefs = None

    def start_reading(self):
        """
        Starts reading from the stream
        """
        self.__interop.StartReading()
