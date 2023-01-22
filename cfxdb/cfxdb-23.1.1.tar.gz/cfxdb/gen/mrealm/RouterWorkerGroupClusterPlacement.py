# automatically generated by the FlatBuffers compiler, do not modify

# namespace: mrealm

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class RouterWorkerGroupClusterPlacement(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RouterWorkerGroupClusterPlacement()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsRouterWorkerGroupClusterPlacement(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # RouterWorkerGroupClusterPlacement
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # OID of this worker-to-cluster placement.
    # RouterWorkerGroupClusterPlacement
    def Oid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            from ..oid_t import oid_t
            obj = oid_t()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OID of (router) worker group this placement applies to.
    # RouterWorkerGroupClusterPlacement
    def WorkerGroupOid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from ..oid_t import oid_t
            obj = oid_t()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OID of cluster onto which the worker is placed.
    # RouterWorkerGroupClusterPlacement
    def ClusterOid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from ..oid_t import oid_t
            obj = oid_t()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # OID of the node onto which the worker is placed.
    # RouterWorkerGroupClusterPlacement
    def NodeOid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from ..oid_t import oid_t
            obj = oid_t()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Local worker name on the node onto which the worker is placed.
    # RouterWorkerGroupClusterPlacement
    def WorkerName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def RouterWorkerGroupClusterPlacementStart(builder): builder.StartObject(5)
def Start(builder):
    return RouterWorkerGroupClusterPlacementStart(builder)
def RouterWorkerGroupClusterPlacementAddOid(builder, oid): builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(oid), 0)
def AddOid(builder, oid):
    return RouterWorkerGroupClusterPlacementAddOid(builder, oid)
def RouterWorkerGroupClusterPlacementAddWorkerGroupOid(builder, workerGroupOid): builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(workerGroupOid), 0)
def AddWorkerGroupOid(builder, workerGroupOid):
    return RouterWorkerGroupClusterPlacementAddWorkerGroupOid(builder, workerGroupOid)
def RouterWorkerGroupClusterPlacementAddClusterOid(builder, clusterOid): builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(clusterOid), 0)
def AddClusterOid(builder, clusterOid):
    return RouterWorkerGroupClusterPlacementAddClusterOid(builder, clusterOid)
def RouterWorkerGroupClusterPlacementAddNodeOid(builder, nodeOid): builder.PrependStructSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(nodeOid), 0)
def AddNodeOid(builder, nodeOid):
    return RouterWorkerGroupClusterPlacementAddNodeOid(builder, nodeOid)
def RouterWorkerGroupClusterPlacementAddWorkerName(builder, workerName): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(workerName), 0)
def AddWorkerName(builder, workerName):
    return RouterWorkerGroupClusterPlacementAddWorkerName(builder, workerName)
def RouterWorkerGroupClusterPlacementEnd(builder): return builder.EndObject()
def End(builder):
    return RouterWorkerGroupClusterPlacementEnd(builder)