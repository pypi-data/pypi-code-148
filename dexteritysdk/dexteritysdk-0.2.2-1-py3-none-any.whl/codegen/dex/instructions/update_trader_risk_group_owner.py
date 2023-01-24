# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.solmate.utils import to_account_meta
from io import BytesIO
from podite import BYTES_CATALOG
from solana.publickey import PublicKey
from solana.transaction import (
    AccountMeta,
    TransactionInstruction,
)
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(update_trader_risk_group_owner)]: DON'T MODIFY
@dataclass
class UpdateTraderRiskGroupOwnerIx:
    program_id: PublicKey

    # account metas
    owner: AccountMeta
    trader_risk_group: AccountMeta
    new_owner: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.owner)
        keys.append(self.trader_risk_group)
        keys.append(self.new_owner)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.UPDATE_TRADER_RISK_GROUP_OWNER))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(update_trader_risk_group_owner)]: DON'T MODIFY
def update_trader_risk_group_owner(
    owner: Union[str, PublicKey, AccountMeta],
    trader_risk_group: Union[str, PublicKey, AccountMeta],
    new_owner: Union[str, PublicKey, AccountMeta],
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(owner, (str, PublicKey)):
        owner = to_account_meta(
            owner,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(trader_risk_group, (str, PublicKey)):
        trader_risk_group = to_account_meta(
            trader_risk_group,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(new_owner, (str, PublicKey)):
        new_owner = to_account_meta(
            new_owner,
            is_signer=False,
            is_writable=False,
        )

    return UpdateTraderRiskGroupOwnerIx(
        program_id=program_id,
        owner=owner,
        trader_risk_group=trader_risk_group,
        new_owner=new_owner,
        remaining_accounts=remaining_accounts,
    ).to_instruction()

# LOCK-END
