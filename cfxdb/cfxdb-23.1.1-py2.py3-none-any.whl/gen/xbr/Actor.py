# automatically generated by the FlatBuffers compiler, do not modify

# namespace: xbr

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# XBR Market Actors.
class Actor(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Actor()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsActor(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Actor
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Ethereum address of the member.
    # Actor
    def Actor(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Actor
    def ActorAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Actor
    def ActorLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Actor
    def ActorIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # Type of the market actor.
    # Actor
    def ActorType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # ID of the market this actor is associated with.
    # Actor
    def Market(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Actor
    def MarketAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Actor
    def MarketLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Actor
    def MarketIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

    # Database transaction time (epoch time in ns) of insert or last update.
    # Actor
    def Timestamp(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Block number (on the blockchain) when the actor (originally) joined the market.
    # Actor
    def Joined(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Actor
    def JoinedAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Actor
    def JoinedLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Actor
    def JoinedIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

    # Security (XBR tokens) deposited by the actor in the market.
    # Actor
    def Security(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Actor
    def SecurityAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Actor
    def SecurityLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Actor
    def SecurityIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        return o == 0

    # The XBR market metadata published by the market owner. IPFS Multihash pointing to a RDF/Turtle file with market metadata.
    # Actor
    def Meta(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Transaction hash of the transaction this change was committed to the blockchain under.
    # Actor
    def Tid(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Actor
    def TidAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Actor
    def TidLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Actor
    def TidIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        return o == 0

    # When signed off-chain and submitted via ``XBRNetwork.registerMemberFor``.
    # Actor
    def Signature(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Actor
    def SignatureAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Actor
    def SignatureLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Actor
    def SignatureIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        return o == 0

def ActorStart(builder): builder.StartObject(9)
def Start(builder):
    return ActorStart(builder)
def ActorAddActor(builder, actor): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(actor), 0)
def AddActor(builder, actor):
    return ActorAddActor(builder, actor)
def ActorStartActorVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartActorVector(builder, numElems):
    return ActorStartActorVector(builder, numElems)
def ActorAddActorType(builder, actorType): builder.PrependUint8Slot(1, actorType, 0)
def AddActorType(builder, actorType):
    return ActorAddActorType(builder, actorType)
def ActorAddMarket(builder, market): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(market), 0)
def AddMarket(builder, market):
    return ActorAddMarket(builder, market)
def ActorStartMarketVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartMarketVector(builder, numElems):
    return ActorStartMarketVector(builder, numElems)
def ActorAddTimestamp(builder, timestamp): builder.PrependUint64Slot(3, timestamp, 0)
def AddTimestamp(builder, timestamp):
    return ActorAddTimestamp(builder, timestamp)
def ActorAddJoined(builder, joined): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(joined), 0)
def AddJoined(builder, joined):
    return ActorAddJoined(builder, joined)
def ActorStartJoinedVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartJoinedVector(builder, numElems):
    return ActorStartJoinedVector(builder, numElems)
def ActorAddSecurity(builder, security): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(security), 0)
def AddSecurity(builder, security):
    return ActorAddSecurity(builder, security)
def ActorStartSecurityVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartSecurityVector(builder, numElems):
    return ActorStartSecurityVector(builder, numElems)
def ActorAddMeta(builder, meta): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(meta), 0)
def AddMeta(builder, meta):
    return ActorAddMeta(builder, meta)
def ActorAddTid(builder, tid): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(tid), 0)
def AddTid(builder, tid):
    return ActorAddTid(builder, tid)
def ActorStartTidVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartTidVector(builder, numElems):
    return ActorStartTidVector(builder, numElems)
def ActorAddSignature(builder, signature): builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(signature), 0)
def AddSignature(builder, signature):
    return ActorAddSignature(builder, signature)
def ActorStartSignatureVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartSignatureVector(builder, numElems):
    return ActorStartSignatureVector(builder, numElems)
def ActorEnd(builder): return builder.EndObject()
def End(builder):
    return ActorEnd(builder)