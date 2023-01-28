import base62
from reedsolo import RSCodec
from speck import SpeckCipher


key_96bit = 0x9E4DC9158C2D33AAD4A9BEE3C3F2F134DBAD

speck = SpeckCipher(key_96bit, key_size=96, block_size=48)
reed_solomon_codec = RSCodec(10)


def encode(value: int, ecc: bool = True) -> str:
    ciphertext = speck.encrypt(value)
    cipherbytes = ciphertext.to_bytes(6, "big")
    if ecc:
        cipherbytes = bytes(reed_solomon_codec.encode(cipherbytes))
    return base62.encodebytes(cipherbytes)


def decode(encoded: str, ecc: bool = True) -> int:
    cipherbytes = base62.decodebytes(encoded)
    if ecc:
        cipherbytes, *_ = reed_solomon_codec.decode(bytearray(cipherbytes))
    ciphertext = int.from_bytes(cipherbytes, "big")
    return speck.decrypt(ciphertext)


class OID:
    def __init__(self, value):
        if isinstance(value, OID):
            value = value._value
        if isinstance(value, str):
            value = decode(value)

        self._value = value

    def decode(self) -> int:
        return decode(self._value)

    def encode(self) -> str:
        return encode(self._value)


# model_id = 99999999999

# # 235963431219045
# ciphertext = speck.encrypt(model_id)

# #  b'\xd6\x9b\x84\x7foe'
# cipherbytes = ciphertext.to_bytes(6, "big")

# # # '150GeEMpZ'
# # encoded = base62.encodebytes(cipherbytes)

# # bytearray(b'\xd6\x9b\x84\x7foe\xefV\xbe\x02\x9e\x1b\x9cJ[\xb1')
# ecc_encoded = rsc.encode(cipherbytes)

# # '6WxQdmGgs2xKd1OHtlYdeb'
# base62_encoded = base62.encodebytes(bytes(ecc_encoded))


# # lets decode and decrypt back to original id

# # 1. With ECC

# # b'\xd6\x9b\x84\x7foe\xefV\xbe\x02\x9e\x1b\x9cJ[\xb1'
# decoded_ecc = base62.decodebytes(base62_encoded)

# # bytearray(b'\xd6\x9b\x84\x7foe')
# cipherbytes, *_ = rsc.decode(bytearray(decoded_ecc))

# # 235963431219045
# ciphertext = int.from_bytes(cipherbytes, "big")

# # 99999999999
# recovered_model_id = speck.decrypt(ciphertext)
