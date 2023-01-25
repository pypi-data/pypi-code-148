from typing import Optional

from trading_api import TradingOrders

import pandas as pd


class Trade:

    def __init__(self, paper_trading_api_key: str) -> None:
        """ Initializes a new instance of the Trade object.

        Arguments:
        ----
        paper_trading_api_key {str} -- The Paper Trading API key assigned when you create an account on the Lemon
        Markets website. Can be found in the API Keys section under General once logged into your account.
        """
        self.trading_orders_api = TradingOrders(paper_trading_api_key)

    def new_order(self, isin: str, side: str, quantity: int, expires_at: Optional[str] = None,
                  stop_price: Optional[int] = None,
                  limit_price: Optional[int] = None) -> pd.Series:
        """ Places a new order on the exchange.

            Able to place four types orders:

            1) Market Order
            2) Stop Price Order: enter stop_price argument
            3) Limit Price Order: enter limit_price argument
            4) Stop Limit Price Order: enter stop_price and limit_price

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        side {string} -- to define whether you want to buy ('buy') or sell ('sell') a specific instrument.

        quantity {int} -- the number of shares you want to buy. This is limited to 25,000€ estimated
        order price per request.

        expires_at {str} -- The order expires at the end of the specified day. The Maximum expiration date
        entered can be 30 days in the future. Format 'YYYY-MM-DD'.

        stop_price {int} -- the stop price for the instrument.

        limit_price {int} -- the limit price for the instrument.

        Returns:
        ----
        pd.Series -- A pandas series with order type, quantity, side and expiration date information. For example:

        For example:
        Order Type                Market Order
        Quantity                             2
        Side                               buy
        Expiration Date    2022-12-06 17:59:00
        """

        # Modifying input values
        if stop_price:
            stop_price *= 10000

        if limit_price:
            limit_price *= 10000

        # API Call
        api_call_dict = self.trading_orders_api.place_order(isin=isin, side=side, quantity=quantity,
                                                            expires_at=expires_at,
                                                            stop_price=stop_price, limit_price=limit_price)

        # Error Message
        if api_call_dict['status'] == 'error':
            return api_call_dict['error_message']

        # Updating Order Type and Price
        order_type = 'Market Order'

        if api_call_dict['results']['limit_price'] is not None:
            order_type = 'Limit Price Order'
            api_call_dict['results']['limit_price'] /= 10000

        if api_call_dict['results']['stop_price'] is not None:
            order_type = 'Stop Price Order'
            api_call_dict['results']['stop_price'] /= 10000

        if api_call_dict['results']['stop_price'] is not None and api_call_dict['results']['limit_price'] is not None:
            order_type = 'Stop Limit Price Order'
            api_call_dict['results']['stop_price'] /= 10000
            api_call_dict['results']['limit_price'] /= 10000

        # Create Series
        new_order_series = pd.Series([order_type, api_call_dict['results']['quantity'],
                                      api_call_dict['results']['side'], api_call_dict['results']['expires_at']], index=
                                     ['Order Type', 'Quantity', 'Side', 'Expiration Date'])

        new_order_series['Expiration Date'] = new_order_series['Expiration Date'].replace('T', ' ')[:19]

        return new_order_series

    def activate_order(self, order_id: str):
        """Activates an order after its placed.

        Arguments:
        ----
        order_id {string} -- the id of the order you want to activate.

        Returns:
        ----
        string -- A message indicating a order has been placed or an error message.
        For example:

        'Order successfully activated.'

        "Can only activate order in status 'inactive'"
        """

        # API Call
        api_call_dict = self.trading_orders_api.activate_order(order_id=order_id)

        if api_call_dict['status'] == 'ok':
            return 'Order successfully activated.'

        return api_call_dict['error_message']

    @property
    def retrieve_orders(self):
        """ Retrieve previous and current order information.

        Returns:
        ----
        pd.Dataframe -- A pandas Dataframe with ISIN, order ID, ISIN Title, Status, Expiration Date, Side, Quantity,
        Stop Price and Limit Price information.
        For example:
                                                                     ISIN Title     Status      Expiration Date  Side
        ISIN         Order ID
        US19260Q1076 ord_qyPZDFF66n8P59W6Xhmft1TD50sxfHQ0R  COINBASE GLOBAL INC.  executed  2022-11-21 17:59:00   buy...
                     ord_qyPZDddYYK7dDg4HQ9GXyGScCpfF1ZxMc  COINBASE GLOBAL INC.  executed  2022-11-21 17:59:00   buy...
        CA88162R1091 ord_qyPfCjjJJWPzFxRyK5pKkRVMymDk7BxnH            TESLA INC.   expired  2022-11-25 17:59:00   buy...
        US19260Q1076 ord_qyPlZXXGGZPjBH5th91zJp5HPgqyVZX0Y  COINBASE GLOBAL INC.   expired  2022-11-30 17:59:00   buy...
                     ord_qyPmDQQmmGrXMVnjzR5zGglHnFdnNBqFP  COINBASE GLOBAL INC.   expired  2022-12-01 17:59:00  sell...
                     ord_qyPmDXXxx6VgYVbt7sMMfB0x4ZMsh6LPH  COINBASE GLOBAL INC.   expired  2022-12-01 17:59:00   buy...
                     ord_qyPmDZZNNQchqg9gWMrpFPwKNHbjrb2Bp  COINBASE GLOBAL INC.   expired  2022-12-01 17:59:00  sell...
        """

        # API Call
        api_call_dict = self.trading_orders_api.retrieve_orders()

        retrieve_orders_information = []

        # Store information into a List[List]
        for results_dict in api_call_dict['results']:
            retrieve_orders_information.append(
                [results_dict['id'], results_dict['isin'], results_dict['isin_title'], results_dict['status'],
                 results_dict['expires_at'], results_dict['side'], results_dict['quantity'],
                 results_dict['stop_price'], results_dict['limit_price']])

        # Create Pandas Dataframe
        retrieve_orders_information_df = pd.DataFrame(data=retrieve_orders_information,
                                                      columns=['Order ID', 'ISIN', 'ISIN Title', 'Status',
                                                               'Expiration Date', 'Side', 'Quantity',
                                                               'Stop Price', 'Limit Price'])

        # Modify Dataframe
        retrieve_orders_information_df = retrieve_orders_information_df.sort_values(['Expiration Date'])
        retrieve_orders_information_df['Expiration Date'] = retrieve_orders_information_df['Expiration Date'].map(
            lambda x: x.replace('T', ' ')[:19])
        retrieve_orders_information_df = retrieve_orders_information_df.set_index(keys=['ISIN', 'Order ID'])

        return retrieve_orders_information_df

    def cancel_order(self, order_id: str):
        """Cancels an order, only if it's 'inactive' or 'activated'.

        Arguments:
        ----
        order_id {string} -- the id of the order you want to cancel.

        Returns:
        ----
        str -- A message indicating a order has been cancelled or an error message.
        For example:

        'Order cancellation sent.'

        'Order in status canceled cannot be cancelled'
        """

        # API Call
        api_call_dict = self.trading_orders_api.cancel_order(order_id=order_id)

        if api_call_dict['status'] == 'ok':
            return 'Order cancellation sent.'

        return api_call_dict['error_message']
