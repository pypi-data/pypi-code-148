import pandas as pd

from trading_api import TradingOrders, TradingAccount
from market_data_api import MarketData

from trades import Trade
from portfolio import Portfolio
from indicators import Indicators


class PyRobot:

    def __init__(self, market_api_key: str, paper_trading_api_key: str) -> None:
        """ Initializes a new instance of the PyRobot object and logs into the API platform specified.

        Arguments:
        ----
        market_api_key {str} -- The Market API key assigned when you create an account on the Lemon Markets website.
        Can be found in the API Keys section under General once logged into your account.

        paper_trading_api_key {str} -- The Paper Trading API key assigned when you create an account on the Lemon
        Markets website. Can be found in the API Keys section under General once logged into your account.
        """

        # Initialize Supporting Objects
        self.portfolio = Portfolio(market_api_key=market_api_key, paper_trading_api_key=paper_trading_api_key)
        self.trade = Trade(paper_trading_api_key=paper_trading_api_key)
        self.indicators = Indicators(market_api_key=market_api_key, paper_trading_api_key=paper_trading_api_key)

        # Initialize API Objects
        self.trading_account_api = TradingAccount(paper_trading_api_key)
        self.trading_orders_api = TradingOrders(paper_trading_api_key)
        self.market_data_api = MarketData(market_api_key)

    @property
    def account_information(self) -> pd.Series:
        """ Displays user's account information.

        Returns:
        ----
        pd.Series -- A pandas Series with account information.
        For example:
        First Name                                           Hamza
        Last Name                                           Rashid
        Email                                   hamzu197@gmail.com
        Account Id          acc_qyPYZBBTTxKNwp1DNKGDbmxk51g8jhdY89
        Balance                                           59479.37
        Cash to Withdraw                                  59479.37
        Cash to Invest                                    59479.37
        Currency                                                 €
        """

        # API Call
        api_call_dict = self.trading_account_api.account_information_()

        # Create Series
        account_information = pd.Series([api_call_dict['results']['firstname'], api_call_dict['results']['lastname'],
                                         api_call_dict['results']['email'],
                                         api_call_dict['results']['account_id'],
                                         api_call_dict['results']['balance'] / 10000,
                                         api_call_dict['results']['cash_to_withdraw'] / 10000,
                                         api_call_dict['results']['cash_to_invest'] / 10000, '€'],
                                        index=['First Name', 'Last Name', 'Email', 'Account Id', 'Balance',
                                               'Cash to Withdraw', 'Cash to Invest', 'Currency'])

        return account_information

    def withdraw_money(self, amount):
        """ Withdraws money from the user's brokerage account and transfers it to the reference account.

        Arguments:
        ----
        amount {float} -- enter a float greater than 0 and less than 2499.99

        Returns:
        ----
        str -- A string indicating the remaining balance within the account. For example:

        ('Amount withdrawn, remaining balance', 59399.37)
        """

        amount *= 10000

        # API Call
        api_call_dict = self.trading_account_api.withdraw_money_(amount=amount)

        # Extracting error message from API Call dictionary
        if api_call_dict['status'] == 'error':
            return api_call_dict['error_message']

        return "Amount withdrawn, remaining balance", self.account_information['Balance']

    @property
    def withdrawal_information(self):
        """ Returns a history of the user's withdrawal information.

        Returns:
        ----
        pd.Dataframe -- A pandas Dataframe with withdrawal information sorted by creation date. For example:

                              Amount Execution Date                           Withdrawal ID
        Created at
        2022-11-22 21:15:23      0.5     2022-12-01  wtd_qyPdDTTffD610tHGqB8NMP1nzmzwxgQsp2
        2022-11-27 20:40:01  25000.0     2022-12-01  wtd_qyPkCzzDDXYyj4XG3fWKyKxjhQR9RDJpVM
        2022-11-28 21:36:43   5000.0     2022-12-01  wtd_qyPlDtt22nj3tn3J4R829nb5M6WrzW0bZs
        2022-12-02 20:05:39    100.0           None  wtd_qyQFCHHzzHn24VKxT2J0d4M4CB2VF4mTR0
        2022-12-02 20:05:49   1000.0           None  wtd_qyQFCHH99P5LblNz8TVbMcBlsRGnyKt4cb
        """

        # API Call
        api_call_dict = self.trading_account_api.retrieve_withdrawals()

        withdrawal_information = []

        # Store information into a List[List]
        for results_dict in api_call_dict['results']:
            withdrawal_information.append([results_dict['amount'] / 10000, results_dict['date'], results_dict['id'],
                                           results_dict['created_at']])

        # Create Pandas Dataframe
        withdrawal_information_df = pd.DataFrame(data=withdrawal_information,
                                                 columns=['Amount', 'Execution Date', 'Withdrawal ID', 'Created at'])

        # Modify Dataframe
        withdrawal_information_df = withdrawal_information_df.sort_values(['Created at'])
        withdrawal_information_df['Created at'] = withdrawal_information_df['Created at'].map(
            lambda x: x.replace('T', ' ')[:19])
        withdrawal_information_df = withdrawal_information_df.set_index(keys=['Created at'])

        return withdrawal_information_df

    def bank_statements(self, from_: str = 'beginning', to_: str = None):
        """ Returns a history of the user's account activity.

            Arguments:
            ----
            from_ {string} -- a starting date in the format 'YYYY-MM-DD'

            to_ {string} -- an ending date in the format 'YYYY-MM-DD'

            Returns:
            ----
            pd.Dataframe -- A pandas Dataframe with account activity information sorted by creation date. For example:

                                                         Quantity            ISIN Title                            ID
            Created at          Type
            2022-11-19 15:00:16 pay_in                        NaN                  None  bst_qyPYZBBWWMrhkCB0kkqpYP70...
                                eod_balance                   NaN                  None  bst_qyPYZBBWWRYK0gy6jlLmd4xM...
            2022-11-21 21:37:08 eod_balance                   NaN                  None  bst_qyPcDwwLLxG6qggTyJyZQ18F...
                                order_buy                    50.0  COINBASE GLOBAL INC.  bst_qyPcDwwLLPR4RrFbj5VBR6st...
                                order_buy                    50.0  COINBASE GLOBAL INC.  bst_qyPcDwwLLfVqZBDzXhpzcDLT...

                """

        # API Call
        api_call_dict = self.trading_account_api.bank_statements_(from_=from_, to_=to_)

        bank_statements_information = []

        # Store information into a List[List]
        for results_dict in api_call_dict['results']:
            bank_statements_information.append([results_dict['type'], results_dict['quantity'],
                                                results_dict['isin_title'], results_dict['id'], results_dict['date'],
                                                results_dict['created_at'], results_dict['amount']])

        # Create Pandas Dataframe
        bank_statements_df = pd.DataFrame(data=bank_statements_information,
                                          columns=['Type', 'Quantity', 'ISIN Title', 'ID', 'Date', 'Created at',
                                                   'Amount'])

        # Modify Dataframe
        bank_statements_df = bank_statements_df.sort_values(['Created at'])
        bank_statements_df['Created at'] = bank_statements_df['Created at'].map(lambda x: x.replace('T', ' ')[:19])
        bank_statements_df = bank_statements_df.set_index(keys=['Created at', 'Type'])

        return bank_statements_df

    def instrument_historical_prices(self, isin: str, unit: str, from_date: str, to_date: str):
        """ Returns historic market data in the Open High Low Close (OHLC) format  for an instrument.

        Arguments:
        ----
        isin {str} -- the International Securities Identification Number (ISIN) for an instrument

        unit {str} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {str} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {str} -- End of time range you want to get OHLC data for

        Returns:
        ----
        pd.Dataframe -- A pandas Dataframe with Open, Close, High, Low prices and Volume for an instrument. For example:

                                           Open  Close   High    Low  Volume
        ISIN         Date|Time
        US19260Q1076 2022-09-05|06:02:00  65.56  65.56  65.56  65.56       1
                     2022-09-05|07:08:00  65.59  65.59  65.59  65.59     382
                     2022-09-05|07:13:00  65.59  63.51  65.59  63.51       8
                     2022-09-05|07:33:00  63.89  63.89  63.89  63.89     392
                     2022-09-05|07:34:00  63.89  63.51  63.89  63.51     784
                     2022-09-05|07:43:00  64.06  64.06  64.06  64.06       0
                     2022-09-05|07:58:00  64.08  64.08  64.08  64.08       1
        """

        # Modifying variables
        from_date = from_date.format(' ', 'T')
        to_date = to_date.format(' ', 'T')

        # API Call
        api_call_dict = self.market_data_api.ohlc(isin=isin, x1=unit, from_=from_date, to_=to_date)

        if api_call_dict['status'] == 'error':
            return api_call_dict['error_message']

        instrument_historical_prices_information = []

        # Store information into a List[List]
        for results_dict in api_call_dict['results']:
            instrument_historical_prices_information.append([results_dict['t'], results_dict['o'], results_dict['c'],
                                                             results_dict['h'], results_dict['l'], results_dict['v'],
                                                             results_dict['isin'], results_dict['t']])

        # Create Pandas Dataframe
        instrument_historical_prices_df = pd.DataFrame(data=instrument_historical_prices_information,
                                                       columns=['Date|Time', 'Open', 'Close', 'High', 'Low', 'Volume',
                                                                'ISIN',
                                                                'Time'])

        # Modify Dataframe
        instrument_historical_prices_df = instrument_historical_prices_df.sort_values(['ISIN', 'Time'])
        instrument_historical_prices_df['Date|Time'] = instrument_historical_prices_df['Date|Time'].map(
            lambda x: x.replace('T', '|')[:19])
        instrument_historical_prices_df = instrument_historical_prices_df.set_index(keys=['ISIN', 'Date|Time'])
        instrument_historical_prices_df.drop(['Time'], axis=1, inplace=True)

        return instrument_historical_prices_df

    def instrument_quote(self, isin: str) -> pd.Series:
        """ Returns information about the price and trading volume of a specific instrument, how it is 'quoted' on
         an exchange.

        Arguments:
        ----
        isin {str} -- the International Securities Identification Number (ISIN) for an instrument.

        Returns:
        ----
        pd.Series -- A pandas Series with ISIN, ask price, ask volume, bid price and bid volume for an instrument.
        For example:

        ISIN          US19260Q1076
        Ask Price           45.325
        Ask Volume             553
        Bid Price            45.17
        Bid Volume             553
        """

        # API Call
        api_call_dict = self.market_data_api.quotes(isin=isin)

        # Creating a pandas Series
        instrument_quote_series = pd.Series([api_call_dict["results"][0]['isin'], api_call_dict["results"][0]['a'],
                                             api_call_dict["results"][0]['a_v'], api_call_dict["results"][0]['b'],
                                             api_call_dict["results"][0]['b_v']], index=
                                            ['ISIN', 'Ask Price', 'Ask Volume', 'Bid Price', 'Bid Volume'])

        return instrument_quote_series
