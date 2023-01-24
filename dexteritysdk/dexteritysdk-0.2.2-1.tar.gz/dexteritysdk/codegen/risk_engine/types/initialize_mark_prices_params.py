# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.codegen.instruments.types.oracle_type import OracleType
from podite import pod
from solana.publickey import PublicKey

# LOCK-END


# LOCK-BEGIN[class(InitializeMarkPricesParams)]: DON'T MODIFY
@pod
class InitializeMarkPricesParams:
    is_hardcoded_oracle: bool
    hardcoded_oracle: PublicKey
    hardcoded_oracle_type: OracleType
    # LOCK-END

    @classmethod
    def to_bytes(cls, obj, **kwargs):
        return cls.pack(obj, converter="bytes", **kwargs)

    @classmethod
    def from_bytes(cls, raw, **kwargs):
        return cls.unpack(raw, converter="bytes", **kwargs)
