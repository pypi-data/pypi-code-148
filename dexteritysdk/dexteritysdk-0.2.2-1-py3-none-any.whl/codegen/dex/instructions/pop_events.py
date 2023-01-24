# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.codegen.dex.types import PopEventsParams
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


# LOCK-BEGIN[ix_cls(pop_events)]: DON'T MODIFY
@dataclass
class PopEventsIx:
    program_id: PublicKey

    # account metas
    authority: AccountMeta
    market_product_group: AccountMeta
    product: AccountMeta
    aaob_program: AccountMeta
    market_signer: AccountMeta
    orderbook: AccountMeta
    event_queue: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    # data fields
    params: PopEventsParams

    def to_instruction(self):
        keys = []
        keys.append(self.authority)
        keys.append(self.market_product_group)
        keys.append(self.product)
        keys.append(self.aaob_program)
        keys.append(self.market_signer)
        keys.append(self.orderbook)
        keys.append(self.event_queue)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.POP_EVENTS))
        buffer.write(BYTES_CATALOG.pack(PopEventsParams, self.params))

        return TransactionInstruction(
            keys=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(pop_events)]: DON'T MODIFY
def pop_events(
    authority: Union[str, PublicKey, AccountMeta],
    market_product_group: Union[str, PublicKey, AccountMeta],
    product: Union[str, PublicKey, AccountMeta],
    aaob_program: Union[str, PublicKey, AccountMeta],
    market_signer: Union[str, PublicKey, AccountMeta],
    orderbook: Union[str, PublicKey, AccountMeta],
    event_queue: Union[str, PublicKey, AccountMeta],
    params: PopEventsParams,
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[PublicKey] = None,
):
    if program_id is None:
        program_id = PublicKey("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(authority, (str, PublicKey)):
        authority = to_account_meta(
            authority,
            is_signer=True,
            is_writable=False,
        )
    if isinstance(market_product_group, (str, PublicKey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(product, (str, PublicKey)):
        product = to_account_meta(
            product,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(aaob_program, (str, PublicKey)):
        aaob_program = to_account_meta(
            aaob_program,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(market_signer, (str, PublicKey)):
        market_signer = to_account_meta(
            market_signer,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(orderbook, (str, PublicKey)):
        orderbook = to_account_meta(
            orderbook,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(event_queue, (str, PublicKey)):
        event_queue = to_account_meta(
            event_queue,
            is_signer=False,
            is_writable=True,
        )

    return PopEventsIx(
        program_id=program_id,
        authority=authority,
        market_product_group=market_product_group,
        product=product,
        aaob_program=aaob_program,
        market_signer=market_signer,
        orderbook=orderbook,
        event_queue=event_queue,
        remaining_accounts=remaining_accounts,
        params=params,
    ).to_instruction()

# LOCK-END
