import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from market_data_api import MarketData
from trading_api import TradingOrders


class Indicators:

    def __init__(self, market_api_key: str, paper_trading_api_key: str) -> None:
        """ Initializes a new instance of the Indicators object.

        Arguments:
        ----
        market_api_key {str} -- The Market API key assigned when you create an account on the Lemon Markets website.
        Can be found in the API Keys section under General once logged into your account.

        paper_trading_api_key {str} -- The Paper Trading API key assigned when you create an account on the Lemon
        Markets website. Can be found in the API Keys section under General once logged into your account.
        """

        # Initialize API objects
        self.orders_api = TradingOrders(paper_trading_api_key)
        self.market_data_api = MarketData(market_api_key)

        self.current_orders = self.orders_api.retrieve_orders()

    def _instrument_historical_prices(self, isin: str, unit: str, from_date: str, to_date: str):
        """ Returns historic market data in the Open High Low Close (OHLC) format  for an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for

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

        # Create pandas Dataframe
        instrument_historical_prices_df = pd.DataFrame(data=instrument_historical_prices_information,
                                                       columns=['Date|Time', 'Open', 'Close', 'High', 'Low', 'Volume',
                                                                'ISIN',
                                                                'Time'])

        # Modify Dataframe
        instrument_historical_prices_df = instrument_historical_prices_df.sort_values(['ISIN', 'Time'])
        instrument_historical_prices_df['Date|Time'] = instrument_historical_prices_df['Date|Time'].map(
            lambda x: x.replace('T', '|')[:19])
        instrument_historical_prices_df = instrument_historical_prices_df.set_index(keys=['Date|Time'])
        instrument_historical_prices_df.drop(['Time'], axis=1, inplace=True)

        return instrument_historical_prices_df

    def change_in_price(self, isin: str, unit: str, from_date: str, to_date: str) -> plt.plot:
        """ Returns a bar chart for the change in price of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for

        Returns:
        ----
        plt.plot -- A bar graph with two bars (Close Price, Change in Price) based on the chosen time horizon
        """

        # API Call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Creating Change in Price column
        historical_price_df['Change in Price'] = historical_price_df['Close']. \
            transform(lambda x: x.diff())

        # Dropping unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN'], axis=1, inplace=True)

        # Plotting DataFrame
        historical_price_df.plot(y=["Close", "Change in Price"], kind="bar", figsize=(15, 15), ylabel='Price',
                                 title=isin + ' - Change in Price')
        plt.show()

    def sma(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Simple Moving Average of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating sma.

        Returns:
        ----
        plt.plot -- A line graph with two lines (Close Price, Simple Moving Average) based on the chosen time horizon
        """

        # API call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Creating Simple Moving Average Column
        historical_price_df['Simple Moving Average'] = historical_price_df['Close']. \
            transform(lambda x: x.rolling(window=period).mean())

        # Drop unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN'], axis=1, inplace=True)

        # Plot DataFrame
        historical_price_df.plot(y=["Close", "Simple Moving Average"], kind="line", figsize=(10, 10), ylabel='Price',
                                 title=isin + ' - Simple Moving Average')
        plt.show()

    def ema(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Exponential Moving Average of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating ema.

        Returns:
        ----
        plt.plot -- A line graph with two lines (Close Price, Exponential Moving Average) based on the chosen time
        horizon
        """

        # API Call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Creating Exponential Moving Average column
        historical_price_df['Exponential Moving Average'] = historical_price_df['Close']. \
            transform(lambda x: x.ewm(span=period).mean())

        # Dropping unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN'], axis=1, inplace=True)

        # Plotting Dataframe
        historical_price_df.plot(y=["Close", "Exponential Moving Average"], kind="line", figsize=(10, 10),
                                 ylabel='Price',
                                 title=isin + ' - Exponential Moving Average')
        plt.show()

    def rsi(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Relative Strength Index of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for

        period {int} -- number of periods to use when calculating rsi.

        Returns:
        ----
        plt.plot -- Two graphs vertically stacked, the top for Price and bottom for RSI based on the chosen time horizon
        """

        # API Call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Change in Price column
        historical_price_df['change_in_price'] = historical_price_df['Close'].transform(lambda x: x.diff())
        historical_price_df['change_in_price'].replace(to_replace=np.nan, value=0, inplace=True)

        # Define the up days.
        historical_price_df['up_day'] = historical_price_df['change_in_price'].transform(
            lambda x: np.where(x >= 0, x, 0))

        # Define the down days.
        historical_price_df['down_day'] = historical_price_df['change_in_price'].transform(
            lambda x: np.where(x < 0, abs(x), 0))

        # Calculate the EWMA for the Up days.
        historical_price_df['ewma_up'] = historical_price_df['up_day'].transform(
            lambda x: x.ewm(span=period).mean())

        # Calculate the EWMA for the Down days.
        historical_price_df['ewma_down'] = historical_price_df['down_day'].transform(
            lambda x: x.ewm(span=period).mean())

        # Calculate the Relative Strength
        relative_strength = historical_price_df['ewma_up'] / historical_price_df['ewma_down']

        # Calculate the Relative Strength Index
        relative_strength_index = 100.0 - (100.0 / (1.0 + relative_strength))

        # Add info to the data frame.
        historical_price_df['Relative Strength Index'] = np.where(relative_strength_index == 0, 100, 100
                                                                  - (100 / (1 + relative_strength_index)))

        # Plot RSI and Close Price
        fig, axs = plt.subplots(2)
        fig.set_figheight(15)
        axs[0].set_title("Price")
        axs[0].plot(historical_price_df['Close'])
        axs[0].tick_params(axis='x', bottom='on', labelcolor='none')

        axs[1].set_title("Relative Strength Index")
        axs[1].plot(historical_price_df['Relative Strength Index'], 'tab:orange')
        plt.xticks(rotation=90)

        plt.show()

    def rate_of_change(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Rate Of Change of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating rate of change.

        Returns:
        ----
        plt.plot -- Two graphs vertically stacked, the top for Price and bottom for Rate of Change based on the chosen
        time horizon
        """

        # API call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Creating Rate Of Change column
        historical_price_df['Rate Of Change'] = historical_price_df['Close']. \
            transform(lambda x: x.pct_change(periods=period))

        # Drop unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN'], axis=1, inplace=True)

        # Plot Close Price and Rate of Change
        fig, axs = plt.subplots(2)
        fig.set_figheight(15)
        axs[0].set_title("Price")
        axs[0].plot(historical_price_df['Close'])
        axs[0].tick_params(axis='x', bottom='on', labelcolor='none')

        axs[1].set_title("Rate Of Change")
        axs[1].plot(historical_price_df['Rate Of Change'], 'tab:orange')
        plt.xticks(rotation=90)

        plt.show()

    def bollinger_bands(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Bollinger Bands of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating bollinger bands.

        Returns:
        ----
        plt.plot -- One graph with the three lines (Upper band, Close Price, Lower band) based on the chosen time
        horizon
        """

        # API Call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Define Moving Average
        historical_price_df['Moving Average'] = historical_price_df['Close']. \
            transform(lambda x: x.rolling(window=period).mean())

        # Define Moving Std
        historical_price_df['moving_std'] = historical_price_df['Close']. \
            transform(lambda x: x.rolling(window=period).std())

        # Define the Upper Band
        historical_price_df['Upper Band'] = historical_price_df['Moving Average'] + historical_price_df[
            'moving_std'] * 2

        # Define the Lower band
        historical_price_df['Lower Band'] = historical_price_df['Moving Average'] - historical_price_df[
            'moving_std'] * 2

        # Drop unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN', 'moving_std'], axis=1,
                                 inplace=True)

        historical_price_df['Date|Time'] = historical_price_df.index
        historical_price_df.reset_index(drop=True, inplace=True)

        # Plot DataFrame
        historical_price_df.plot(y=["Upper Band", "Lower Band", "Moving Average"], kind="line", figsize=(10, 10),
                                 ylabel='Price', xlabel='Date|Time', title=isin + ' - Bollinger Bands')

        plt.fill_between(historical_price_df["Date|Time"], historical_price_df["Lower Band"],
                         historical_price_df["Upper Band"], historical_price_df["Lower Band"], color='grey', alpha=0.1)

        plt.show()

    def stochastic_oscillator(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Stochastic Oscillator of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating stochastic oscillator.

        Returns:
        ----
        plt.plot -- A graph with two lines, fast stochastic (%K) and slow stochastic (%D) based on the chosen time
        horizon
        """

        # API Call function
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Fast Line
        historical_price_df['%K'] = (historical_price_df['Close'] - historical_price_df['Close'].rolling(
            period).min()) / \
                                    (historical_price_df['High'].rolling(period).max() - historical_price_df[
                                        'Close'].rolling(period).min())

        # Slow Line
        historical_price_df['%D'] = historical_price_df['%K'].rolling(3).mean()

        # Drop unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN'], axis=1,
                                 inplace=True)
        # Plot DataFrame
        historical_price_df.plot(y=["%K", "%D"], kind="line", figsize=(10, 10),
                                 ylabel='Price', xlabel='Date|Time', title=isin + ' - Stochastic Oscillator')

        plt.show()

    def force_index(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Force Index of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating force index.

        Returns:
        ----
        plt.plot -- Two graphs vertically stacked, the top for Price and bottom for Farce Index based on the chosen
        time horizon
        """

        # API Call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Create Force Index column
        historical_price_df['Force Index'] = historical_price_df['Close'].diff(period) * historical_price_df[
            'Volume'].diff(period)

        # Drop unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN'], axis=1,
                                 inplace=True)

        # Plot Close Price and Force Index
        fig, axs = plt.subplots(2)
        fig.set_figheight(15)
        axs[0].set_title("Price")
        axs[0].plot(historical_price_df['Close'])
        axs[0].tick_params(axis='x', bottom='on', labelcolor='none')

        axs[1].set_title("Force Index")
        axs[1].plot(historical_price_df['Force Index'], 'tab:orange')
        plt.xticks(rotation=90)

        plt.show()

    def ease_of_movement(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Ease Of Movement of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating ease of movement.

        Returns:
        ----
        plt.plot -- Two graphs vertically stacked, the top for Close Price and bottom for Ease Of Movement based on the
        chosen time horizon
        """

        # API Call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Calculate Raw Ease of Movement.
        high_plus_low = (historical_price_df['High'].diff(1) + historical_price_df['Low'].diff(1))
        diff_divi_vol = (historical_price_df['High'] - historical_price_df['Low']) / (2 * historical_price_df['Volume'])
        historical_price_df['ease_of_movement_raw'] = high_plus_low * diff_divi_vol

        # Calculate the Rolling Average of the Ease of Movement.
        historical_price_df['ease_of_movement'] = historical_price_df['ease_of_movement_raw'].transform(
            lambda x: x.rolling(window=period).mean()
        )

        # Drop unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN', 'ease_of_movement_raw'], axis=1,
                                 inplace=True)

        # Plot Close Price and Ease Of Movement
        fig, axs = plt.subplots(2)
        fig.set_figheight(15)
        axs[0].set_title("Price")
        axs[0].plot(historical_price_df['Close'])
        axs[0].tick_params(axis='x', bottom='on', labelcolor='none')

        axs[1].set_title("Ease Of Movement")
        axs[1].plot(historical_price_df['ease_of_movement'], 'tab:orange')
        plt.xticks(rotation=90)

        plt.show()

    def std(self, isin: str, unit: str, from_date: str, to_date: str, period: int) -> plt.plot:
        """ Returns a line chart for the Standard Deviation of an instrument.

        Arguments:
        ----
        isin {string} -- the International Securities Identification Number (ISIN) for an instrument.

        unit {string} -- the unit for data aggregation m1 (per-minute), h1 (hourly), d1 (daily).

        from_date {string} -- Start of time range you want to get OHLC data for. For d1, you can request 60 days of
        data with one request. For m1 and h1, you can request data for one day. The difference between from_date and
        to_date can cannot be longer than 1 day for m1, h1 and 60 days for d1.

        to_date {string} -- End of time range you want to get OHLC data for.

        period {int} -- number of periods to use when calculating standard deviation.

        Returns:
        ----
        plt.plot -- Two graphs vertically stacked, the top for Price and bottom for Standard Deviation based on the
        chosen time horizon
        """

        # API call
        historical_price_df = self._instrument_historical_prices(isin, unit, from_date, to_date)

        # Calculate the Standard Deviation.
        historical_price_df['std'] = historical_price_df['Close'].transform(lambda x: x.ewm(span=period).std())

        # Drop unwanted columns
        historical_price_df.drop(columns=['Open', 'High', 'Low', 'Volume', 'ISIN'], axis=1,
                                 inplace=True)

        # Plot Close Price and Standard Deviation
        fig, axs = plt.subplots(2)
        fig.set_figheight(15)
        axs[0].set_title("Price")
        axs[0].plot(historical_price_df['Close'])
        axs[0].tick_params(axis='x', bottom='on', labelcolor='none')

        axs[1].set_title("Standard Deviation")
        axs[1].plot(historical_price_df['std'], 'tab:orange')
        plt.xticks(rotation=90)

        plt.show()
