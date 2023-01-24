# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.risk_engine.types.risk_account_tag import RiskAccountTag
from dexteritysdk.solmate.dtypes import Usize
from podite import (
    FixedLenArray,
    I8,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(CorrelationMatrix)]: DON'T MODIFY
@pod
class CorrelationMatrix:
    tag: RiskAccountTag
    num_active_products: Usize
    correlations: FixedLenArray[I8, 8256]
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
