from ._http_manager import _DerivativesHTTPManager
from ._websocket_stream import _V3WebSocketManager
from ._websocket_stream import UNIFIED_MARGIN
from .contract import WebSocket as ContractWebSocket
from . import _helpers


ws_name = UNIFIED_MARGIN
from .contract import PUBLIC_USDT_WS
from .contract import PUBLIC_USDC_PERPETUAL_WS
from .contract import PUBLIC_USDC_OPTIONS_WS
PRIVATE_UNIFIED_MARGIN_WS = "wss://{SUBDOMAIN}.{DOMAIN}.com/unified/private/v3"


class HTTP(_DerivativesHTTPManager):
    def upgrade_to_unified_margin_account(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/account/upgrade-unified-account",
            query=kwargs,
            auth=True
        )

    def place_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/order/create",
            query=kwargs,
            auth=True
        )

    def batch_place_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/order/create-batch",
            query=kwargs,
            auth=True
        )

    def get_open_orders(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/order/unfilled-orders",
            query=kwargs,
            auth=True
        )

    def get_orders(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/order/list",
            query=kwargs,
            auth=True
        )

    def replace_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/order/replace",
            query=kwargs,
            auth=True
        )

    def batch_replace_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/order/replace-batch",
            query=kwargs,
            auth=True
        )

    def cancel_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/order/cancel",
            query=kwargs,
            auth=True
        )

    def batch_cancel_order(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/order/cancel-batch",
            query=kwargs,
            auth=True
        )

    def cancel_all_orders(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/order/cancel-all",
            query=kwargs,
            auth=True
        )

    def get_position(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/position/list",
            query=kwargs,
            auth=True
        )

    def set_leverage(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/position/set-leverage",
            query=kwargs,
            auth=True
        )

    def set_trading_stop(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/position/trading-stop",
            query=kwargs,
            auth=True
        )

    def set_auto_add_margin(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/position/set-auto-add-margin",
            query=kwargs,
            auth=True
        )

    def set_risk_limit(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/position/set-risk-limit",
            query=kwargs,
            auth=True
        )

    def switch_tp_sl_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint +
                 "/unified/v3/private/position/tpsl/switch-mode",
            query=kwargs,
            auth=True
        )

    def switch_margin_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/position/switch-isolated",
            query=kwargs,
            auth=True
        )

    def switch_position_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/position/switch-mode",
            query=kwargs,
            auth=True
        )

    def get_trade_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/execution/list",
            query=kwargs,
            auth=True
        )

    def get_closed_profit_and_loss_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/position/closed-pnl",
            query=kwargs,
            auth=True
        )

    def get_usdc_options_settlement_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/delivery-record",
            query=kwargs,
            auth=True
        )

    def get_usdc_perpetuals_settlement_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/settlement-record",
            query=kwargs,
            auth=True
        )

    def get_wallet_balance(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/account/wallet/balance",
            query=kwargs,
            auth=True
        )

    def get_trading_fee_rate(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/account/fee-rate",
            query=kwargs,
            auth=True
        )

    def get_wallet_fund_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint +
                 "/unified/v3/private/account/wallet/fund-records",
            query=kwargs,
            auth=True
        )

    def get_transaction_log(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/account/transaction-log",
            query=kwargs,
            auth=True
        )

    def get_exchange_coins_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/asset/v2/private/exchange/exchange-order-all",
            query=kwargs,
            auth=True
        )

    def get_borrowing_history(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/account/borrow-history",
            query=kwargs,
            auth=True
        )

    def get_borrowing_rate(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/account/borrow-rate",
            query=kwargs,
            auth=True
        )

    def set_margin_mode(self, **kwargs):
        return self._submit_request(
            method="POST",
            path=self.endpoint + "/unified/v3/private/account/setMarginMode",
            query=kwargs,
            auth=True
        )

    def get_margin_mode(self, **kwargs):
        return self.get_account_info(**kwargs)

    def get_account_info(self, **kwargs):
        return self._submit_request(
            method="GET",
            path=self.endpoint + "/unified/v3/private/account/info",
            query=kwargs,
            auth=True
        )


class WebSocket(ContractWebSocket):
    @staticmethod
    def _determine_public_ws_connection(symbol):
        if _helpers.is_usdt_perpetual(symbol):
            return PUBLIC_USDT_WS
        elif _helpers.is_usdc_perpetual(symbol):
            return PUBLIC_USDC_PERPETUAL_WS
        elif _helpers.is_usdc_option(symbol):
            return PUBLIC_USDC_OPTIONS_WS

    def _ws_private_subscribe(self, topic, callback):
        if not self.ws_private:
            self.ws_private = \
                _V3WebSocketManager(ws_name, **self.args)
            self.ws_private._connect(PRIVATE_UNIFIED_MARGIN_WS)
            self.active_connections.append(self.ws_private)
        self.ws_private.subscribe(topic, callback)

    # Private topics
    def position_stream(self, callback):
        topic = "user.position.unifiedAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def execution_stream(self, callback):
        topic = "user.execution.unifiedAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def order_stream(self, callback):
        topic = "user.order.unifiedAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def wallet_stream(self, callback):
        topic = "user.wallet.unifiedAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def greeks_stream(self, callback):
        topic = "user.greeks.unifiedAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def account_info_stream(self, callback):
        topic = "user.info.unifiedAccount"
        self._ws_private_subscribe(topic=topic, callback=callback)
