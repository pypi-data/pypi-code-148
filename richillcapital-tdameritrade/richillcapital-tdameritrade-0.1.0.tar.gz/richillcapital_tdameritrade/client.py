
from typing import List

import requests

from richillcapital_tdameritrade.models import (
    Candle,
    Quote,
    Instrument
)

class TDAmeritradeClient:
    """
    TD Ameritrade API Client
    """
    BASE_ADDRESS = "https://api.tdameritrade.com"

    def __init__(self, apiKey: str) -> None:
        self._apiKey = apiKey

    def post_access_token(self):
        """
        The token endpoint returns an access token along with an optional refresh token.
        """
        raise NotImplementedError()

    def get_account(self):
        """ 
        Account balances, positions, and orders for a specific account.
        """
        raise NotImplementedError()

        
    def get_accounts(self):
        """ 
        Account balances, positions, and orders for all linked accounts.
        """
        raise NotImplementedError()
        
    def cancel_order(self):
        """ 
        Cancel a specific order for a specific account.   
        Order throttle limits may apply.  
        """
        raise NotImplementedError()

    def get_order(self):
        """ 
        Get a specific order for a specific account.
        """
        raise NotImplementedError()
        
    def get_orders_by_path(self):
        """ 
        Orders for a specific account.
        """
        raise NotImplementedError()
        
    def get_orders_by_query(self):
        """
        All orders for a specific account or, if account ID isn't specified, orders will be returned for all linked accounts.
        """
        raise NotImplementedError()

    def place_order(self):
        """ 
        Place an order for a specific account.   Order throttle limits may apply.  
        """
        raise NotImplementedError()
        
    def replace_order(self):
        """ 
        eplace an existing order for an account. The existing order will be replaced by the new order. 
        Once replaced, the old order will be canceled and a new order will be created.   
        Order throttle limits may apply
        """
        raise NotImplementedError()
        
    def create_saved_order(self):
        """ 
        Save an order for a specific account. 
        """
        raise NotImplementedError()
        
    def delete_saved_order(self):
        """ 
        Delete a specific saved order for a specific account.
        """
        raise NotImplementedError()

    def get_saved_order(self):
        """ 
        Specific saved order by its ID, for a specific account.
        """
        raise NotImplementedError()
   
    def get_saved_order_by_path(self):
        """ 
        Saved orders for a specific account.
        """
        raise NotImplementedError()
   
    def replace_saved_order(self):
        """ 
        Replace an existing saved order for an account. The existing saved order will be replaced by the new order. 
        """
        raise NotImplementedError()

    def get_price_history_daily(self, symbol: str) -> List[Candle]:
        """
        Get daily price history for a symbol.
        """
        endpoint = f"/v1/marketdata/{symbol}/pricehistory"
        parameters = {
            "apikey": self._apiKey,
            "frequency": 1, 
            "frequencyType": "daily",
            "periodType": "ytd",
        }

        url = self.BASE_ADDRESS + endpoint
        response = requests.get(url, params = parameters)

        json_data: dict = response.json()
        
        empty: bool = json_data.get("empty", str())
        candles_data: List[dict] = json_data.get("candles", list())

        return [
            Candle(
                    json_data.get("symbol", str()), 
                    data.get("datetime", 0),
                    data.get("open", 0.0),
                    data.get("high", 0.0),
                    data.get("low", 0.0),
                    data.get("close", 0.0),
                    data.get("volume", 0),
                )
            for data in candles_data
        ]

    def get_quote(self, symbol: str) -> Quote:
        """
        Get quote for a symbol.
        """
        endpoint = f"/v1/marketdata/{symbol}/quotes"

        url = self.BASE_ADDRESS + endpoint
        response = requests.get(url, params = self._get_default_query_parameters())
        
        json_data: dict = response.json()[symbol]

        symbol = json_data.get("symbol", "")
        description = json_data.get("description", "")
        asset_type = json_data.get("assetType", "")
        asset_main_type = json_data.get("assetMainType", "")
        asset_sub_type = json_data.get("assetSubType", "")
        cusip = json_data.get("cusip", "")

        bid_price = json_data.get("bidPrice", "")
        bid_size = json_data.get("bidSize", "")
        bid_id = json_data.get("bidId", "")
        ask_price = json_data.get("askPrice", "")
        ask_size = json_data.get("askSize", "")
        ask_id = json_data.get("askId", "")
        last_price = json_data.get("lastPrice", "")
        last_size = json_data.get("lastSize", "")
        last_id = json_data.get("lastId", "")
        open_price = json_data.get("openPrice", "")
        high_price = json_data.get("highPrice", "")
        low_price = json_data.get("lowPrice", "")
        close_price = json_data.get("closePrice", "")
        bid_tick = json_data.get("bidTick", "")
        net_change = json_data.get("netChange", "")
        total_volume = json_data.get("totalVolume", "")
        
        quote_time_in_long = json_data.get("quoteTimeInLong", "")
        trade_time_in_long = json_data.get("tradeTimeInLong", "")
        mark = json_data.get("mark", "")
        exchange = json_data.get("exchange", "")
        exchange_name = json_data.get("exchangeName", "")
      
        marginable = json_data.get("marginable", "")
        shortable = json_data.get("shortable", "")
        volatility = json_data.get("volatility", "")
        digits = json_data.get("digits", "")

        regular_market_last_size = json_data.get("regularMarketLastSize", "")
        regular_market_net_change = json_data.get("regularMarketNetChange", "")
        regular_market_trade_time_in_long = json_data.get("regularMarketTradeTimeInLong", "")

        net_percent_change_in_double = json_data.get("netPercentChangeInDouble", "")
        mark_change_in_double = json_data.get("markChangeInDouble", "")
        mark_percent_change_in_double = json_data.get("markPercentChangeInDouble", "")
        regular_market_pcerent_change_in_double = json_data.get("regularMarketPercentChangeInDouble", "")
        delayed = json_data.get("delayed", False)
        realtime_entitled = json_data.get("realtimeEntitled", "")

        return Quote()

    def get_quotes(self, symbols: List[str]):
        """
        Get quote for one or more symbols.
        """
        raise NotImplementedError("Not implemented. get_quotes()")

    def get_market_hours(self, market_type):
        """
        Retrieve market hours for specified single market.
        """
        raise NotImplementedError()

    def get_market_hours_multi(self):
        """
        Retrieve market hours for specified markets
        """
        raise NotImplementedError()
    
    def search_instruments(self, symbol: str) -> Instrument:
        """
        Search or retrieve instrument data, including fundamental data.
        """
        endpoint = "/v1/instruments"

        parameters = {
            "apikey": self._apiKey,
            "symbol": symbol,
            "projection": "symbol-search"
        }

        url = self.BASE_ADDRESS + endpoint
        response = requests.get(url, params = parameters)


        json_data: dict = response.json()[symbol]

        cusip = json_data.get("cusip", "")
        symbol = json_data.get("symbol", "")
        description = json_data.get("description", "")
        exchange = json_data.get("exchange", "")
        asset_type = json_data.get("assetType", "")

        return Instrument(
            symbol,
            description,
            exchange,
            asset_type,
            cusip
        )

    def get_instrument(self, cusip: str):
        """
        Get an instrument by CUSIP.
        """
        endpoint = f"/v1/instruments/{cusip}"

        url = self.BASE_ADDRESS + endpoint
        response = requests.get(url, params = self._get_default_query_parameters())

        print(response.json())

    def get_transaction(self):
        """
        Transaction for a specific account.
        """
        raise NotImplementedError()

    def get_transactions(self):
        """
        Transactions for a specific account.
        """
        raise NotImplementedError()

    def get_option_chain(self):
        """
        Get option chain for an optionable Symbol
        """
        raise NotImplementedError()

    def get_movers(self):
        """
        Top 10 (up or down) movers by value or percent for a particular market
        """
        raise NotImplementedError()

    def create_watchlist(self, account_id: str):
        """
        Create watchlist for specific account.This method does not verify that the symbol or asset type are valid.
        """
        endpoint = f"/v1/accounts/{account_id}/watchlists"        
        raise NotImplementedError()

    def delete_watchlist(self, account_id: str, watchlist_id: str):
        """
        Delete watchlist for a specific account.
        """
        endpoint = f"v1/accounts/{account_id}/watchlists/{watchlist_id}"
        raise NotImplementedError()

    def get_watchlist(self):
        raise NotImplementedError()
        
    def get_watchlists(self):
        raise NotImplementedError()
        
    def replace_watchlist(self):
        raise NotImplementedError()
        
    def update_watchlist(self):
        raise NotImplementedError()

    def get_preferences(self):
        """
        Preferences for a specific account.
        """
        raise NotImplementedError()

    def get_streamer_subscription_keys(self):
        """
        SubscriptionKey for provided accounts or default accounts.
        """
        raise NotImplementedError()

    def get_user_principals(self):
        """
        User Principal details.
        """
        raise NotImplementedError()

    def update_preferences(self):
        """
        Update preferences for a specific account. 
        Please note that the directOptionsRouting and directEquityRouting values cannot be modified via this operation.
        """
        raise NotImplementedError()

    def _get_default_query_parameters(self) -> dict:
        return {
            "apikey": self._apiKey
        }