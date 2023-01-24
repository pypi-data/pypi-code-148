# LOCK-BEGIN[imports]: DON'T MODIFY
from podite import (
    AutoTagType,
    Enum,
    pod,
)

# LOCK-END


# LOCK-BEGIN[class(RiskError)]: DON'T MODIFY
@pod
class RiskError(Enum[AutoTagType]):
    INVALID_ACCOUNT_TAG = None
    ACCOUNT_ALREADY_INITIALIZED = None
    INVALID_RISK_SIGNER = None
    INVALID_ACCOUNT_OWNER = None
    INVALID_ACCOUNT_ADDRESS = None
    INVALID_COVARIANCE_AUTHORITY = None
    INVALID_COVARIANCE_MATRIX_ACCESS = None
    MISSING_COVARIANCE_ENTRY = None
    INVALID_SQRT_INPUT = None
    INVALID_COVARIANCE_INPUT = None
    MISSING_B_B_O_FOR_MARK_PRICE = None
    NUMERICAL_OVERFLOW = None
    UNEXPECTED_PRODUCT_TYPE = None
    UNEXPECTED_RESULT = None
    MISMATCHED_RISK_STATE_ACCOUNT = None
    FAILED_TO_FIND_CACHE_INDEX_FOR_LEG = None
    COMBO_SIZE_GREATER_THAN_COLLECTION_LEN = None
    INVALID_MARK_PRICE_ACCOUNTS_LEN = None
    MISMATCHED_ORACLE_PRICE_ACCOUNT = None
    MISSING_MARK_PRICE = None
    INCORRECT_MARK_PRICES_BUMP = None
    MARK_PRICES_ARRAY_IS_FULL = None
    MARK_PRICES_OUT_OF_DATE = None
    # LOCK-END

    @classmethod
    def _to_bytes_partial(cls, buffer, obj, **kwargs):
        # to modify packing, change this method
        return super()._to_bytes_partial(buffer, obj, **kwargs)

    @classmethod
    def _from_bytes_partial(cls, buffer, **kwargs):
        # to modify unpacking, change this method
        return super()._from_bytes_partial(buffer, **kwargs)

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
