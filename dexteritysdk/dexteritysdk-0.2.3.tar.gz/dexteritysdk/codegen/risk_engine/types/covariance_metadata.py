# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.risk_engine.types.fast_int import FastInt
from dexteritysdk.codegen.risk_engine.types.risk_account_tag import RiskAccountTag
from dexteritysdk.solmate.dtypes import Usize
from podite import (
    FixedLenArray,
    U64,
    pod,
)
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(CovarianceMetadata)]: DON'T MODIFY
@pod
class CovarianceMetadata:
    tag: RiskAccountTag
    update_slot: U64
    authority: PublicKey
    num_active_products: Usize
    product_keys: FixedLenArray[PublicKey, 128]
    standard_deviations: FixedLenArray[FastInt, 128]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
