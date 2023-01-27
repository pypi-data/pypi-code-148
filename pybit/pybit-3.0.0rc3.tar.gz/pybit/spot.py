from ._http_manager import _V3HTTPManager
from ._websocket_stream import _V3WebSocketManager
from ._websocket_stream import SPOT
from . import _helpers

from concurrent.futures import ThreadPoolExecutor


ws_name = SPOT
PUBLIC_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/spot/public/v3"
PRIVATE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/spot/private/v3"


class HTTP(_V3HTTPManager):
    def get_instruments(self):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/symbols",
        )

    def get_tickers(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/quote/ticker/24hr",
            query=kwargs
        )

    def get_order_book(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/quote/depth",
            query=kwargs
        )

    def get_merged_order_book(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/quote/depth/merged",
            query=kwargs
        )

    def get_klines(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/quote/kline",
            query=kwargs
        )

    def get_public_trading_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/quote/trades",
            query=kwargs
        )

    def get_last_traded_price(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/quote/ticker/price",
            query=kwargs
        )

    def get_best_bid_ask_price(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/quote/ticker/bookTicker",
            query=kwargs
        )

    def place_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/order",
            query=kwargs,
            auth=True
        )

    def get_open_orders(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/open-orders",
            query=kwargs,
            auth=True
        )

    def get_orders(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/order",
            query=kwargs,
            auth=True
        )

    def get_order_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/history-orders",
            query=kwargs,
            auth=True
        )

    def cancel_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/cancel-order",
            query=kwargs,
            auth=True
        )

    def batch_cancel_orders(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/cancel-orders",
            query=kwargs,
            auth=True
        )

    def cancel_all_orders(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/cancel-orders-by-ids",
            query=kwargs,
            auth=True
        )

    def get_trade_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/my-trades",
            query=kwargs,
            auth=True
        )

    def get_wallet_balance(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/account",
            query=kwargs,
            auth=True
        )

    def get_server_time(self):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/server-time",
            auth=False
        )

    def borrow_cross_margin_loan(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/cross-margin-loan",
            query=kwargs,
            auth=True
        )

    def repay_cross_margin_loan(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/cross-margin-repay",
            query=kwargs,
            auth=True
        )

    def get_cross_margin_borrowing_info(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/cross-margin-orders",
            query=kwargs,
            auth=True
        )

    def get_cross_margin_account_info(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/cross-margin-account",
            query=kwargs,
            auth=True
        )

    def get_cross_margin_interest_quota(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/cross-margin-loan-info",
            query=kwargs,
            auth=True
        )

    def get_cross_margin_repayment_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/cross-margin-repay-history",
            query=kwargs,
            auth=True
        )

    def get_leveraged_token_asset_info(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/infos",
            query=kwargs
        )

    def get_leveraged_token_market_info(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/reference",
            query=kwargs,
            auth=True
        )

    def purchase_leveraged_token(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/purchase",
            query=kwargs,
            auth=True
        )

    def redeem_leveraged_token(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/spot/v3/private/redeem",
            query=kwargs,
            auth=True
        )

    def get_leveraged_token_purchase_redemption_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/record",
            query=kwargs,
            auth=True
        )

    def get_institutional_loan_products(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/margin-product-infos",
            query=kwargs
        )

    def get_institutional_loan_margin_coins(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/public/margin-ensure-tokens",
            query=kwargs
        )

    def get_institutional_loans(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/margin-loan-infos",
            query=kwargs,
            auth=True
        )

    def get_institutional_loan_repayment_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/margin-repaid-infos",
            query=kwargs,
            auth=True
        )

    def get_institutional_loan_ltv(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/spot/v3/private/margin-ltv",
            query=kwargs,
            auth=True
        )


class WebSocket:
    def __init__(
            self,
            testnet,
            domain="",
            api_key=None,
            api_secret=None,
            ping_interval=20,
            ping_timeout=10,
            retries=10,
            restart_on_error=True,
            trace_logging=False
    ):
        self.ws_public = None
        self.ws_private = None
        self.active_connections = []
        self.args = _helpers.make_private_args(locals())
        self.public_args = _helpers.make_public_kwargs(self.args)

    def _ws_public_subscribe(self, topic, callback, symbol):
        if not self.ws_public:
            self.ws_public = _V3WebSocketManager(
                ws_name, **self.public_args)
            self.ws_public._connect(PUBLIC_WSS)
            self.active_connections.append(self.ws_public)
        self.ws_public.subscribe(topic, callback, symbol)

    def _ws_private_subscribe(self, topic, callback):
        if not self.ws_private:
            self.ws_private = _V3WebSocketManager(
                ws_name, **self.args)
            self.ws_private._connect(PRIVATE_WSS)
            self.active_connections.append(self.ws_private)
        self.ws_private.subscribe(topic, callback)

    def orderbook_stream(self, callback, symbol):
        """
        This topic always returns messages in the "snapshot" format for a
        simplified user experience. pybit processes the delta/snapshot
        messages for you. Read the Bybit API documentation for more information.

        """
        topic = "orderbook.40.{}"
        self._ws_public_subscribe(topic, callback, symbol)

    def trade_stream(self, callback, symbol):
        topic = "trade.{}"
        self._ws_public_subscribe(topic, callback, symbol)

    def kline_stream(self, callback, symbol, interval):
        topic = "kline.{}.{}"
        topic = topic.format(str(interval), "{}")
        self._ws_public_subscribe(topic, callback, symbol)

    def ticker_stream(self, callback, symbol):
        topic = "tickers.{}"
        self._ws_public_subscribe(topic, callback, symbol)

    def book_ticker_stream(self, callback, symbol):
        topic = "bookticker.{}"
        self._ws_public_subscribe(topic, callback, symbol)

    # Private topics
    def outbound_account_info_stream(self, callback):
        topic = "outboundAccountInfo"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def order_stream(self, callback):
        topic = "order"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def stop_order_stream(self, callback):
        topic = "stopOrder"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def ticket_info_stream(self, callback):
        topic = "ticketInfo"
        self._ws_private_subscribe(topic=topic, callback=callback)

