# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.risk_engine.types.fast_int import FastInt
from dexteritysdk.codegen.risk_engine.types.risk_account_tag import RiskAccountTag
from dexteritysdk.solmate.dtypes import Usize
from podite import (
    FixedLenArray,
    U64,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(VarianceCache)]: DON'T MODIFY
@pod
class VarianceCache:
    tag: RiskAccountTag
    update_slot: U64
    position_value: FastInt
    total_variance: FastInt
    open_order_variance: FastInt
    product_indexes: FixedLenArray[Usize, 32]
    positions: FixedLenArray[FastInt, 32]
    sigma_p: FixedLenArray[FastInt, 32]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
