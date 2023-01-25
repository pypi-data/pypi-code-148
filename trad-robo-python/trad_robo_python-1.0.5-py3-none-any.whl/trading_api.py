import requests
import json

from typing import Optional


class TradingAccount:

    def __init__(self, trading_api_key: str) -> None:
        """ Initializes a new instance of the TradingAccount object.

        Arguments:
        ----
        trading_api_key {str} -- The Paper Trading API key assigned when you create an account on the Lemon Markets
        website. Can be found in the API Keys section under General once logged into your account.
        """

        self.trading_api_key: str = trading_api_key

    def account_information_(self) -> dict:
        """Retrieves all account information for the user.

        Returns:
        ----
        dict -- A dictionary containing the unique identification number for the account (account_id), firstname,
        lastname and other relevant information. For example:

        {
          "time": "2021-11-22T15:37:56.520+00:00",
          "status": "ok",
          "mode":"paper",
          "results": {
            "created_at": "2021-10-12T10:29:49.769+00:00",
            "account_id": "acc_pyNQNll99hQbXMCS0dRzHyKQCRKYHpy3zg",
            "firstname": "Michael",
            "lastname": "Burry",
            "email": "m_burry@tradingapi.com",
            "phone": "+491637876521",
            "address": "Ritterstraße 2A 10969 Berlin",
            "billing_address": "Ritterstraße 2A 10969 Berlin",
            "billing_email": "m_burry@tradingapi.com",
            "billing_name": "Michael Burry",
            "billing_vat": "DE999999999",
            "mode": "paper",
            "deposit_id": "K2057263187",
            "client_id": "2057263",
            "account_number": "2057263187",
            "iban_brokerage": "DE12345678902057263",
            "iban_origin": "DE123456789012345",
            "bank_name_origin": "Test Bank",
            "balance": 100000000,
            "cash_to_invest": 80000000,
            "cash_to_withdraw": 20000000,
            "amount_bought_intraday": 0,
            "amount_sold_intraday": 0,
            "amount_open_orders": 0,
            "amount_open_withdrawals": 1475200,
            "amount_estimate_taxes": 0,
            "approved_at": "2021-11-19T07:40:12.563+00:00",
            "trading_plan": "investor",
            "data_plan": "investor",
            "tax_allowance": 8010000,
            "tax_allowance_start": "2021-01-01",
            "tax_allowance_end": "2021-01-01"
          }
        }
        """

        # Get request
        request = requests.get("https://paper-trading.lemon.markets/v1/account",
                               headers={"Authorization": f"Bearer {self.trading_api_key}"})

        return request.json()

    def withdraw_money_(self, amount: int = 0) -> dict:
        """To request a withdrawal from your borkerage to your reference account.

        Arguments:
        ----
        amount {int} -- Using this request body parameter, you can specify the amount you wish to withdraw. Specify the
        amount in the format Int * 10000 (e.g., 1000000 to withdraw 100 €).

        Returns:
        ----
        dict -- A dictionary containing the timestamp of your request (time), status of your request (status) and
        environment the request was placed in: 'paper' or 'money' (mode). For Example:

        {
          "time": "2021-11-22T15:37:56.520+00:00",
          "mode":"paper",
          "status": "ok"
        }
        """

        # Post request
        request_withdraw = requests.post("https://paper-trading.lemon.markets/v1/account/withdrawals",
                                data=json.dumps({
                                    "amount": amount
                                }),
                                headers={"Authorization": f"Bearer {self.trading_api_key}"})

        return request_withdraw.json()

    def retrieve_withdrawals(self) -> dict:
        """To retrieve all information regarding withdrawals of the user.

        Returns:
        ----
        dict -- A dictionary containing the unique identification number of the withdrawal (id), amount specified for
        the withdrawal (amount), timestamp the withdrawal was created at (created_at), timestamp the withdrawal was
        processed by the partner bank (date) and unique idempotency key specified in POST request to prevent duplicate
        withdrawals (idempotency). For example:

        {
          "time": "2021-12-15T11:21:21.023+00:00",
          "status": "ok",
          "mode":"paper",
          "results": [
            {
              "id": "wtd_pyQTPbbLLMNBQTM0mzkK7Ygb8kH60Ff10X",
              "amount": 1000000,
              "created_at": "2021-12-15T11:21:05.853+00:00",
              "date": "2021-12-15T25:12:02.765+00:00",
              "idempotency": "1234abcd"
            },
            {
              ...
            }
          ],
          "previous": "https://paper-trading.lemon.markets/v1/account/withdrawals?limit=20&page=1",
          "next": "https://paper-trading.lemon.markets/v1/account/withdrawals?limit=2&page=3",
          "total": 80,
          "page": 2,
          "pages": 4
        }
        """

        # Get request
        request = requests.get("https://paper-trading.lemon.markets/v1/account/withdrawals",
                               headers={"Authorization": f"Bearer {self.trading_api_key}"})

        return request.json()

    def bank_statements_(self,from_: str = 'beginning', to_ = None) -> dict:
        """Returns a list of objects containing all activities from the last "active day" (in the paper money
        environment) and all activities from the last working day (in the real money environment).

         Arguments:
        ----
        from_ {str} -- Filter for bank statements after a specific date. Format: "YYYY-MM-DD". If you set
        from=beginning, you can conveniently retrieve all bank statements since your account opening.

        to_ {str} -- Filter for bank statements until a specific date. Format: "YYYY-MM-DD".

        Returns:
        ----
        dict -- A dictionary containing the unique identification number of your bank statement (id), unique
        identification number of the account the bank statement is related to (account_id), type of bank statement
        (type), date of bank statement (date), amount associated with bank statement (amount), the International
        Securities Identification Number (ISIN) related to your bank statement (isin_title) and the timestamp the bank
        statement was created internally (created_at). For example:

        {
          "time": "2021-11-22T15:41:04.028+00:00",
          "status": "ok",
          "mode": "paper",
          "results": [
            {
              "id": "bst_pyQKKTTSS0Q2drg2J7yRhTwBkMPd1JgZzZ",
              "account_id": "acc_pyNQNll99hQbXMCS0dRzHyKQCRKYHpy3zg",
              "type": "order_buy",
              "date": "2021-12-16",
              "amount": 100000,
              "isin": "US19260Q1076",
              "isin_title": "COINBASE GLOBAL INC.",
              "created_at": "2021-12-17T01:37:03.362+00:00"
            },
            {
              ...
            }
          ],
          "previous": "https://paper-trading.lemon.markets/v1/account/bankstatements?limit=20&page=1",
          "next": "https://paper-trading.lemon.markets/v1/account/bankstatements?limit=2&page=3",
          "total": 80,
          "page": 2,
          "pages": 4
        }
        """

        # Request URL
        if to_ is None:
            request_url = "https://paper-trading.lemon.markets/v1/account/bankstatements/?from={from_}".\
                format(from_=from_)
        else:
            request_url = "https://paper-trading.lemon.markets/v1/account/bankstatements/?from={from_}&to={to_}".\
                format(from_=from_,to_=to_)

        # Get request
        request = requests.get(request_url,headers = {"Authorization": f"Bearer {self.trading_api_key}"})

        return request.json()

class TradingOrders:

    def __init__(self, trading_api_key: str) -> None:
        """ Initializes a new instance of the TradingOrders object.

        Arguments:
        ----
        trading_api_key {str} -- The Paper Trading API key assigned when you create an account on the Lemon Markets
        website. Can be found in the API Keys section under General once logged into your account.
        """

        self.trading_api_key: str = trading_api_key

    def place_order(self, isin: str, side: str, quantity: int, expires_at: Optional[str], stop_price: Optional[int],
                  limit_price: Optional[int]) -> dict:
        """Request to place an order for an instrument.

         Arguments:
        ----
        isin {str} -- the International Security Identification Number that uniquely identifies the instrument you wish
        to buy or sell.

        side {str} -- attribute to define whether you want to buy or sell a specific instrument.

        quantity {int} -- to define the number of shares you want to buy. This is limited to 25,000€ estimated order
        price per request.

        expires_at {str} -- to specify the expiry date. By default, the order expires at the end of the specified day.
        The Maximum expiration date is 30 days in the future.

        stop_price {int} -- to define a Stop Price for your Order.

        limit_price {int} -- to define a Limit Price for your Order.

        Returns:
        ----
        dict -- A dictionary containing the order infomration. For example:

        {
          "time":"2021-11-21T19:34:45.071+00:00",
          "status": "ok",
          "mode":"paper",
          "results": {
            "created_at": "2021-11-15T13:58:19.981+00:00",
            "id": "ord_pyPGQggmmj0jhlLHw2nfM92Hm9PmgTYq9K",
            "status": "inactive",
            "regulatory_information": {
              "costs_entry": 20000,
              "costs_entry_pct": "0.30%",
              "costs_running": 0,
              "costs_running_pct": "0.00%",
              "costs_product": 0,
              "costs_product_pct": "0.00%",
              "costs_exit": 20000,
              "costs_exit_pct": "0.30%",
              "yield_reduction_year": 20000,
              "yield_reduction_year_pct": "0.30%",
              "yield_reduction_year_following": 0,
              "yield_reduction_year_following_pct": "0.00%",
              "yield_reduction_year_exit": 20000,
              "yield_reduction_year_exit_pct": "0.30%",
              "estimated_holding_duration_years": "5",
              "estimated_yield_reduction_total": 40000,
              "estimated_yield_reduction_total_pct": "0.61%",
              "KIID": "text",
              "legal_disclaimer": "text"
            },
            "isin": "DE0008232125",
            "expires_at": "2021-11-07T22:59:00.000+00:00",
            "side": "buy",
            "quantity": 1,
            "stop_price": null,
            "limit_price": null,
            "venue": "xmun",
            "estimated_price": 66140000,
            "notes": "I want to attach a note to this order",
            "idempotency": "1234abcd",
            "charge": 20000,
            "chargeable_at": "2021-12-10T07:57:12.628+00:00",
            "key_creation_id": "apk_pyJKKbbDDNympXsVwZzPp2nBVlTMTLRmxy"
          }
        }
        """

        # Post request
        request = requests.post("https://paper-trading.lemon.markets/v1/orders",
                                data=json.dumps({
                                    "isin": isin,
                                    "side": side,
                                    "quantity": quantity,
                                    "expires_at": expires_at,
                                    "stop_price": stop_price,
                                    "limit_price": limit_price
                                }),
                                headers={"Authorization": f"Bearer {self.trading_api_key}"})
        return request.json()

    def activate_order(self, order_id: str) -> dict:
        """To activate an order.

        Arguments:
        ----
        order_id {str} -- the id of the order you want to activate.

        Returns:
        ----
        dict -- A dictionary containing information regarding order activation. For example:

        {
          "time":"2021-11-21T19:34:45.071+00:00",
          "mode":"paper",
          "status": "ok"
        }
        """

        # Post request
        request = requests.post("https://paper-trading.lemon.markets/v1/orders/{order_id}/activate".
                                format(order_id=order_id),
                               data=json.dumps({
                                   "pin": "7652"
                               }),
                               headers={"Authorization": f"Bearer {self.trading_api_key}"})
        return request.json()

    def retrieve_orders(self) -> dict:
        """ To retrieve previous and current order information.

        Returns:
        ----
        dict -- A dictionary containing order information. For example:

        {
          "time":"2021-11-21T19:34:45.071+00:00",
          "status": "ok",
          "mode":"paper",
          "results":
          [
            {
              "id": "ord_pyPGQhhllz0mypLHw2nfM67Gm9PmgTYq0J",
              "isin": "DE0008232125",
              "isin_title": "DEUTSCHE LUFTHANSA AG",
              "expires_at": "2021-11-07T22:59:00.000+00:00",
              "created_at": "2021-11-04T12:25:30.063+00:00",
              "side": "buy",
              "quantity": 1000,
              "stop_price": null,
              "limit_price": null,
              "estimated_price": 66140000,
              "estimated_price_total": 66140000,
              "venue": "xmun",
              "status": "inactive",
              "type": "market",
              "executed_quantity": 1,
              "executed_price": 2965000,
              "executed_price_total": 2965000,
              "executed_at": "2021-11-04T12:25:12.402+00:00",
              "rejected_at": null,
              "notes": "My Notes",
              "charge": 20000,
              "chargeable_at": "2021-12-10T07:57:12.628+00:00",
              "key_creation_id": "apk_pyJHHbbDDNympXsVwZzPp2nNBlTMTLRmxy",
              "key_activation_id": "apk_pyJHHbbDDNympXsVwZzPp2nNBlTMTLRmxy",
              "regulatory_information": {
                  "costs_entry": 20000,
                  "costs_entry_pct": "0.30%",
                  "costs_running": 0,
                  "costs_running_pct": "0.00%",
                  "costs_product": 0,
                  "costs_product_pct": "0.00%",
                  "costs_exit": 20000,
                  "costs_exit_pct": "0.30%",
                  "yield_reduction_year": 20000,
                  "yield_reduction_year_pct": "0.30%",
                  "yield_reduction_year_following": 0,
                  "yield_reduction_year_following_pct": "0.00%",
                  "yield_reduction_year_exit": 20000,
                  "yield_reduction_year_exit_pct": "0.30%",
                  "estimated_holding_duration_years": "5",
                  "estimated_yield_reduction_total": 40000,
                  "estimated_yield_reduction_total_pct": "0.61%",
                  "KIID": "text",
                  "legal_disclaimer": "text"
              },
              "idempotency": "1235abcd"
            }
          ],
          "previous": "https://paper-trading.lemon.markets/v1/orders?limit=10&page=1",
          "next": "https://paper-trading.lemon.markets/v1/orders?limit=10&page=3",
          "total": 33,
          "page": 2,
          "pages": 4
        }
        """

        # Get request
        request = requests.get("https://paper-trading.lemon.markets/v1/orders",
                               headers={"Authorization": f"Bearer {self.trading_api_key}"})

        return request.json()

    def cancel_order(self, order_id: str) -> dict:
        """A delete request to cancel an inactive or activated order.

        Arguments:
        ----
        order_id {str} -- the id of the order you want to cancel.

        Returns:
        ----
        dict -- A dictionary containing cancellation status. For example:

        {
          "time":"2021-11-21T19:34:45.071+00:00",
          "status": "ok",
          "mode":"paper"
        }
        """

        # Delete request
        request = requests.delete("https://paper-trading.lemon.markets/v1/orders/{order_id}".format(order_id=order_id),
                                  headers={"Authorization": f"Bearer {self.trading_api_key}"})
        return request.json()

class TradingPositions:

    def __init__(self, trading_api_key: str) -> None:
        """ Initializes a new instance of the TradingOrders object.

        Arguments:
        ----
        trading_api_key {str} -- The Paper Trading API key assigned when you create an account on the Lemon Markets
        website. Can be found in the API Keys section under General once logged into your account.
        """

        self.trading_api_key: str = trading_api_key

    def positions(self) -> dict:
        """Retrieves current positions in portfolio.

        Returns:
        ----
        dict -- A dictionary containing information regarding positions. For example:

        {
          "time":"2021-11-21T19:34:45.071+00:00",
          "status": "ok",
          "mode":"paper",
          "results": [
            {
              "isin": "US19260Q1076",
              "isin_title": "COINBASE GLOBAL INC.",
              "quantity": 2,
              "buy_price_avg": 2965000,
              "estimated_price_total": 5800000,
              "estimated_price": 2900000
            },
            {
              "isin": "US19260Q1076",
              ...
            }
          ],
          "previous": "https://paper-trading.lemon.markets/v1/positions?limit=10&page=1",
          "next": "https://paper-trading.lemon.markets/v1/positions?limit=10&page=3",
          "total": 33,
          "page": 2,
          "pages": 4
        }
        """

        # Positions request
        request = requests.get("https://paper-trading.lemon.markets/v1/positions",
                                  headers={"Authorization": f"Bearer {self.trading_api_key}"})
        return request.json()










