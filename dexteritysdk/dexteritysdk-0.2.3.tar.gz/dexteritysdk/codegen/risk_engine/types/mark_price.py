# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.risk_engine.types.fast_int import FastInt
from podite import pod
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(MarkPrice)]: DON'T MODIFY
@pod
class MarkPrice:
    product_key: PublicKey
    mark_price: FastInt
    prev_oracle_minus_book_ewma: FastInt
    oracle_minus_book_ewma: FastInt
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
