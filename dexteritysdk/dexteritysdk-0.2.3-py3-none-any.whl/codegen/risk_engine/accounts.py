# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.risk_engine.types.correlation_matrix import CorrelationMatrix
from dexteritysdk.codegen.risk_engine.types.covariance_metadata import CovarianceMetadata
from dexteritysdk.codegen.risk_engine.types.mark_prices_array import MarkPricesArray
from dexteritysdk.codegen.risk_engine.types.variance_cache import VarianceCache
from dexteritysdk.solmate.anchor import AccountDiscriminant
from podite import (
    Enum,
    U64,
    pod,
)

# LOCK-END


# LOCK-BEGIN[accounts]: DON'T MODIFY
@pod
class Accounts(Enum[U64]):
    CORRELATION_MATRIX = AccountDiscriminant(field=CorrelationMatrix)
    COVARIANCE_METADATA = AccountDiscriminant(field=CovarianceMetadata)
    MARK_PRICES_ARRAY = AccountDiscriminant(field=MarkPricesArray)
    VARIANCE_CACHE = AccountDiscriminant(field=VarianceCache)
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
