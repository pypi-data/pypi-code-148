from decimal import Decimal
from typing import Optional


class Kyc:
    def __init__(self, kyc_data: dict):
        self.shared: bool = kyc_data.get('shared')
        self.external: bool = kyc_data.get('external')


class OrderValidation:
    def __init__(self, order_validation_data: dict):
        self.max_tokens_allowed: int = order_validation_data.get('maxTokensAllowed')
        has_kyc_asset_data: dict = order_validation_data.get('hasKycAsset')
        self.has_kyc_asset: HasKycAsset = HasKycAsset(has_kyc_asset_data) if has_kyc_asset_data is not None else None
        self.property_asset_balance: int = order_validation_data.get('propertyAssetBalance')
        self.payment_asset_balance: int = order_validation_data.get('paymentAssetBalance')


class DisplayStreams:
    def __init__(self, display_streams_data: dict):
        self.created_at: int = display_streams_data.get('createdAt')
        self.order_id: str = display_streams_data.get('orderId')
        self.id: str = display_streams_data.get('id')
        price: float = display_streams_data.get('price')
        self.price: Optional[Decimal] = Decimal(str(price)) if price is not None else None
        self.quantity: int = display_streams_data.get('quantity')
        self.property_id: str = display_streams_data.get('propertyId')
        self.status: str = display_streams_data.get('status')
        self.type: str = display_streams_data.get('type')
        self.active_state: str = display_streams_data.get('activeState')
        self.user_id: str = display_streams_data.get('userId')


class Cancelled:
    def __init__(self, cancelled_data: dict):
        self.id: str = cancelled_data.get('id')
        self.property_id: str = cancelled_data.get('propertyId')
        self.direction: str = cancelled_data.get('direction')
        self.status: str = cancelled_data.get('status')
        self.quantity: int = cancelled_data.get('quantity')
        price: float = cancelled_data.get('price')
        self.price: Optional[Decimal] = Decimal(str(price)) if price is not None else None
        self.quantity_executed: int = cancelled_data.get('quantityExecuted')
        self.payment_currency: str = cancelled_data.get('paymentCurrency')
        self.expire_at: int = cancelled_data.get('expireAt')
        self.display_streams: list[DisplayStreams] = [DisplayStreams(item) for item in
                                                      cancelled_data.get('displayStreams')]
        self.created_at: int = cancelled_data.get('createdAt')


class BuyTransactions:
    def __init__(self, buy_transactions_data: dict):
        self.created_at: int = buy_transactions_data.get('createdAt')
        self.buy_order_id: str = buy_transactions_data.get('buyOrderId')
        self.sell_order_id: str = buy_transactions_data.get('sellOrderId')
        self.id: str = buy_transactions_data.get('id')
        price: float = buy_transactions_data.get('price')
        self.price: Optional[Decimal] = Decimal(str(price)) if price is not None else None
        self.quantity: int = buy_transactions_data.get('quantity')
        self.property_id: str = buy_transactions_data.get('propertyId')
        self.buy_order_created_at: int = buy_transactions_data.get('buyOrderCreatedAt')
        self.sell_order_created_at: int = buy_transactions_data.get('sellOrderCreatedAt')
        self.buy_escrow_app_id: int = buy_transactions_data.get('buyEscrowAppId')
        self.sell_escrow_app_id: int = buy_transactions_data.get('sellEscrowAppId')
        self.payment_currency: str = buy_transactions_data.get('paymentCurrency')
        self.used_exchange_rate: int = buy_transactions_data.get('usedExchangeRate')
        self.blockchain_swap_txn_id: str = buy_transactions_data.get('blockchainSwapTxnId')
        self.swapped_amount: int = buy_transactions_data.get('swappedAmount')
        self.buyer_fee_amount: int = buy_transactions_data.get('buyerFeeAmount')
        self.seller_fee_amount: int = buy_transactions_data.get('sellerFeeAmount')


class Transactions:
    def __init__(self, transactions_data: dict):
        self.buy_transactions: list[BuyTransactions] = [BuyTransactions(item) for item in
                                                        transactions_data.get('buyTransactions')]
        # TODO: unsure what the type is here - possibly the same shape as BuyTransactions
        self.sell_transactions: list = transactions_data.get('sellTransactions')


class Executed:
    def __init__(self, executed_data: dict):
        self.id: str = executed_data.get('id')
        self.property_id: str = executed_data.get('propertyId')
        self.direction: str = executed_data.get('direction')
        self.status: str = executed_data.get('status')
        self.quantity: int = executed_data.get('quantity')
        price: float = executed_data.get('price')
        self.price: Optional[Decimal] = Decimal(str(price)) if price is not None else None
        self.quantity_executed: int = executed_data.get('quantityExecuted')
        self.payment_currency: str = executed_data.get('paymentCurrency')
        self.expire_at: int = executed_data.get('expireAt')
        self.display_streams: list[DisplayStreams] = [DisplayStreams(item) for item in
                                                      executed_data.get('displayStreams')]
        self.created_at: int = executed_data.get('createdAt')


class Orders:
    def __init__(self, orders_data: dict):
        executed_data: Optional[list] = orders_data.get('executed')
        self.executed: list[Executed] = [Executed(item) for item in executed_data] if executed_data else None
        cancelled_data: Optional[list] = orders_data.get('cancelled')
        self.cancelled: list[Cancelled] = [Cancelled(item) for item in cancelled_data] if cancelled_data else None


class HasKycAsset:
    def __init__(self, has_kyc_asset_data: dict):
        self.shared: bool = has_kyc_asset_data.get('shared')
        self.external: bool = has_kyc_asset_data.get('external')


class Property:
    def __init__(self, property_data: dict):
        orders_data: dict = property_data.get('orders')
        self.orders: Orders = Orders(orders_data) if orders_data is not None else None
        transactions_data: dict = property_data.get('transactions')
        self.transactions: Transactions = Transactions(transactions_data) if transactions_data is not None else None
        order_validation_data: dict = property_data.get('orderValidation')
        self.order_validation: OrderValidation = OrderValidation(
            order_validation_data) if order_validation_data is not None else None


class ExchangeUserInfo:
    def __init__(self, exchange_user_info_data: dict):
        kyc_data: dict = exchange_user_info_data.get('kyc')
        self.kyc: Kyc = Kyc(kyc_data) if kyc_data is not None else None
        properties_data: dict = exchange_user_info_data.get('properties')
        # note that the real API response has the properties as key-value pairs with
        # the property ID as the key, and the value as the property data
        self.properties: list[Property] = [Property(property_data) for property_data in
                                           properties_data.values()] if properties_data is not None else None
