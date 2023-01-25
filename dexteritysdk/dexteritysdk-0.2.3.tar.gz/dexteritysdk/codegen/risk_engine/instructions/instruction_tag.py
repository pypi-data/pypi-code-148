# LOCK-BEGIN[imports]: DON'T MODIFY
from dexteritysdk.solmate.anchor import InstructionDiscriminant
from podite import (
    Enum,
    U64,
    pod,
)

# LOCK-END


# LOCK-BEGIN[instruction_tag]: DON'T MODIFY
@pod
class InstructionTag(Enum[U64]):
    VALIDATE_ACCOUNT_HEALTH = InstructionDiscriminant()
    VALIDATE_ACCOUNT_LIQUIDATION = InstructionDiscriminant()
    CREATE_RISK_STATE_ACCOUNT = InstructionDiscriminant()
    INITIALIZE_COVARIANCE_MATRIX = InstructionDiscriminant()
    INITIALIZE_MARK_PRICES = InstructionDiscriminant()
    CLOSE_MARK_PRICES = InstructionDiscriminant()
    UPDATE_MARK_PRICES = InstructionDiscriminant()
    # LOCK-END
