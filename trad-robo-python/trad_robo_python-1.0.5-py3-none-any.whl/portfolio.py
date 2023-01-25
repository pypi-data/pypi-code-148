import pandas as pd

from market_data_api import MarketData
from trading_api import TradingOrders
from trading_api import TradingPositions


class Portfolio:

    def __init__(self, market_api_key: str, paper_trading_api_key: str) -> None:
        """ Initializes a new instance of the Portfolio object.

        Arguments:
        ----
        market_api_key {str} -- The Market API key assigned when you create an account on the Lemon Markets website.
        Can be found in the API Keys section under General once logged into your account.

        paper_trading_api_key {str} -- The Paper Trading API key assigned when you create an account on the Lemon
        Markets website. Can be found in the API Keys section under General once logged into your account.
        """

        # Initialize API objects
        self.orders_api = TradingOrders(paper_trading_api_key)
        self.positions_api = TradingPositions(paper_trading_api_key)
        self.market_data_api = MarketData(market_api_key)

        self.current_orders = self.orders_api.retrieve_orders()

    @property
    def portfolio_orders(self):
        """Returns position information for current instruments within portfolio.

        Returns:
        ----
        pd.Dataframe -- A pandas Dataframe with ID, ISIN, ISIN Title, Expires At, Created At, Side, Quantity, Stop Price
        , Limit Price, Order Type, Executed Total Price and Status information for current positions.
        For example:
                                                                       ISIN Title           Expires At...
        ID                                     ISIN
        ord_qyPZDFF66n8P59W6Xhmft1TD50sxfHQ0RS US19260Q1076  COINBASE GLOBAL INC.  2022-11-21 17:59:00...
        ord_qyPZDddYYK7dDg4HQ9GXyGScCpfF1ZxMcY US19260Q1076  COINBASE GLOBAL INC.  2022-11-21 17:59:00...
        ord_qyPfCjjJJWPzFxRyK5pKkRVMymDk7BxnHW CA88162R1091            TESLA INC.  2022-11-25 17:59:00...
        ord_qyPlZXXGGZPjBH5th91zJp5HPgqyVZX0Yc US19260Q1076  COINBASE GLOBAL INC.  2022-11-30 17:59:00...
        ord_qyPmDQQmmGrXMVnjzR5zGglHnFdnNBqFPM US19260Q1076  COINBASE GLOBAL INC.  2022-12-01 17:59:00...
        """

        # API Call
        api_call_dict = self.orders_api.retrieve_orders()

        # Collect information
        current_instrument_positions_information = []

        for results_dict in api_call_dict['results']:

            if results_dict['stop_price'] is not None and results_dict['limit_price'] is not None:
                order_type = 'Stop Limit'
                results_dict['stop_price'] /= 10000
                results_dict['limit_price'] /= 10000
            elif results_dict['stop_price'] is not None:
                order_type = 'Stop Price'
                results_dict['stop_price'] /= 10000
            elif results_dict['limit_price'] is not None:
                order_type = 'Limit Price'
                results_dict['limit_price'] /= 10000
            else:
                order_type = 'Market Order'

            current_instrument_positions_information.append(
                [results_dict["id"], results_dict["isin"], results_dict["isin_title"],
                 results_dict["expires_at"], results_dict["created_at"],
                 results_dict["side"], results_dict["quantity"],
                 results_dict["stop_price"], results_dict["limit_price"],
                 order_type,
                 results_dict["executed_price_total"] / 10000,
                 results_dict["status"]])

        # Create Pandas Dataframe
        current_instrument_positions_df = pd.DataFrame(data=current_instrument_positions_information,
                                                       columns=['ID', 'ISIN', 'ISIN Title', 'Expires At', 'Created At',
                                                                'Side',
                                                                'Quantity', 'Stop Price', 'Limit Price',
                                                                'Order Type',
                                                                'Executed Total Price', 'Status'])

        # Modify Dataframe
        current_instrument_positions_df = current_instrument_positions_df.sort_values(['Created At'])
        current_instrument_positions_df['Expires At'] = current_instrument_positions_df['Expires At'].map(
            lambda x: x.replace('T', ' ')[:19])
        current_instrument_positions_df['Created At'] = current_instrument_positions_df['Created At'].map(
            lambda x: x.replace('T', ' ')[:19])
        current_instrument_positions_df = current_instrument_positions_df.set_index(keys=['ID', 'ISIN'])

        return current_instrument_positions_df

    @property
    def current_instrument_quotes(self) -> pd.DataFrame:
        """ Returns information about the price and trading volume of portfolio instruments, how they are 'quoted'
        on an exchange.

        Returns:
        ----
        pd.Dataframe -- A pandas Dataframe with ISIN, ISIN Title, ask price, ask volume, bid price and bid volume for an
        instrument. For example:
                                                   Bid Volume  Ask Volume  Bid Price  Ask Price
        ISIN         ISIN Title
        CA88162R1091 TESLA INC.                    500         500         12.00      12.50
        US19260Q1076 COINBASE GLOBAL INC.          570         570         43.78      43.93
        """
        current_instruments_dict = {}
        current_instrument_quotes_information = []

        # API Call to collect information
        for order in self.orders_api.retrieve_orders()["results"]:

            if order["isin"] in current_instruments_dict:
                pass

            else:
                current_instruments_dict[order["isin"]] = order["isin"]

                # Quote Information
                current_quote = self.market_data_api.quotes(isin=order["isin"])

                current_instrument_quotes_information.append([order["isin"], order["isin_title"],
                                                              current_quote["results"][0]['b_v'],
                                                              current_quote["results"][0]['a_v'],
                                                              current_quote["results"][0]['b'],
                                                              current_quote["results"][0]['a']])

        # Create Pandas Dataframe
        current_instrument_quotes_df = pd.DataFrame(data=current_instrument_quotes_information,
                                                    columns=['ISIN', 'ISIN Title', 'Bid Volume',
                                                             'Ask Volume',
                                                             'Bid Price',
                                                             'Ask Price'])

        # Modify Dataframe
        current_instrument_quotes_df = current_instrument_quotes_df.sort_values(['ISIN'])
        current_instrument_quotes_df = current_instrument_quotes_df.set_index(keys=['ISIN', 'ISIN Title'])

        return current_instrument_quotes_df

    def current_instrument_historical_prices(self, unit: str, from_date: str, to_date: str):
        """ Returns historic market data in the Open High Low Close (OHLC) format  for instrument's within portfolio.

        Arguments:
        ----
        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for

        Returns:
        ----
        pd.Dataframe -- A pandas Dataframe with Open, Close, High, Low prices and Volume for instruments. For example:

                                           Open  Close   High    Low  Volume
        ISIN         Date|Time
        CA88162R1091 2022-09-05|06:02:00  20.00  20.00  20.00  20.00       0
                     2022-09-05|07:13:00  20.00  20.00  20.00  20.00       0
                     2022-09-05|07:43:00  20.00  20.00  20.00  20.00       0
                     2022-09-05|08:33:00  20.20  20.20  20.20  20.20       1
                     2022-09-05|09:43:00  20.20  20.20  20.20  20.20       0
                     2022-09-05|11:43:00  20.20  20.20  20.20  20.20       0
                     2022-09-05|13:43:00  20.20  20.20  20.20  20.20       0
                     2022-09-05|15:43:00  20.20  20.20  20.20  20.20       0
                     2022-09-05|17:43:00  20.20  20.20  20.20  20.20       0
        US19260Q1076 2022-09-05|06:02:00  65.56  65.56  65.56  65.56       1
                     2022-09-05|07:08:00  65.59  65.59  65.59  65.59     382
                     2022-09-05|07:13:00  65.59  63.51  65.59  63.51       8
                     2022-09-05|07:33:00  63.89  63.89  63.89  63.89     392
        """

        current_instruments_dict = {}

        # Collecting Unique ISIN's
        for order in self.orders_api.retrieve_orders()["results"]:

            if order["isin"] in current_instruments_dict:
                pass

            else:
                current_instruments_dict[order["isin"]] = order["isin"]

        # Modifying variables for the API call
        isin_lst = list(current_instruments_dict.keys())
        for i in range(len(isin_lst) - 1):
            isin_lst[i] = isin_lst[i] + ','
        isin = ''.join(isin_lst)

        from_date = from_date.format(' ', 'T')
        to_date = to_date.format(' ', 'T')

        # API Call
        api_call_dict = self.market_data_api.ohlc(isin=isin, x1=unit, from_=from_date, to_=to_date)

        # Error Message
        if api_call_dict['status'] == 'error':
            return api_call_dict['error_message']

        current_instrument_historical_prices_information = []

        # Store information into a List[List]
        for results_dict in api_call_dict['results']:
            current_instrument_historical_prices_information.append(
                [results_dict['t'], results_dict['o'], results_dict['c'],
                 results_dict['h'], results_dict['l'], results_dict['v'],
                 results_dict['isin'], results_dict['t']])

        # Create Pandas Dataframe
        current_instrument_historical_prices_df = pd.DataFrame(data=current_instrument_historical_prices_information,
                                                               columns=['Date|Time', 'Open', 'Close', 'High', 'Low',
                                                                        'Volume',
                                                                        'ISIN',
                                                                        'Time'])

        # Modify Dataframe
        current_instrument_historical_prices_df = current_instrument_historical_prices_df.sort_values(['ISIN', 'Time'])
        current_instrument_historical_prices_df['Date|Time'] = current_instrument_historical_prices_df['Date|Time'].map(
            lambda x: x.replace('T', '|')[:19])
        current_instrument_historical_prices_df = current_instrument_historical_prices_df.set_index(
            keys=['ISIN', 'Date|Time'])
        current_instrument_historical_prices_df.drop(['Time'], axis=1, inplace=True)

        return current_instrument_historical_prices_df

    @property
    def portfolio_metrics(self):
        """ Returns portfolio metrics regarding current open positions.

        Returns:
        ----
        pd.Dataframe -- A pandas with information such as Quantity, Profit/Loss, ISIN Title etc. For example:

                              Quantity  Buy Avg. Price  Buy Avg. Total Price  Estimated Price  Estimated Total Price...
        ISIN
        US30303M1027               2.0        126.2000                252.40           126.06                 252.12...
        US88160R1014               2.0        113.3200                226.64           113.80                 227.60...
        US19260Q1076             100.0         43.9843               4398.43            43.89                4389.00...
        Total                    104.0             NaN               4877.47              NaN                4868.72...
        """

        # API Call
        api_call_dict = self.positions_api.positions()

        # Store information into a List[List]
        portfolio_positions_information = []

        for results_dict in api_call_dict['results']:
            portfolio_positions_information.append(
                [results_dict['buy_price_avg'] / 10000, results_dict['estimated_price'] / 10000,
                 results_dict['estimated_price_total'] / 10000, results_dict['isin'], results_dict['isin_title'],
                 results_dict['quantity']])

        # Create Pandas Dataframe
        portfolio_positions_information_df = pd.DataFrame(data=portfolio_positions_information,
                                                          columns=['Buy Avg. Price', 'Estimated Price',
                                                                   'Estimated Total Price', 'ISIN', 'ISIN Title',
                                                                   'Quantity'])

        portfolio_positions_information_df = portfolio_positions_information_df.sort_values(['Quantity'])
        portfolio_positions_information_df = portfolio_positions_information_df.set_index(keys=['ISIN'])

        # Additional Fields
        portfolio_positions_information_df['Buy Avg. Total Price'] = \
            portfolio_positions_information_df['Buy Avg. Price'] * portfolio_positions_information_df['Quantity']
        portfolio_positions_information_df['Profit/Loss'] = portfolio_positions_information_df['Estimated Total Price'] \
                                                            - portfolio_positions_information_df['Buy Avg. Total Price']
        portfolio_positions_information_df['%'] = 100 * portfolio_positions_information_df['Profit/Loss'] \
                                                  / portfolio_positions_information_df['Buy Avg. Total Price']
        portfolio_positions_information_df['%'] = portfolio_positions_information_df['%'].round(decimals=2)
        portfolio_positions_information_df['Total'] = None
        portfolio_positions_information_df.loc['Total'] = pd.Series([portfolio_positions_information_df[
                                                                         'Quantity'].sum(),
                                                                     portfolio_positions_information_df[
                                                                         'Buy Avg. Total Price'].sum(),
                                                                     portfolio_positions_information_df[
                                                                         'Estimated Total Price'].sum(),
                                                                     portfolio_positions_information_df[
                                                                         'Profit/Loss'].sum(),
                                                                     100 * portfolio_positions_information_df[
                                                                         'Profit/Loss'].sum() \
                                                                     / portfolio_positions_information_df[
                                                                         'Buy Avg. Total Price'].sum()],
                                                                    index=['Quantity', 'Buy Avg. Total Price',
                                                                           'Estimated Total Price',
                                                                           'Profit/Loss', '%'])

        # Rearranging Columns
        cols = ['Quantity', 'Buy Avg. Price', 'Buy Avg. Total Price', 'Estimated Price', 'Estimated Total Price',
                'Profit/Loss', '%', 'ISIN Title']

        return portfolio_positions_information_df[cols]


