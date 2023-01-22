# automatically generated by the FlatBuffers compiler, do not modify

# namespace: arealm

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# WAMP permission (authorization of performing a WAMP action on a WAMP URI pattern).
class Permission(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 9

    # Permission
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # URI or URI pattern to match for the permission to apply.
    # URI check level.
    # Permission
    def UriCheckLevel(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # URI matching mode.
    # Permission
    def Match(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(1))
    # Allow/disallow calling procedures on a match.
    # Permission
    def AllowCall(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(2))
    # Allow/disallow registering procedures on a match.
    # Permission
    def AllowRegister(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(3))
    # Allow/disallow publishing events on a match.
    # Permission
    def AllowPublish(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Allow/disallow subscribing topics on a match.
    # Permission
    def AllowSubscribe(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(5))
    # Disclose the caller on a match (of a procedure) when called.
    # Permission
    def DiscloseCaller(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(6))
    # Disclose the publisher on a match (of a topic) when published to.
    # Permission
    def DisclosePublisher(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(7))
    # Cache the permission on a match in the router worker.
    # Permission
    def Cache(self): return self._tab.Get(flatbuffers.number_types.BoolFlags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))

def CreatePermission(builder, uriCheckLevel, match, allowCall, allowRegister, allowPublish, allowSubscribe, discloseCaller, disclosePublisher, cache):
    builder.Prep(1, 9)
    builder.PrependBool(cache)
    builder.PrependBool(disclosePublisher)
    builder.PrependBool(discloseCaller)
    builder.PrependBool(allowSubscribe)
    builder.PrependBool(allowPublish)
    builder.PrependBool(allowRegister)
    builder.PrependBool(allowCall)
    builder.PrependInt8(match)
    builder.PrependInt8(uriCheckLevel)
    return builder.Offset()
