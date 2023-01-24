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


# LOCK-BEGIN[ix_cls(validate_account_health)]: DON'T MODIFY
@dataclass
class ValidateAccountHealthIx:
    program_id: PublicKey

    # account metas
    market_product_group: AccountMeta
    trader_risk_group: AccountMeta
    risk_output_register: AccountMeta
    variance_cache: AccountMeta
    risk_model_configuration: AccountMeta
    risk_signer: AccountMeta
    covariance_metadata: AccountMeta
    correlation_matrix: AccountMeta
    mark_prices: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.market_product_group)
        keys.append(self.trader_risk_group)
        keys.append(self.risk_output_register)
        keys.append(self.variance_cache)
        keys.append(self.risk_model_configuration)
        keys.append(self.risk_signer)
        keys.append(self.covariance_metadata)
        keys.append(self.correlation_matrix)
        keys.append(self.mark_prices)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.VALIDATE_ACCOUNT_HEALTH))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(validate_account_health)]: DON'T MODIFY
def validate_account_health(
    market_product_group: Union[str, PublicKey, AccountMeta],
    trader_risk_group: Union[str, PublicKey, AccountMeta],
    risk_output_register: Union[str, PublicKey, AccountMeta],
    variance_cache: Union[str, PublicKey, AccountMeta],
    risk_model_configuration: Union[str, PublicKey, AccountMeta],
    risk_signer: Union[str, PublicKey, AccountMeta],
    covariance_metadata: Union[str, PublicKey, AccountMeta],
    correlation_matrix: Union[str, PublicKey, AccountMeta],
    mark_prices: Union[str, PublicKey, AccountMeta],
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("92wdgEqyiDKrcbFHoBTg8HxMj932xweRCKaciGSW3uMr")

    if isinstance(market_product_group, (str, PublicKey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(trader_risk_group, (str, PublicKey)):
        trader_risk_group = to_account_meta(
            trader_risk_group,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(risk_output_register, (str, PublicKey)):
        risk_output_register = to_account_meta(
            risk_output_register,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(variance_cache, (str, PublicKey)):
        variance_cache = to_account_meta(
            variance_cache,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(risk_model_configuration, (str, PublicKey)):
        risk_model_configuration = to_account_meta(
            risk_model_configuration,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(risk_signer, (str, PublicKey)):
        risk_signer = to_account_meta(
            risk_signer,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(covariance_metadata, (str, PublicKey)):
        covariance_metadata = to_account_meta(
            covariance_metadata,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(correlation_matrix, (str, PublicKey)):
        correlation_matrix = to_account_meta(
            correlation_matrix,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(mark_prices, (str, PublicKey)):
        mark_prices = to_account_meta(
            mark_prices,
            is_signer=False,
            is_writable=True,
        )

    return ValidateAccountHealthIx(
        program_id=program_id,
        market_product_group=market_product_group,
        trader_risk_group=trader_risk_group,
        risk_output_register=risk_output_register,
        variance_cache=variance_cache,
        risk_model_configuration=risk_model_configuration,
        risk_signer=risk_signer,
        covariance_metadata=covariance_metadata,
        correlation_matrix=correlation_matrix,
        mark_prices=mark_prices,
        remaining_accounts=remaining_accounts,
    ).to_instruction()

# LOCK-END
