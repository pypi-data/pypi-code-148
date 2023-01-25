from typing import Union, Dict

from ..native.Python.QuixSdkStreaming.Raw.RawMessage import RawMessage as rmi
from ..native.Python.InteropHelpers.ExternalTypes.System.Array import Array as ai
from ..models.netdict import NetDict
import ctypes
from ..helpers.nativedecorator import nativedecorator


@nativedecorator
class RawMessage(object):
    """
        Class to hold the raw value being read from the message broker
    """

    def __init__(self, data: Union[ctypes.c_void_p, bytes, bytearray]):
        if isinstance(data, ctypes.c_void_p):
            self.__interop = rmi(data)
        elif isinstance(data, (bytes, bytearray)):
            # TODO
            self.__interop = rmi(rmi.Constructor2(data))
        else:
            raise Exception("Bad data type '" + type(data) + "' for the message. Must be ctypes_c.void_p, bytes or bytearray.")

        self.__metadata = None
        self.__value = None
    

    """
    Get associated .net object pointer
    """
    def get_net_pointer(self):
        return self.__interop._get_interop_ptr()

    """
    Get the optional key of the message. Depending on broker and message it is not guaranteed
    """
    @property
    def key(self) -> str:
        """Get the optional key of the message. Depending on broker and message it is not guaranteed """
        return self.__interop.get_Key()

    """
    Set the message key
    """
    @key.setter
    def key(self, value: str):
        """Set the message key"""
        self.__interop.set_Key(value)


    """
    Get message value (bytes content of message)
    """
    @property
    def value(self):
        """Get message value (bytes content of message)"""
        if self.__value is None:
            val_hptr = self.__interop.get_Value()
            self.__value = ai.ReadBytes(val_hptr)
        return self.__value

    @value.setter
    def value(self, value: Union[bytearray, bytes]):
        """Set message value (bytes content of message)"""
        self.__value = None  # in case it is read back, will be set again
        # todo
        self.__interop.set_Value(value)

    """
    Get wrapped message metadata

    (returns Dict[str, str])
    """
    @property
    def metadata(self) -> Dict[str, str]:
        """Get the default Epoch used for Parameters and Events"""
        if self.__metadata is None:
            self.__metadata = NetDict.constructor_for_string_string(self.__interop.get_Metadata())
        return self.__metadata

