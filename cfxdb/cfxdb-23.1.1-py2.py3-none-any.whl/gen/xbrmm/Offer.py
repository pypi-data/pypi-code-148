# automatically generated by the FlatBuffers compiler, do not modify

# namespace: xbrmm

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# Data encryption key off-chain offerings, submitted by seller/provider delegates in the market.
class Offer(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Offer()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsOffer(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Offer
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Offer transaction time (epoch time in ns)
    # Offer
    def Timestamp(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # ID of the data encryption key offer.
    # Offer
    def Offer(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Offer
    def OfferAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Offer
    def OfferLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def OfferIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # Address of the XBR provider offering the data encryption key.
    # Offer
    def Seller(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Offer
    def SellerAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Offer
    def SellerLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def SellerIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

    # WAMP session ID of the caller that originally placed this offer.
    # Offer
    def SellerSessionId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # WAMP session authid of the caller that originally placed this offer.
    # Offer
    def SellerAuthid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # ID of the data encryption key offered.
    # Offer
    def Key(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Offer
    def KeyAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Offer
    def KeyLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def KeyIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        return o == 0

    # ID of the API the encrypted data (this key is for) is provided under.
    # Offer
    def Api(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Offer
    def ApiAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Offer
    def ApiLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def ApiIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        return o == 0

    # URI under which the data encrypted with the key offered is provided under.
    # Offer
    def Uri(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Timestamp from which the offer is valid (epoch time in ns).
    # Offer
    def ValidFrom(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Seller delegate signature for the offer. The signature covers all information of the original offer placement request and requestor.
    # Offer
    def Signature(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Offer
    def SignatureAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Offer
    def SignatureLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def SignatureIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        return o == 0

    # Price of data encryption key in ERC20 tokens of the market coin type.
    # Offer
    def Price(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Offer
    def PriceAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Offer
    def PriceLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def PriceIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        return o == 0

    # Keys for optional user defined categories the specific data that is provided falls under.
    # Offer
    def CategoriesKey(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(26))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # Offer
    def CategoriesKeyLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(26))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def CategoriesKeyIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(26))
        return o == 0

    # Values for optional user defined categories the specific data that is provided falls under.
    # Offer
    def CategoriesValue(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # Offer
    def CategoriesValueLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Offer
    def CategoriesValueIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(28))
        return o == 0

    # Optional data at which this offer expires (epoch time in ns).
    # Offer
    def Expires(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(30))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Optional maximum number of times this data encryption key is to be sold or 0 for unlimited.
    # Offer
    def Copies(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(32))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # Remaining number of copies to be sold (if "copies" is set >0, otherwise 0).
    # Offer
    def Remaining(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(34))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

def OfferStart(builder): builder.StartObject(16)
def Start(builder):
    return OfferStart(builder)
def OfferAddTimestamp(builder, timestamp): builder.PrependUint64Slot(0, timestamp, 0)
def AddTimestamp(builder, timestamp):
    return OfferAddTimestamp(builder, timestamp)
def OfferAddOffer(builder, offer): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(offer), 0)
def AddOffer(builder, offer):
    return OfferAddOffer(builder, offer)
def OfferStartOfferVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartOfferVector(builder, numElems):
    return OfferStartOfferVector(builder, numElems)
def OfferAddSeller(builder, seller): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(seller), 0)
def AddSeller(builder, seller):
    return OfferAddSeller(builder, seller)
def OfferStartSellerVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartSellerVector(builder, numElems):
    return OfferStartSellerVector(builder, numElems)
def OfferAddSellerSessionId(builder, sellerSessionId): builder.PrependUint64Slot(3, sellerSessionId, 0)
def AddSellerSessionId(builder, sellerSessionId):
    return OfferAddSellerSessionId(builder, sellerSessionId)
def OfferAddSellerAuthid(builder, sellerAuthid): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(sellerAuthid), 0)
def AddSellerAuthid(builder, sellerAuthid):
    return OfferAddSellerAuthid(builder, sellerAuthid)
def OfferAddKey(builder, key): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(key), 0)
def AddKey(builder, key):
    return OfferAddKey(builder, key)
def OfferStartKeyVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartKeyVector(builder, numElems):
    return OfferStartKeyVector(builder, numElems)
def OfferAddApi(builder, api): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(api), 0)
def AddApi(builder, api):
    return OfferAddApi(builder, api)
def OfferStartApiVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartApiVector(builder, numElems):
    return OfferStartApiVector(builder, numElems)
def OfferAddUri(builder, uri): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(uri), 0)
def AddUri(builder, uri):
    return OfferAddUri(builder, uri)
def OfferAddValidFrom(builder, validFrom): builder.PrependUint64Slot(8, validFrom, 0)
def AddValidFrom(builder, validFrom):
    return OfferAddValidFrom(builder, validFrom)
def OfferAddSignature(builder, signature): builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(signature), 0)
def AddSignature(builder, signature):
    return OfferAddSignature(builder, signature)
def OfferStartSignatureVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartSignatureVector(builder, numElems):
    return OfferStartSignatureVector(builder, numElems)
def OfferAddPrice(builder, price): builder.PrependUOffsetTRelativeSlot(10, flatbuffers.number_types.UOffsetTFlags.py_type(price), 0)
def AddPrice(builder, price):
    return OfferAddPrice(builder, price)
def OfferStartPriceVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def StartPriceVector(builder, numElems):
    return OfferStartPriceVector(builder, numElems)
def OfferAddCategoriesKey(builder, categoriesKey): builder.PrependUOffsetTRelativeSlot(11, flatbuffers.number_types.UOffsetTFlags.py_type(categoriesKey), 0)
def AddCategoriesKey(builder, categoriesKey):
    return OfferAddCategoriesKey(builder, categoriesKey)
def OfferStartCategoriesKeyVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartCategoriesKeyVector(builder, numElems):
    return OfferStartCategoriesKeyVector(builder, numElems)
def OfferAddCategoriesValue(builder, categoriesValue): builder.PrependUOffsetTRelativeSlot(12, flatbuffers.number_types.UOffsetTFlags.py_type(categoriesValue), 0)
def AddCategoriesValue(builder, categoriesValue):
    return OfferAddCategoriesValue(builder, categoriesValue)
def OfferStartCategoriesValueVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def StartCategoriesValueVector(builder, numElems):
    return OfferStartCategoriesValueVector(builder, numElems)
def OfferAddExpires(builder, expires): builder.PrependUint64Slot(13, expires, 0)
def AddExpires(builder, expires):
    return OfferAddExpires(builder, expires)
def OfferAddCopies(builder, copies): builder.PrependUint32Slot(14, copies, 0)
def AddCopies(builder, copies):
    return OfferAddCopies(builder, copies)
def OfferAddRemaining(builder, remaining): builder.PrependUint32Slot(15, remaining, 0)
def AddRemaining(builder, remaining):
    return OfferAddRemaining(builder, remaining)
def OfferEnd(builder): return builder.EndObject()
def End(builder):
    return OfferEnd(builder)