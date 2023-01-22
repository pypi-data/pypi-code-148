# automatically generated by the FlatBuffers compiler, do not modify

# namespace: log

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# Aggregate usage metering records for management realms. Primary key: (timestamp, mrealm_id).
class MasterNodeUsage(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MasterNodeUsage()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMasterNodeUsage(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # MasterNodeUsage
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Primary key: Timestamp (end of aggregate interval) recorded in UTC (Unix time in ns).
    # MasterNodeUsage
    def Timestamp(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Primary key: Management realm ID.
    # MasterNodeUsage
    def MrealmId(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # MasterNodeUsage
    def MrealmIdAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # MasterNodeUsage
    def MrealmIdLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MasterNodeUsage
    def MrealmIdIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # Timestamp (start of aggregate interval) recorded in UTC (Unix time in ns).
    # MasterNodeUsage
    def TimestampFrom(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Public key of the CrossbarFX master node that submitted the usage record.
    # MasterNodeUsage
    def Pubkey(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # MasterNodeUsage
    def PubkeyAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # MasterNodeUsage
    def PubkeyLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MasterNodeUsage
    def PubkeyIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        return o == 0

    # Client IPv4 address (4 bytes) or IPv6 (16 bytes) address of the CrossbarFX master node that submitted the usage record.
    # MasterNodeUsage
    def ClientIpAddress(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # MasterNodeUsage
    def ClientIpAddressAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # MasterNodeUsage
    def ClientIpAddressLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MasterNodeUsage
    def ClientIpAddressIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

    # Client IP version of the CrossbarFX master node that submitted the usage record.
    # MasterNodeUsage
    def ClientIpVersion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Client IP port of the CrossbarFX master node that submitted the usage record.
    # MasterNodeUsage
    def ClientIpPort(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint16Flags, o + self._tab.Pos)
        return 0

    # Sequence number as sent in the log record by the CF node (started at 0 for CF start and incremented by one on each heartbeat).
    # MasterNodeUsage
    def Seq(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Unix time in ns. This timestamp is from the original received event payload (from CF node clock).
    # MasterNodeUsage
    def Sent(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Unix time in ns. Set when this record was processed.
    # MasterNodeUsage
    def Processed(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Status of usage metering record.
    # MasterNodeUsage
    def Status(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Status message for current status.
    # MasterNodeUsage
    def StatusMessage(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(26))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Filled after this usage metering record was successfully submitted to the metering service.
    # MasterNodeUsage
    def MeteringId(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # MasterNodeUsage
    def MeteringIdAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # MasterNodeUsage
    def MeteringIdLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MasterNodeUsage
    def MeteringIdIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        return o == 0

    # Number of aggregated records from MworkerLogs
    # MasterNodeUsage
    def Count(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(30))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of aggregated and summed MworkerLogs.count records
    # MasterNodeUsage
    def Total(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(32))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Nodes by node type
    # MasterNodeUsage
    def Nodes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(34))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of node controllers metered.
    # MasterNodeUsage
    def Controllers(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(36))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of hostmonitor workers metered.
    # MasterNodeUsage
    def Hostmonitors(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(38))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of router workers metered.
    # MasterNodeUsage
    def Routers(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(40))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of container workers metered.
    # MasterNodeUsage
    def Containers(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(42))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of guest workers metered.
    # MasterNodeUsage
    def Guests(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(44))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of proxy workers metered.
    # MasterNodeUsage
    def Proxies(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(46))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of XBR market maker workers metered.
    # MasterNodeUsage
    def Marketmakers(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(48))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP sessions attached to router workers and metered.
    # MasterNodeUsage
    def Sessions(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(50))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP CALL messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsCall(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(52))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP YIELD messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsYield(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(54))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP INVOCATION messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsInvocation(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(56))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP RESULT messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsResult(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(58))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP ERROR messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsError(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(60))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP PUBLISH messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsPublish(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(62))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP PUBLISHED messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsPublished(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(64))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP EVENT messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsEvent(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(66))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP REGISTER messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsRegister(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(68))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP REGISTERED messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsRegistered(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(70))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP SUBSCRIBE messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsSubscribe(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(72))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Number of WAMP SUBSCRIBED messages processed by a router worker and metered.
    # MasterNodeUsage
    def MsgsSubscribed(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(74))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

def MasterNodeUsageStart(builder): builder.StartObject(36)
def Start(builder):
    return MasterNodeUsageStart(builder)
def MasterNodeUsageAddTimestamp(builder, timestamp): builder.PrependUint64Slot(0, timestamp, 0)
def AddTimestamp(builder, timestamp):
    return MasterNodeUsageAddTimestamp(builder, timestamp)
def MasterNodeUsageAddMrealmId(builder, mrealmId): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(mrealmId), 0)
def AddMrealmId(builder, mrealmId):
    return MasterNodeUsageAddMrealmId(builder, mrealmId)
def MasterNodeUsageStartMrealmIdVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartMrealmIdVector(builder, numElems):
    return MasterNodeUsageStartMrealmIdVector(builder, numElems)
def MasterNodeUsageAddTimestampFrom(builder, timestampFrom): builder.PrependUint64Slot(2, timestampFrom, 0)
def AddTimestampFrom(builder, timestampFrom):
    return MasterNodeUsageAddTimestampFrom(builder, timestampFrom)
def MasterNodeUsageAddPubkey(builder, pubkey): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(pubkey), 0)
def AddPubkey(builder, pubkey):
    return MasterNodeUsageAddPubkey(builder, pubkey)
def MasterNodeUsageStartPubkeyVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartPubkeyVector(builder, numElems):
    return MasterNodeUsageStartPubkeyVector(builder, numElems)
def MasterNodeUsageAddClientIpAddress(builder, clientIpAddress): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(clientIpAddress), 0)
def AddClientIpAddress(builder, clientIpAddress):
    return MasterNodeUsageAddClientIpAddress(builder, clientIpAddress)
def MasterNodeUsageStartClientIpAddressVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartClientIpAddressVector(builder, numElems):
    return MasterNodeUsageStartClientIpAddressVector(builder, numElems)
def MasterNodeUsageAddClientIpVersion(builder, clientIpVersion): builder.PrependUint8Slot(5, clientIpVersion, 0)
def AddClientIpVersion(builder, clientIpVersion):
    return MasterNodeUsageAddClientIpVersion(builder, clientIpVersion)
def MasterNodeUsageAddClientIpPort(builder, clientIpPort): builder.PrependUint16Slot(6, clientIpPort, 0)
def AddClientIpPort(builder, clientIpPort):
    return MasterNodeUsageAddClientIpPort(builder, clientIpPort)
def MasterNodeUsageAddSeq(builder, seq): builder.PrependUint64Slot(7, seq, 0)
def AddSeq(builder, seq):
    return MasterNodeUsageAddSeq(builder, seq)
def MasterNodeUsageAddSent(builder, sent): builder.PrependUint64Slot(8, sent, 0)
def AddSent(builder, sent):
    return MasterNodeUsageAddSent(builder, sent)
def MasterNodeUsageAddProcessed(builder, processed): builder.PrependUint64Slot(9, processed, 0)
def AddProcessed(builder, processed):
    return MasterNodeUsageAddProcessed(builder, processed)
def MasterNodeUsageAddStatus(builder, status): builder.PrependUint8Slot(10, status, 0)
def AddStatus(builder, status):
    return MasterNodeUsageAddStatus(builder, status)
def MasterNodeUsageAddStatusMessage(builder, statusMessage): builder.PrependUOffsetTRelativeSlot(11, flatbuffers.number_types.UOffsetTFlags.py_type(statusMessage), 0)
def AddStatusMessage(builder, statusMessage):
    return MasterNodeUsageAddStatusMessage(builder, statusMessage)
def MasterNodeUsageAddMeteringId(builder, meteringId): builder.PrependUOffsetTRelativeSlot(12, flatbuffers.number_types.UOffsetTFlags.py_type(meteringId), 0)
def AddMeteringId(builder, meteringId):
    return MasterNodeUsageAddMeteringId(builder, meteringId)
def MasterNodeUsageStartMeteringIdVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartMeteringIdVector(builder, numElems):
    return MasterNodeUsageStartMeteringIdVector(builder, numElems)
def MasterNodeUsageAddCount(builder, count): builder.PrependUint64Slot(13, count, 0)
def AddCount(builder, count):
    return MasterNodeUsageAddCount(builder, count)
def MasterNodeUsageAddTotal(builder, total): builder.PrependUint64Slot(14, total, 0)
def AddTotal(builder, total):
    return MasterNodeUsageAddTotal(builder, total)
def MasterNodeUsageAddNodes(builder, nodes): builder.PrependUint64Slot(15, nodes, 0)
def AddNodes(builder, nodes):
    return MasterNodeUsageAddNodes(builder, nodes)
def MasterNodeUsageAddControllers(builder, controllers): builder.PrependUint64Slot(16, controllers, 0)
def AddControllers(builder, controllers):
    return MasterNodeUsageAddControllers(builder, controllers)
def MasterNodeUsageAddHostmonitors(builder, hostmonitors): builder.PrependUint64Slot(17, hostmonitors, 0)
def AddHostmonitors(builder, hostmonitors):
    return MasterNodeUsageAddHostmonitors(builder, hostmonitors)
def MasterNodeUsageAddRouters(builder, routers): builder.PrependUint64Slot(18, routers, 0)
def AddRouters(builder, routers):
    return MasterNodeUsageAddRouters(builder, routers)
def MasterNodeUsageAddContainers(builder, containers): builder.PrependUint64Slot(19, containers, 0)
def AddContainers(builder, containers):
    return MasterNodeUsageAddContainers(builder, containers)
def MasterNodeUsageAddGuests(builder, guests): builder.PrependUint64Slot(20, guests, 0)
def AddGuests(builder, guests):
    return MasterNodeUsageAddGuests(builder, guests)
def MasterNodeUsageAddProxies(builder, proxies): builder.PrependUint64Slot(21, proxies, 0)
def AddProxies(builder, proxies):
    return MasterNodeUsageAddProxies(builder, proxies)
def MasterNodeUsageAddMarketmakers(builder, marketmakers): builder.PrependUint64Slot(22, marketmakers, 0)
def AddMarketmakers(builder, marketmakers):
    return MasterNodeUsageAddMarketmakers(builder, marketmakers)
def MasterNodeUsageAddSessions(builder, sessions): builder.PrependUint64Slot(23, sessions, 0)
def AddSessions(builder, sessions):
    return MasterNodeUsageAddSessions(builder, sessions)
def MasterNodeUsageAddMsgsCall(builder, msgsCall): builder.PrependUint64Slot(24, msgsCall, 0)
def AddMsgsCall(builder, msgsCall):
    return MasterNodeUsageAddMsgsCall(builder, msgsCall)
def MasterNodeUsageAddMsgsYield(builder, msgsYield): builder.PrependUint64Slot(25, msgsYield, 0)
def AddMsgsYield(builder, msgsYield):
    return MasterNodeUsageAddMsgsYield(builder, msgsYield)
def MasterNodeUsageAddMsgsInvocation(builder, msgsInvocation): builder.PrependUint64Slot(26, msgsInvocation, 0)
def AddMsgsInvocation(builder, msgsInvocation):
    return MasterNodeUsageAddMsgsInvocation(builder, msgsInvocation)
def MasterNodeUsageAddMsgsResult(builder, msgsResult): builder.PrependUint64Slot(27, msgsResult, 0)
def AddMsgsResult(builder, msgsResult):
    return MasterNodeUsageAddMsgsResult(builder, msgsResult)
def MasterNodeUsageAddMsgsError(builder, msgsError): builder.PrependUint64Slot(28, msgsError, 0)
def AddMsgsError(builder, msgsError):
    return MasterNodeUsageAddMsgsError(builder, msgsError)
def MasterNodeUsageAddMsgsPublish(builder, msgsPublish): builder.PrependUint64Slot(29, msgsPublish, 0)
def AddMsgsPublish(builder, msgsPublish):
    return MasterNodeUsageAddMsgsPublish(builder, msgsPublish)
def MasterNodeUsageAddMsgsPublished(builder, msgsPublished): builder.PrependUint64Slot(30, msgsPublished, 0)
def AddMsgsPublished(builder, msgsPublished):
    return MasterNodeUsageAddMsgsPublished(builder, msgsPublished)
def MasterNodeUsageAddMsgsEvent(builder, msgsEvent): builder.PrependUint64Slot(31, msgsEvent, 0)
def AddMsgsEvent(builder, msgsEvent):
    return MasterNodeUsageAddMsgsEvent(builder, msgsEvent)
def MasterNodeUsageAddMsgsRegister(builder, msgsRegister): builder.PrependUint64Slot(32, msgsRegister, 0)
def AddMsgsRegister(builder, msgsRegister):
    return MasterNodeUsageAddMsgsRegister(builder, msgsRegister)
def MasterNodeUsageAddMsgsRegistered(builder, msgsRegistered): builder.PrependUint64Slot(33, msgsRegistered, 0)
def AddMsgsRegistered(builder, msgsRegistered):
    return MasterNodeUsageAddMsgsRegistered(builder, msgsRegistered)
def MasterNodeUsageAddMsgsSubscribe(builder, msgsSubscribe): builder.PrependUint64Slot(34, msgsSubscribe, 0)
def AddMsgsSubscribe(builder, msgsSubscribe):
    return MasterNodeUsageAddMsgsSubscribe(builder, msgsSubscribe)
def MasterNodeUsageAddMsgsSubscribed(builder, msgsSubscribed): builder.PrependUint64Slot(35, msgsSubscribed, 0)
def AddMsgsSubscribed(builder, msgsSubscribed):
    return MasterNodeUsageAddMsgsSubscribed(builder, msgsSubscribed)
def MasterNodeUsageEnd(builder): return builder.EndObject()
def End(builder):
    return MasterNodeUsageEnd(builder)