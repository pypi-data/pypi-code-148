# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.instruments.types.oracle_type import OracleType
from dexteritysdk.codegen.risk_engine.types.mark_price import MarkPrice
from podite import (
    FixedLenArray,
    U64,
    U8,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(MarkPricesArray)]: DON'T MODIFY
@pod
class MarkPricesArray:
    bump: U8
    padding0: FixedLenArray[U8, 7]
    update_slot: U64
    is_hardcoded_oracle: bool
    hardcoded_oracle: PublicKey
    padding1: FixedLenArray[U8, 7]
    hardcoded_oracle_type: OracleType
    padding2: FixedLenArray[U8, 7]
    array: FixedLenArray[MarkPrice, 64]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
