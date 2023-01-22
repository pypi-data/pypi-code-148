# automatically generated by the FlatBuffers compiler, do not modify

# namespace: log

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# Logs of runs (from start to end) of a CFC instance.
class MasterRun(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MasterRun()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMasterRun(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # MasterRun
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # When the his run ended (Unix time in ns).
    # MasterRun
    def Ended(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # CFC run ID (this is unique over all start-stop cycles of CFC, and constant per run).
    # MasterRun
    def RunId(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # MasterRun
    def RunIdAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # MasterRun
    def RunIdLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MasterRun
    def RunIdIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # When the his run started (Unix time in ns).
    # MasterRun
    def Started(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Current master state.
    # MasterRun
    def State(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

def MasterRunStart(builder): builder.StartObject(4)
def Start(builder):
    return MasterRunStart(builder)
def MasterRunAddEnded(builder, ended): builder.PrependUint64Slot(0, ended, 0)
def AddEnded(builder, ended):
    return MasterRunAddEnded(builder, ended)
def MasterRunAddRunId(builder, runId): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(runId), 0)
def AddRunId(builder, runId):
    return MasterRunAddRunId(builder, runId)
def MasterRunStartRunIdVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartRunIdVector(builder, numElems):
    return MasterRunStartRunIdVector(builder, numElems)
def MasterRunAddStarted(builder, started): builder.PrependUint64Slot(2, started, 0)
def AddStarted(builder, started):
    return MasterRunAddStarted(builder, started)
def MasterRunAddState(builder, state): builder.PrependUint8Slot(3, state, 0)
def AddState(builder, state):
    return MasterRunAddState(builder, state)
def MasterRunEnd(builder): return builder.EndObject()
def End(builder):
    return MasterRunEnd(builder)