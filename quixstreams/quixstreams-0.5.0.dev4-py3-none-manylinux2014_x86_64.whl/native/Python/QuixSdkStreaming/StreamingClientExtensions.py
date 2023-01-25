# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .Models.CommitMode import CommitMode
from ..QuixSdkProcess.Kafka.AutoOffsetReset import AutoOffsetReset
from .IInputTopic import IInputTopic
from ..InteropHelpers.InteropUtils import InteropUtils


class StreamingClientExtensions(object):
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamingclientextensions_openinputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, ctypes.c_int, ctypes.c_int]
    @staticmethod
    def OpenInputTopic(client: c_void_p, topic: str, consumerGroup: str = None, commitMode: CommitMode = CommitMode.Automatic, autoOffset: AutoOffsetReset = AutoOffsetReset.Earliest) -> c_void_p:
        """
        Parameters
        ----------
        
        client: c_void_p
            GC Handle Pointer to .Net type KafkaStreamingClient
        
        topic: str
            Underlying .Net type is string
        
        consumerGroup: str
            (Optional) Underlying .Net type is string. Defaults to Default
        
        commitMode: CommitMode
            (Optional) Underlying .Net type is CommitMode. Defaults to Automatic
        
        autoOffset: AutoOffsetReset
            (Optional) Underlying .Net type is AutoOffsetReset. Defaults to Earliest
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IInputTopic
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        
        result = InteropUtils.invoke("streamingclientextensions_openinputtopic", client, topic_ptr, consumerGroup_ptr, commitMode.value, autoOffset.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
