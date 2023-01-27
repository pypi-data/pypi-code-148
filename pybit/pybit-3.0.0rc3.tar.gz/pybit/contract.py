from ._http_manager import _DerivativesHTTPManager
from ._websocket_stream import _V3WebSocketManager
from ._websocket_stream import CONTRACT
from . import _helpers


ws_name = CONTRACT
PUBLIC_INVERSE_WS = "wss://{SUBDOMAIN}.{DOMAIN}.com/contract/inverse/public/v3"
PUBLIC_USDT_WS = "wss://{SUBDOMAIN}.{DOMAIN}.com/contract/usdt/public/v3"
PUBLIC_USDC_PERPETUAL_WS = "wss://{SUBDOMAIN}.{DOMAIN}.com/contract/usdc/public/v3"
PUBLIC_USDC_OPTIONS_WS = "wss://{SUBDOMAIN}.{DOMAIN}.com/option/usdc/public/v3"
PRIVATE_CONTRACT_WS = "wss://{SUBDOMAIN}.{DOMAIN}.com/contract/private/v3"


class HTTP(_DerivativesHTTPManager):
    def place_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/order/create",
            query=kwargs,
            auth=True
        )

    def get_open_orders(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/order/unfilled-orders",
            query=kwargs,
            auth=True
        )

    def get_orders(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/order/list",
            query=kwargs,
            auth=True
        )

    def replace_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/order/replace",
            query=kwargs,
            auth=True
        )

    def cancel_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/order/cancel",
            query=kwargs,
            auth=True
        )

    def cancel_all_orders(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/order/cancel-all",
            query=kwargs,
            auth=True
        )

    def get_position(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/position/list",
            query=kwargs,
            auth=True
        )

    def set_leverage(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/position/set-leverage",
            query=kwargs,
            auth=True
        )

    def set_trading_stop(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/position/trading-stop",
            query=kwargs,
            auth=True
        )

    def set_auto_add_margin(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/position/set-auto-add-margin",
            query=kwargs,
            auth=True
        )

    def set_risk_limit(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/position/set-risk-limit",
            query=kwargs,
            auth=True
        )

    def switch_tp_sl_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/position/switch-tpsl-mode",
            query=kwargs,
            auth=True
        )

    def switch_cross_isolated_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/position/switch-isolated",
            query=kwargs,
            auth=True
        )

    def switch_position_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/position/switch-mode",
            query=kwargs,
            auth=True
        )

    def get_trade_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/execution/list",
            query=kwargs,
            auth=True
        )

    def get_closed_profit_and_loss_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/position/closed-pnl",
            query=kwargs,
            auth=True
        )

    def get_wallet_balance(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/account/wallet/balance",
            query=kwargs,
            auth=True
        )

    def get_trading_fee_rate(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/account/fee-rate",
            query=kwargs,
            auth=True
        )

    def get_wallet_fund_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/contract/v3/private/account/wallet/fund-records",
            query=kwargs,
            auth=True
        )

    def set_margin_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/contract/v3/private/account/setMarginMode",
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

    @staticmethod
    def _determine_public_ws_connection(symbol):
        if _helpers.is_inverse_contract(symbol):
            return PUBLIC_INVERSE_WS
        elif _helpers.is_usdt_perpetual(symbol):
            return PUBLIC_USDT_WS
        elif _helpers.is_usdc_perpetual(symbol):
            return PUBLIC_USDC_PERPETUAL_WS
        elif _helpers.is_usdc_option(symbol):
            return PUBLIC_USDC_OPTIONS_WS

    def _ws_public_subscribe(self, topic, callback, symbol):
        ws_public = self._determine_public_ws_connection(symbol)

        if not self.ws_public:
            self.ws_public = \
                _V3WebSocketManager(ws_name, **self.public_args)
            self.ws_public._connect(ws_public)
            self.active_connections.append(self.ws_public)
        self.ws_public.subscribe(topic, callback, symbol)

    def _ws_private_subscribe(self, topic, callback):
        if not self.ws_private:
            self.ws_private = \
                _V3WebSocketManager(ws_name, **self.args)
            self.ws_private._connect(PRIVATE_CONTRACT_WS)
            self.active_connections.append(self.ws_private)
        self.ws_private.subscribe(topic, callback)

    def orderbook_stream(self, callback, symbol, level):
        """
        This topic always returns messages in the "snapshot" format for a
        simplified user experience. pybit processes the delta/snapshot
        messages for you. Read the Bybit API documentation for more information.

        """
        topic = "orderbook.{}.{}"
        topic = topic.format(str(level), "{}")
        self._ws_public_subscribe(topic, callback, symbol)

    def trade_stream(self, callback, symbol):
        topic = "publicTrade.{}"
        self._ws_public_subscribe(topic, callback, symbol)

    def ticker_stream(self, callback, symbol):
        topic = "tickers.{}"
        self._ws_public_subscribe(topic, callback, symbol)

    def kline_stream(self, callback, symbol, interval):
        topic = "kline.{}.{}"
        topic = topic.format(str(interval), "{}")
        self._ws_public_subscribe(topic, callback, symbol)

    def liquidation_stream(self, callback, symbol):
        topic = "liquidation.{}"
        self._ws_public_subscribe(topic, callback, symbol)

    # Private topics
    def position_stream(self, callback):
        topic = "user.position.contractAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def execution_stream(self, callback):
        topic = "user.execution.contractAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def order_stream(self, callback):
        topic = "user.order.contractAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def wallet_stream(self, callback):
        topic = "user.wallet.contractAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)
