# automatically generated by the FlatBuffers compiler, do not modify

# namespace: reflection

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Enum(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Enum()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsEnum(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def EnumBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x42\x46\x42\x53", size_prefixed=size_prefixed)

    # Enum
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Enum
    def Name(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Enum
    def Values(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from reflection.EnumVal import EnumVal
            obj = EnumVal()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Enum
    def ValuesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Enum
    def ValuesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # Enum
    def IsUnion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Enum
    def UnderlyingType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from reflection.Type import Type
            obj = Type()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Enum
    def Attributes(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from reflection.KeyValue import KeyValue
            obj = KeyValue()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Enum
    def AttributesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Enum
    def AttributesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

    # Enum
    def Documentation(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # Enum
    def DocumentationLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Enum
    def DocumentationIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        return o == 0

def EnumStart(builder): builder.StartObject(6)
def Start(builder):
    return EnumStart(builder)
def EnumAddName(builder, name): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)
def AddName(builder, name):
    return EnumAddName(builder, name)
def EnumAddValues(builder, values): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(values), 0)
def AddValues(builder, values):
    return EnumAddValues(builder, values)
def EnumStartValuesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartValuesVector(builder, numElems):
    return EnumStartValuesVector(builder, numElems)
def EnumAddIsUnion(builder, isUnion): builder.PrependBoolSlot(2, isUnion, 0)
def AddIsUnion(builder, isUnion):
    return EnumAddIsUnion(builder, isUnion)
def EnumAddUnderlyingType(builder, underlyingType): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(underlyingType), 0)
def AddUnderlyingType(builder, underlyingType):
    return EnumAddUnderlyingType(builder, underlyingType)
def EnumAddAttributes(builder, attributes): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(attributes), 0)
def AddAttributes(builder, attributes):
    return EnumAddAttributes(builder, attributes)
def EnumStartAttributesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartAttributesVector(builder, numElems):
    return EnumStartAttributesVector(builder, numElems)
def EnumAddDocumentation(builder, documentation): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(documentation), 0)
def AddDocumentation(builder, documentation):
    return EnumAddDocumentation(builder, documentation)
def EnumStartDocumentationVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartDocumentationVector(builder, numElems):
    return EnumStartDocumentationVector(builder, numElems)
def EnumEnd(builder): return builder.EndObject()
def End(builder):
    return EnumEnd(builder)