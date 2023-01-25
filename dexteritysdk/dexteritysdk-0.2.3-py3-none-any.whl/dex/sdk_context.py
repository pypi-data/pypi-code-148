import threading
from io import BytesIO

import base58

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Optional, Callable, Any

from borsh_construct import CStruct, U32, U8
from solana.rpc import commitment, types
from solana.rpc.commitment import Confirmed
from solana.rpc.websocket_api import connect as solana_ws_connect
from solders.rpc.responses import AccountNotification, SubscriptionResult, SubscriptionError
from spl.token import instructions as spl_token_instructions

from dexteritysdk.codegen.instruments.types import DerivativeMetadata
from dexteritysdk.codegen.risk_engine.types import MarkPricesArray
from dexteritysdk.pyserum.structs.event_queue import FillEvent, OutEvent
from dexteritysdk.pyserum.layouts.event_queue import Side
from dexteritysdk.pyserum.event_queue import EventQueue
from dexteritysdk.pyserum.orderbook import OrderBook

from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import AccountMeta, TransactionInstruction
from solana import system_program

import dexteritysdk.codegen.dex.instructions as dixs
import dexteritysdk.codegen.dex.types as dtys
import dexteritysdk.codegen.risk_engine.instructions as rixs
from dexteritysdk import program_ids as pids, mints
from dexteritysdk.codegen.dex.accounts import Accounts as DexAccounts
from dexteritysdk.codegen.dex.constants import SENTINEL
from dexteritysdk.codegen.dex.types import MarketProductGroup, CancelOrderParams, ProductMetadata, account_tag
from dexteritysdk.codegen.risk_engine.accounts import Accounts as RiskEngineAccounts
from dexteritysdk.constant_fees import instructions as fee_ixs
from dexteritysdk.dex import addrs as daddrs
from dexteritysdk.dex.actions import DexOrderSummary
from dexteritysdk.utils import solana as solana_utils
from dexteritysdk.utils.aob import state as aaob_state
from dexteritysdk.codegen.instruments.accounts import Accounts as InstrumentAccounts
from dexteritysdk.utils.solana import Client, Context, AccountParser, explore, fetch_account_details
from dexteritysdk.solmate.utils import to_account_meta


class SDKEventType(Enum):
    SNAPSHOT = 1
    NEW = 2
    UPDATED = 3
    CLOSED = 4
    CANCELLED = 5
    FILLED = 6


@dataclass
class SDKFill:
    product: "SDKProduct"
    side: aaob_state.Side
    order_id: int
    qty: float


@dataclass
class SDKPosition:
    product: "SDKProduct"
    position: float
    pending_position: float
    last_cum_funding_snapshot: float
    last_social_loss_snapshot: float


@dataclass
class SDKOrder:
    order_id: int
    product: "SDKProduct"
    side: aaob_state.Side
    price: float
    qty: float

    @staticmethod
    def from_pyserum_orderbook(order_book: OrderBook, product: "SDKProduct", bids: bool) -> List["SDKOrder"]:
        return [
            SDKOrder(
                o.order_id,
                product,
                aaob_state.Side.BID if bids else aaob_state.Side.ASK,
                o.info.price,
                o.info.size
            ) for o in order_book.orders()
        ]


@dataclass
class SDKOrderSummary:
    order_id: int
    product: "SDKProduct"
    side: aaob_state.Side
    price: float
    qty: float
    filled_qty: float
    remaining_qty: float

    @staticmethod
    def from_dex_order_summary(sdk: "SDKContext", order_summary: DexOrderSummary, product: "SDKProduct",
                               side: aaob_state.Side, quantity: Union[dtys.Fractional, float],
                               price: Union[dtys.Fractional, float]) -> "SDKOrderSummary":
        if isinstance(quantity, dtys.Fractional):
            quantity = quantity.value
        if isinstance(price, dtys.Fractional):
            price = price.value
        order_id = None if order_summary.posted_order_id == order_summary.posted_order_id.NONE \
            else order_summary.posted_order_id.field
        if order_id:
            price = OrderBook.get_price_from_key(order_id, product.metadata.tick_size, product.metadata.price_offset)
        remaining_qty = order_summary.total_base_qty_posted / (10 ** sdk.decimals)
        filled_qty = quantity - remaining_qty
        return SDKOrderSummary(
            order_id=order_id,
            product=product,
            side=side,
            price=price,
            qty=quantity,
            filled_qty=filled_qty,
            remaining_qty=remaining_qty
        )


@dataclass
class SDKProduct:
    key: PublicKey
    index: int
    name: str  # max 16 bytes
    orderbook: PublicKey
    bids: PublicKey
    asks: PublicKey
    market_signer: PublicKey
    event_queue: PublicKey
    metadata: ProductMetadata  # last time prod was fetched
    _orderbook_data: "SDKOrderBook" = None

    def __hash__(self):
        return self.key.__hash__()

    def get_orderbook(self, sdk: "SDKContext", refresh: bool = False) -> "SDKOrderBook":
        if refresh or self._orderbook_data is None:
            self._orderbook_data = SDKOrderBook.from_product(sdk, self)
        return self._orderbook_data

    def crank_raw(self, sdk: "SDKContext", trader_and_risk_accounts: List[PublicKey], reward_target: PublicKey):
        trader_and_risk_accounts.sort()
        trader_and_risk_accounts = _dedup(trader_and_risk_accounts)
        ix = dixs.consume_orderbook_events(
            aaob_program=sdk.aaob_program,
            market_product_group=sdk.market_product_group,
            product=self.key,
            market_signer=self.market_signer,
            orderbook=self.orderbook,
            event_queue=self.event_queue,
            reward_target=reward_target,
            fee_model_program=sdk.fee_model_program,
            fee_model_configuration_acct=sdk.fee_model_configuration_acct,
            fee_output_register=sdk.fee_output_register,
            risk_and_fee_signer=daddrs.get_risk_signer(sdk.market_product_group),
            params=dtys.ConsumeOrderbookEventsParams(
                20
            ),
            remaining_accounts=[AccountMeta(pk, False, False) for pk in trader_and_risk_accounts]
        )
        solana_utils.send_instructions(ix)


def _dedup(xs):
    if len(xs) < 2:
        return xs
    i = 0
    for acct in xs[1:]:
        if xs[i] != acct:
            i += 1
            xs[i] = acct
    return xs[:i + 1]


@dataclass
class SDKOrderBook:
    product: SDKProduct
    bids: List[SDKOrder]
    asks: List[SDKOrder]

    @staticmethod
    def from_product(sdk: "SDKContext", product: "SDKProduct") -> "SDKOrderBook":
        bids_data = explore(product.bids).data
        asks_data = explore(product.asks).data

        return SDKOrderBook(
            product=product,
            bids=SDKOrder.from_pyserum_orderbook(
                order_book=OrderBook.from_bytes(bids_data, product.metadata.base_decimals,
                                                product.metadata.price_offset, product.metadata.tick_size),
                product=product,
                bids=True,
            ),
            asks=SDKOrder.from_pyserum_orderbook(
                order_book=OrderBook.from_bytes(asks_data, product.metadata.base_decimals,
                                                product.metadata.price_offset, product.metadata.tick_size),
                product=product,
                bids=False,
            )
        )

    def find_order(self, order_id: int) -> SDKOrder:
        bid_match = next((o for o in self.bids if o.order_id == order_id), None)
        return bid_match if bid_match is not None else next((o for o in self.asks if o.order_id == order_id), None)


@dataclass
class _PendingNewOrder:
    product: Union[SDKProduct, PublicKey]
    side: aaob_state.Side
    size: Union[dtys.Fractional, float]
    price: Union[dtys.Fractional, float]
    self_trade_behavior: aaob_state.SelfTradeBehavior
    order_type: dtys.OrderType


@dataclass
class SDKTrader:
    keypair: Keypair
    account: PublicKey
    wallet: PublicKey
    trader_fee_state_acct: PublicKey
    trader_risk_state_acct: PublicKey  # separate pk vs kp to allow **vars(trader) in ixs
    whitelist_token_wallet: PublicKey

    _batches_lock: threading.Lock
    _batch_id: int
    _pending_batches: dict

    async def _monitor_accounts(
            self,
            sdk: "SDKContext",
            url: str,
            positions_callback: Callable[[List[SDKPosition], SDKEventType], Any],
            orders_callback: Callable[[List[SDKOrder], SDKEventType], Any],
            fills_callback: Callable[[SDKFill, SDKEventType], Any]
    ):
        def is_event_queue(acc: PublicKey) -> bool:
            return acc != self.account

        async for ws in solana_ws_connect(url):
            try:
                prev_trg = None
                trg, trg_slot = self.get_trader_risk_group()

                positions = None
                if positions_callback:
                    positions = list(self.open_positions(sdk, trg=trg))
                    positions_callback(positions, SDKEventType.SNAPSHOT)

                open_order_ids = defaultdict(set)
                if orders_callback:
                    open_orders = list(self.open_orders(sdk, trg=trg))
                    orders_callback(open_orders, SDKEventType.SNAPSHOT)
                    for o in open_orders:
                        open_order_ids[o.product].add(o.order_id)

                sub_to_pubkey = dict()
                event_queue_to_product = {product.event_queue: product for product in sdk.products}

                accounts = [product.event_queue for product in sdk.products]
                accounts.append(self.account)

                for account in accounts:
                    await ws.account_subscribe(account, commitment=commitment.Confirmed, encoding="base64")

                handled_orders = set()
                pending_products = set()

                def handle_cancelled_orders(product):
                    prev_open_order_ids = open_order_ids[product]

                    new_open_order_ids = set(
                        [order for _, order in self.open_order_ids(sdk, products=[product], trg=trg)]
                    )

                    open_order_ids[product] = new_open_order_ids

                    removed_order_ids = prev_open_order_ids.difference(new_open_order_ids)
                    for removed_order_id in removed_order_ids:
                        if removed_order_id in handled_orders:
                            handled_orders.remove(removed_order_id)
                            continue

                        removed_order_price = OrderBook.get_price_from_key(
                            removed_order_id,
                            product.metadata.tick_size,
                            product.metadata.price_offset
                        )
                        removed_order_side = aaob_state.Side.BID if OrderBook.key_is_bid(removed_order_id) \
                            else aaob_state.Side.ASK
                        removed_order_size = 0

                        if prev_trg is not None:
                            order_idx = prev_trg.open_orders.products[product.index].head_index
                            while order_idx != SENTINEL:
                                curr_order = prev_trg.open_orders.orders[order_idx]
                                if curr_order.id == removed_order_id:
                                    removed_order_size = curr_order.qty
                                    break
                                order_idx = curr_order.next

                        orders_callback(
                            [SDKOrder(
                                removed_order_id,
                                product,
                                removed_order_side,
                                removed_order_price,
                                removed_order_size / (10 ** product.metadata.base_decimals),
                            )],
                            SDKEventType.CANCELLED
                        )

                async for msgs in ws:
                    for msg in msgs:
                        if isinstance(msg, SubscriptionResult):
                            sub_to_pubkey[msg.result] = accounts[msg.id - 1]
                        elif isinstance(msg, SubscriptionError):
                            raise ValueError(f"Failed to subscribe [account={accounts[msg.id - 1]}, exc={msg}]")
                        elif isinstance(msg, AccountNotification):
                            notification_account = sub_to_pubkey[msg.subscription]
                            data = msg.result.value.data
                            slot = msg.result.context.slot
                            if is_event_queue(notification_account):
                                if fills_callback or orders_callback:
                                    product = event_queue_to_product[notification_account]
                                    event_queue = EventQueue.from_bytes(data)
                                    for e in event_queue:
                                        if isinstance(e, FillEvent) and fills_callback:
                                            # if we were the maker
                                            if e.maker_callback.account == self.account:
                                                # convert taker to maker side
                                                maker_side = aaob_state.Side.BID \
                                                    if e.taker_side == Side.ASK else aaob_state.Side.ASK
                                                fill_size = e.base_size / (10 ** product.metadata.base_decimals)
                                                if fills_callback:
                                                    fills_callback(
                                                        SDKFill(
                                                            product,
                                                            maker_side,
                                                            e.maker_order_id,
                                                            fill_size
                                                        ),
                                                        SDKEventType.NEW
                                                    )
                                            # else if we were the taker
                                            elif e.taker_callback.account == self.account:
                                                taker_side = aaob_state.Side.ASK \
                                                    if e.taker_side == Side.ASK else aaob_state.Side.BID
                                                size = e.base_size / (10 ** product.metadata.base_decimals)
                                                if fills_callback:
                                                    fills_callback(
                                                        SDKFill(
                                                            product,
                                                            taker_side,
                                                            None,
                                                            size
                                                        ),
                                                        SDKEventType.NEW
                                                    )
                                        elif isinstance(e, OutEvent) and orders_callback:
                                            if e.callback.account == self.account:
                                                handled_orders.add(e.order_id)
                                                event_type = SDKEventType.FILLED if e.base_size == 0 \
                                                    else SDKEventType.CANCELLED
                                                side = aaob_state.Side.BID if OrderBook.key_is_bid(e.order_id) \
                                                    else aaob_state.Side.ASK
                                                price = OrderBook.get_price_from_key(
                                                    e.order_id,
                                                    product.metadata.tick_size,
                                                    product.metadata.price_offset
                                                )
                                                orders_callback(
                                                    [SDKOrder(
                                                        e.order_id,
                                                        product,
                                                        side,
                                                        price,
                                                        e.base_size / (10 ** product.metadata.base_decimals)
                                                    )],
                                                    event_type
                                                )

                                    # try to infer what happened to the rest of our open orders
                                    if orders_callback:
                                        if slot != trg_slot:
                                            pending_products.add(product)
                                            continue

                                        handle_cancelled_orders(product)
                            else:
                                prev_trg = trg
                                trg = DexAccounts.from_bytes(data).field
                                trg_slot = slot

                                for p in pending_products:
                                    handle_cancelled_orders(p)

                                pending_products = set()

                                if positions_callback:
                                    new_positions = list(self.open_positions(sdk, trg))
                                    for position in positions:
                                        new_position = next(
                                            (p for p in new_positions if p.product == position.product),
                                            None
                                        )
                                        # if position was closed
                                        if not new_position:
                                            positions_callback([SDKPosition(position.product, 0, 0, 0, 0)],
                                                               SDKEventType.CLOSED)
                                        # if existing position has changed
                                        elif position != new_position:
                                            positions_callback([new_position], SDKEventType.UPDATED)

                                    for new_position in new_positions:
                                        old_position = next(
                                            (p for p in positions if p.product == new_position.product),
                                            None
                                        )
                                        # if new position
                                        if not old_position:
                                            positions_callback([new_position], SDKEventType.NEW)

                                    positions = new_positions

                        else:
                            print(f"Unknown msg: {msg}")
            except Exception as e:
                print(f"Monitoring Exception: {str(e)}")
                continue

    async def subscribe(
            self,
            sdk: "SDKContext",
            ws_url: str,
            positions_callback: Callable[[List[SDKPosition], SDKEventType], Any] = None,
            orders_callback: Callable[[List[SDKOrder], SDKEventType], Any] = None,
            fills_callback: Callable[[SDKFill, SDKEventType], Any] = None,
    ):
        await self._monitor_accounts(sdk, ws_url, positions_callback, orders_callback, fills_callback)

    @staticmethod
    def connect(
            sdk: "SDKContext",
            account: PublicKey,
            keypair: Keypair,
    ) -> "SDKTrader":
        wallet = spl_token_instructions.get_associated_token_address(keypair.public_key, sdk.vault_mint)
        trader_fee_state_acct = daddrs.get_trader_fee_state_acct(account, sdk.market_product_group,
                                                                 sdk.fee_model_program)
        trg: dtys.TraderRiskGroup = explore(account).data_obj
        assert trg.market_product_group == sdk.market_product_group
        assert trg.fee_state_account == trader_fee_state_acct
        assert trg.owner == keypair.public_key

        whitelist_token_wallet = spl_token_instructions.get_associated_token_address(
            keypair.public_key,
            mints.WHITELIST_TOKEN_MINT
        )

        return SDKTrader(
            keypair, account, wallet, trader_fee_state_acct, trg.risk_state_account, whitelist_token_wallet,
            _batches_lock=threading.Lock(), _batch_id=0, _pending_batches={})

    def get_trader_risk_group(self) -> (dtys.TraderRiskGroup, int):
        account_details = fetch_account_details(self.account)
        return account_details.data_obj, account_details.slot

    def deposit(self, sdk: "SDKContext", qty: Union[float, dtys.Fractional]):
        if not isinstance(qty, dtys.Fractional):
            qty = dtys.Fractional(int(qty * (10 ** sdk.decimals)), sdk.decimals)
        ix = dixs.deposit_funds(
            user=self.keypair.public_key,
            user_token_account=self.wallet,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            market_product_group_vault=sdk.market_product_group_vault,
            capital_limits=sdk.capital_limits,
            whitelist_ata_acct=self.whitelist_token_wallet,
            params=dtys.DepositFundsParams(
                quantity=qty,
            ),
            program_id=sdk.dex_program,
        )
        return sdk.send_instructions(ix)

    def withdraw(self, sdk: "SDKContext", qty: Union[float, dtys.Fractional]):
        if not isinstance(qty, dtys.Fractional):
            qty = dtys.Fractional(int(qty * sdk.decimals), sdk.decimals)
        update_mark_prices_ix = self._update_mark_prices_ix(sdk)
        ix = dixs.withdraw_funds(
            user=self.keypair.public_key,
            user_token_account=self.wallet,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            market_product_group_vault=sdk.market_product_group_vault,
            risk_output_register=sdk.risk_output_register,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_signer=sdk.risk_signer,
            capital_limits=sdk.capital_limits,
            trader_risk_state_acct=self.trader_risk_state_acct,
            params=dtys.WithdrawFundsParams(
                quantity=qty,
            ),
            program_id=sdk.dex_program,
        )
        return sdk.send_instructions(update_mark_prices_ix, ix)

    def init_batch(self):
        self._batches_lock.acquire()
        batch_id = self._batch_id
        self._batch_id += 1
        self._batches_lock.release()
        self._pending_batches[batch_id] = []
        return batch_id

    def commit_batch(self, sdk: "SDKContext", batch_id: int) -> List[SDKOrderSummary]:
        if batch_id not in self._pending_batches:
            raise ValueError("Invalid batch_id")

        pending_actions = self._pending_batches.pop(batch_id)
        assert(pending_actions and len(pending_actions) > 0)

        ixs = []
        pending_places = []
        for a in pending_actions:
            if isinstance(a, _PendingNewOrder):
                pending_places.append(a)
                ixs.append(self._place_order_ix(sdk, a.product, a.side, a.size, a.price, a.self_trade_behavior,
                                                a.order_type, sdk.additional_risk_accts))
            else:
                ixs.append(a)

        ixs.insert(0, self._update_mark_prices_ix(sdk))
        ixs.insert(0, self._request_compute_ix(sdk))

        trans_details = sdk.send_instructions(*ixs, raise_on_error=False)
        if trans_details.error:
            raise ValueError(trans_details.error_from_log)
        else:
            return [
                SDKOrderSummary.from_dex_order_summary(
                    sdk,
                    DexOrderSummary.from_bytes(raw_summary),
                    pending_places[idx].product,
                    pending_places[idx].side,
                    pending_places[idx].size,
                    pending_places[idx].price
                ) for idx, raw_summary in enumerate(trans_details.emitted_dex_order_summaries())
            ]

    def _request_compute_ix(self, sdk: "SDKContext", units: int = 1400000):
        request_units = CStruct(
            "units" / U32,
        )

        buffer = BytesIO()
        # this is the enum value for SetComputeUnitLimit
        buffer.write(U8.build(2))
        buffer.write(request_units.build({"units": units}))

        return TransactionInstruction(
            [],
            PublicKey("ComputeBudget111111111111111111111111111111"),
            buffer.getvalue()
        )

    def place_order(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, PublicKey],
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.CANCEL_PROVIDE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT,
            batch_id: int = None
    ) -> SDKOrderSummary:
        ix = self._place_order_ix(sdk, product, side, size, price, self_trade_behavior, order_type,
                                  sdk.additional_risk_accts)
        if batch_id is not None:
            self._pending_batches[batch_id].append(_PendingNewOrder(product, side, size, price, self_trade_behavior, order_type))
        else:
            request_compute_ix = self._request_compute_ix(sdk, 800000)
            update_mark_prices_ix = self._update_mark_prices_ix(sdk)
            trans_details = sdk.send_instructions(request_compute_ix, update_mark_prices_ix, ix, raise_on_error=False)
            if trans_details.error:
                raise ValueError(trans_details.error_from_log)
            else:
                raw_summary = trans_details.emitted_logs["new-order:order-summary"]
                return SDKOrderSummary.from_dex_order_summary(sdk, DexOrderSummary.from_bytes(raw_summary),
                                                              product, side, size, price)

    def _place_order_ix(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, PublicKey],
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.CANCEL_PROVIDE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT,
            risk_accounts: Optional[List[PublicKey]] = None,
    ):
        remaining_accounts = [to_account_meta(ra, is_signer=False, is_writable=True) for ra in risk_accounts]

        ix = dixs.new_order(
            program_id=sdk.dex_program,
            user=self.keypair.public_key,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            product=product.key,
            aaob_program=sdk.aaob_program,
            orderbook=product.orderbook,
            market_signer=product.market_signer,
            event_queue=product.event_queue,
            bids=product.bids,
            asks=product.asks,
            fee_model_program=sdk.fee_model_program,
            fee_model_configuration_acct=sdk.fee_model_configuration_acct,
            trader_fee_state_acct=self.trader_fee_state_acct,
            fee_output_register=sdk.fee_output_register,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_and_fee_signer=sdk.risk_signer,
            params=dtys.NewOrderParams(
                side=side,
                max_base_qty=dtys.Fractional.into(size, product.metadata.base_decimals),
                order_type=order_type,
                self_trade_behavior=self_trade_behavior,
                match_limit=10,
                limit_price=dtys.Fractional.into(price, product.metadata.base_decimals),
            ),
            remaining_accounts=remaining_accounts,
        )

        return ix

    def cancel(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            batch_id: int = None,
    ):
        self.cancel_underwater(sdk, product, order_id, self.account, batch_id)

    def cancel_underwater(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            under_water_trg: PublicKey,
            batch_id: int = None,
            no_err: bool = False,
    ):
        if batch_id is not None:
            self._pending_batches[batch_id].append(self._cancel_ix(sdk, product, order_id, under_water_trg, no_err))
        else:
            update_mark_prices_ix = self._update_mark_prices_ix(sdk)
            update_variance_cache_ix = self._update_variance_cache_ix(sdk)
            ix = self._cancel_ix(sdk, product, order_id, under_water_trg, no_err)
            trans_details = sdk.send_instructions(update_mark_prices_ix, ix, update_variance_cache_ix, raise_on_error=False)
            if trans_details.error:
                raise ValueError(f"{order_id}:" + trans_details.error_from_log)

    def _update_variance_cache_ix(
            self,
            sdk: "SDKContext"
    ):
        remaining_accounts = [
            to_account_meta(ra, is_signer=False, is_writable=True) for ra in sdk.additional_risk_accts
        ]

        return dixs.update_variance_cache(
            payer=self.keypair.public_key,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_and_fee_signer=sdk.risk_signer,
            remaining_accounts=remaining_accounts
        )

    def _update_mark_prices_ix(
            self,
            sdk: "SDKContext"
    ):
        remaining_accounts = [
            to_account_meta(ra, is_signer=False, is_writable=True) for ra in (sdk.mark_price_accounts + sdk.price_oracle_accounts)
        ]

        ix = rixs.update_mark_prices(
            payer=self.keypair.public_key,
            mark_prices=sdk.additional_risk_accts[2],
            market_product_group=sdk.market_product_group,
            remaining_accounts=remaining_accounts,
        )

        return ix

    def _cancel_ix(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            under_water_trg: PublicKey,
            no_err: bool,
    ):
        ix = dixs.cancel_order(
            user=self.keypair.public_key,
            trader_risk_group=under_water_trg,
            market_product_group=sdk.market_product_group,
            product=product.key,
            aaob_program=sdk.aaob_program,
            orderbook=product.orderbook,
            market_signer=product.market_signer,
            event_queue=product.event_queue,
            bids=product.bids,
            asks=product.asks,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_signer=sdk.risk_signer,
            params=CancelOrderParams(order_id=order_id, no_err=no_err),
            remaining_accounts=None,
            program_id=sdk.dex_program,
        )

        # workaround to correctly serialize no_err
        if no_err:
            return TransactionInstruction(
                keys=ix.keys,
                program_id=ix.program_id,
                data=ix.data[:-1] + b'\x01',
            )

        return ix

    def replace(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, PublicKey],
            order_id: int,
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.CANCEL_PROVIDE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT,
            batch_id: int = None,
            cancel_no_err: bool = True,
    ) -> DexOrderSummary:
        cancel_ix = self._cancel_ix(sdk, product, order_id, self.account, no_err=cancel_no_err)
        place_ix = self._place_order_ix(sdk, product, side, size, price, self_trade_behavior, order_type,
                                        sdk.additional_risk_accts)

        if batch_id is not None:
            self._pending_batches[batch_id].append(cancel_ix)
            self._pending_batches[batch_id].append(_PendingNewOrder(product, side, size, price, self_trade_behavior, order_type))
        else:
            request_compute_ix = self._request_compute_ix(sdk, 800000)
            update_mark_prices_ix = self._update_mark_prices_ix(sdk)
            trans_details = sdk.send_instructions(request_compute_ix, update_mark_prices_ix, cancel_ix, place_ix, raise_on_error=False)
            if trans_details.error:
                raise Exception(trans_details.error_from_log)
            else:
                raw_summary = trans_details.emitted_logs["new-order:order-summary"]
                return SDKOrderSummary.from_dex_order_summary(sdk, DexOrderSummary.from_bytes(raw_summary),
                                                              product, side, size, price)

    def open_positions(
            self,
            sdk: "SDKContext",
            trg: dtys.TraderRiskGroup = None
    ) -> Iterable[SDKPosition]:
        if not trg:
            trg, _ = self.get_trader_risk_group()
        for position in trg.trader_positions:
            if position.tag == account_tag.AccountTag.UNINITIALIZED or \
                    (position.position.value == 0 and position.pending_position.value == 0):
                continue
            yield SDKPosition(
                next(product for product in sdk.products if product.key == position.product_key),
                position.position.value,
                position.pending_position.value,
                position.last_cum_funding_snapshot.value,
                position.last_social_loss_snapshot.value
            )

    def open_orders(
            self,
            sdk: "SDKContext",
            products: List[SDKProduct] = None,
            trg: dtys.TraderRiskGroup = None
    ) -> Iterable[SDKOrder]:
        if products is None or len(products) == 0:
            products = sdk.products

        if not trg:
            trg, _ = self.get_trader_risk_group()
        for p in products:
            ptr = trg.open_orders.products[p.index].head_index
            order = trg.open_orders.orders[ptr]
            assert order.prev == SENTINEL
            while ptr != SENTINEL:
                order = trg.open_orders.orders[ptr]
                assert order.id != 0
                yield SDKOrder(
                    order.id,
                    p,
                    aaob_state.Side.BID if OrderBook.key_is_bid(order.id) else aaob_state.Side.ASK,
                    OrderBook.get_price_from_key(order.id, p.metadata.tick_size, p.metadata.price_offset),
                    order.qty / (10 ** p.metadata.base_decimals)
                )
                ptr = order.next

    def open_order_ids(
            self,
            sdk: "SDKContext",
            products: List[SDKProduct] = None,
            trg: dtys.TraderRiskGroup = None
    ) -> Iterable[SDKProduct, int]:
        if products is None or len(products) == 0:
            products = sdk.products

        if not trg:
            trg, _ = self.get_trader_risk_group()
        for p in products:
            ptr = trg.open_orders.products[p.index].head_index
            order = trg.open_orders.orders[ptr]
            assert order.prev == SENTINEL
            while ptr != SENTINEL:
                order = trg.open_orders.orders[ptr]
                assert order.id != 0
                yield p, order.id
                ptr = order.next

    def _chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def cancel_all_orders(
            self,
            sdk: "SDKContext",
            products: List[SDKProduct] = None,
            no_err: bool = True,
            batch_size: int = 8
    ):
        if products is None or len(products) == 0:
            products = sdk.products

        update_mark_prices_ix = self._update_mark_prices_ix(sdk)
        update_variance_cache_ix = self._update_variance_cache_ix(sdk)

        for p in products:
            open_orders = self.open_order_ids(sdk, [p])
            ixs = [self._cancel_ix(sdk, p, o, self.account, no_err) for p, o in open_orders]

            # batch cancels in tx's of batch_size
            for chunk in self._chunks(ixs, batch_size):
                sdk.send_instructions(update_mark_prices_ix, *chunk, update_variance_cache_ix)


@dataclass
class SDKContext:
    product_group_name: str  # max 16 chars
    trader_risk_state_account_len: int
    decimals: int
    # cached products, reload if necessary
    products: List[SDKProduct]
    # program_ids
    dex_program: PublicKey
    aaob_program: PublicKey
    risk_engine_program: PublicKey
    instruments_program: PublicKey
    # dummy_oracle_program_id: PublicKey
    fee_model_program: PublicKey
    # accts
    market_product_group: PublicKey
    capital_limits: PublicKey
    payer: Keypair
    market_product_group_vault: PublicKey
    vault_mint: PublicKey
    fee_model_configuration_acct: PublicKey
    risk_model_configuration_acct: PublicKey
    risk_signer: PublicKey
    fee_signer: PublicKey
    risk_output_register: PublicKey
    fee_output_register: PublicKey
    fee_collector: PublicKey
    mark_price_accounts: List[PublicKey]
    price_oracle_accounts: List[PublicKey]
    additional_risk_accts: List[PublicKey]

    @staticmethod
    def connect(client: Client,
                payer: Keypair,
                market_product_group_key: PublicKey,
                trader_risk_state_account_len: int = 0,
                dex_program_id: PublicKey = pids.DEX_PROGRAM_ID,
                aaob_program_id: PublicKey = pids.AOB_PROGRAM_ID,
                risk_engine_program_id: PublicKey = pids.RISK_ENGINE_PROGRAM_ID,
                instruments_program_id: PublicKey = pids.INSTRUMENTS_PROGRAM_ID,
                fee_model_program_id: PublicKey = pids.CONSTANT_FEES_MODEL_PROGRAM_ID,
                raise_on_error: bool = False,
                **kwargs):
        parser = AccountParser()
        parser.register_parser_from_account_enum(pids.DEX_PROGRAM_ID, DexAccounts)
        parser.register_parser_from_account_enum(pids.RISK_ENGINE_PROGRAM_ID, RiskEngineAccounts)
        parser.register_parser(pids.AOB_PROGRAM_ID, aaob_state.account_parser)
        parser.register_parser_from_account_enum(pids.INSTRUMENTS_PROGRAM_ID, InstrumentAccounts)
        Context.init_globals(
            fee_payer=payer,
            client=client,
            signers=[(payer, "payer")],
            parser=parser,
            raise_on_error=raise_on_error,
        )

        mpg: MarketProductGroup = solana_utils.explore(market_product_group_key).data_obj

        capital_limits_key, _ = PublicKey.find_program_address(
            [b"capital_limits_state", bytes(market_product_group_key)],
            dex_program_id
        )

        s_account, _ = PublicKey.find_program_address(
            [b"s", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        r_account, _ = PublicKey.find_program_address(
            [b"r", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        mark_prices_account, _ = PublicKey.find_program_address(
            [b"mark_prices", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        sdk_context = SDKContext(
            product_group_name=bytes(mpg.name).decode("utf-8").strip(),
            trader_risk_state_account_len=trader_risk_state_account_len,
            decimals=mpg.decimals,
            # cached products reload if necessary
            products=[],
            # program_ids
            dex_program=dex_program_id,
            aaob_program=aaob_program_id,
            risk_engine_program=risk_engine_program_id,
            instruments_program=instruments_program_id,
            # dummy_oracle_program_id=None,
            fee_model_program=fee_model_program_id,
            # accts
            market_product_group=market_product_group_key,
            capital_limits=capital_limits_key,
            payer=payer,
            market_product_group_vault=daddrs.get_market_product_group_vault(market_product_group_key),
            vault_mint=mpg.vault_mint,
            fee_model_configuration_acct=mpg.fee_model_configuration_acct,
            risk_model_configuration_acct=mpg.risk_model_configuration_acct,
            risk_signer=daddrs.get_risk_signer(market_product_group_key),
            fee_signer=daddrs.get_risk_signer(market_product_group_key),
            risk_output_register=mpg.risk_output_register,
            fee_output_register=mpg.fee_output_register,
            fee_collector=mpg.fee_collector,
            mark_price_accounts=list(),
            price_oracle_accounts=list(),
            additional_risk_accts=[s_account, r_account, mark_prices_account],
        )
        sdk_context.load_products()
        return sdk_context

    def list_trader_risk_groups(self) -> List[PublicKey]:
        account_discriminator_filter = types.MemcmpOpts(
            offset=0,
            bytes=str(base58.b58encode(
                int(DexAccounts.TRADER_RISK_GROUP).to_bytes(8, "little")
            ), 'utf-8')
        )
        mpg_filter = types.MemcmpOpts(
            offset=16,
            bytes=str(self.market_product_group.to_base58(), 'utf-8')
        )
        trader_filter = types.MemcmpOpts(
            offset=48,
            bytes=str(self.payer.public_key.to_base58(), 'utf-8')
        )
        response = Context.get_global_client().get_program_accounts(
            pubkey=self.dex_program,
            commitment=Confirmed,
            encoding="base64",
            data_slice=types.DataSliceOpts(offset=0, length=0),  # we don't need any data
            filters=[account_discriminator_filter, mpg_filter, trader_filter]
        )
        trgs = []
        for account in response.value:
            trgs.append(PublicKey.from_solders(account.pubkey))
        return trgs

    def load_mpg(self) -> MarketProductGroup:
        return solana_utils.fetch_account_details(self.market_product_group).data_obj

    def load_products(self):
        mpg = self.load_mpg()
        products = []
        mark_price_accounts = []
        price_oracle_accounts = []

        mark_prices: MarkPricesArray = fetch_account_details(self.additional_risk_accts[2]).data_obj
        if mark_prices.is_hardcoded_oracle:
            mark_price_accounts.append(mark_prices.hardcoded_oracle)

        for idx, prod in mpg.active_products():
            if mpg.is_expired(prod):
                continue
            metadata = prod.metadata()
            orderbook: aaob_state.MarketState = fetch_account_details(metadata.orderbook).data_obj
            products.append(
                SDKProduct(
                    metadata.product_key,
                    idx,
                    bytes(metadata.name).decode('utf-8').strip(),
                    orderbook=metadata.orderbook,
                    asks=orderbook.asks,
                    bids=orderbook.bids,
                    event_queue=orderbook.event_queue,
                    market_signer=daddrs.get_market_signer(metadata.product_key),
                    metadata=metadata,
                )
            )

            if not mark_prices.is_hardcoded_oracle and prod.is_outright():
                derivative_metadata: DerivativeMetadata = fetch_account_details(metadata.product_key).data_obj
                mark_price_accounts.append(metadata.product_key)
                price_oracle_accounts.append(derivative_metadata.price_oracle)

        self.products = products
        self.mark_price_accounts = mark_price_accounts
        self.price_oracle_accounts = price_oracle_accounts

    def send_instructions(self, *ixs: TransactionInstruction, **kwargs):
        return solana_utils.send_instructions(*ixs, **kwargs)

    def register_trader(self, keypair: Keypair):
        trader_risk_group = Keypair.generate()
        trader_risk_state_acct = Keypair.generate()
        _ident = keypair.public_key.to_base58()[:8]
        Context.add_signers(
            (trader_risk_state_acct, f"{_ident}'s trader_risk_state_acct"),
            (trader_risk_group, f"{_ident}'s trader_risk_group)"),
        )
        trader_fee_state_acct = daddrs.get_trader_fee_state_acct(
            trader_risk_group.public_key,
            self.market_product_group,
            self.fee_model_program)

        fee_ix = fee_ixs.initialize_trader_acct_ix(
            program_id=self.fee_model_program,
            payer=self.payer.public_key,
            fee_model_config_acct=self.fee_model_configuration_acct,
            trader_fee_acct=trader_fee_state_acct,
            market_product_group=self.market_product_group,
            trader_risk_group=trader_risk_group.public_key,
            system_program=SYS_PROGRAM_ID)
        size = dtys.TraderRiskGroup.calc_max_size() + 8
        allocate_trg = system_program.create_account(
            system_program.CreateAccountParams(
                from_pubkey=self.payer.public_key,
                new_account_pubkey=trader_risk_group.public_key,
                lamports=solana_utils.calc_rent(size),
                space=size,
                program_id=self.dex_program,
            )
        )
        trg_init_ix = dixs.initialize_trader_risk_group(
            owner=keypair.public_key,
            trader_risk_group=trader_risk_group.public_key,
            trader_risk_state_acct=trader_risk_state_acct.public_key,
            trader_fee_state_acct=trader_fee_state_acct,
            market_product_group=self.market_product_group,
            risk_signer=self.risk_signer,
            risk_engine_program=self.risk_engine_program,
            program_id=self.dex_program,
            # **vars(self),
        )
        self.send_instructions(fee_ix, allocate_trg, trg_init_ix)
        return SDKTrader.connect(
            self,
            trader_risk_group.public_key,
            keypair,
        )
