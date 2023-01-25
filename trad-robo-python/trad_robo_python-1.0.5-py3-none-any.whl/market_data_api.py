import requests


class MarketData:

    def __init__(self, market_api_key: str) -> None:
        """ Initializes a new instance of the MarketData object.

        Arguments:
        ----
        market_api_key {str} -- The Market API key assigned when you create an account on the Lemon Markets website.
        Can be found in the API Keys section under General once logged into your account.
        """
        self.market_api_key: str = market_api_key

    def ohlc(self, isin: str, x1: str = 'h1', from_: str = '', to_: str = '') -> dict:
        """Returns historic market data in the Open High Low Close (OHLC) format - typical candlestick charts.

        Arguments:
        ----
        isin {str} -- the International Securities Identification Number for the security, can specify a list as
        well.

        x1 {str} -- data granularity. Accepts the following entries, m1 (per-minute basis), h1 (hourly basis) and
        d1 (daily basis).

        from_ {str} -- Start of time range you want to get OHLC data for. Use int/date-iso-string to define the start
        date of your timestamp range. For d1 data, you can request 60 days of data with one request, therefore the time
        range between from and to cannot be longer than 60 days. If to_ is not defined, the API automatically returns
        data until the current day or up to 60 days, based on the from date. For h1 and m1 data, you can request
        historical data for one day, therefore the time range between from and to cannot be longer than 1 day.

        to_ {str} -- End of time range you want to get OHLC data for. Use int/date-iso-string to define the end date
        of your timestamp range. Request parameters are the same as from_ argument.

        Returns:
        ----
        dict -- A dictionary containing the isin, Open Price (o), Highest Price (h), Lowest Price (l), Close Price (c)
        and other relevant information. For Example:

        {
          "time": "2022-02-14T20:44:03.759+00:00",
          "results":
          [
            {
              "isin": "US88160R1014",
              "o": 777.9,
              "h": 777.9,
              "l": 762.5,
              "c": 768.7,
              "v": 433,
              "pbv": 333645.1,
              "t": "2021-09-02T00:00:00.000+00:00",
              "mic": "XMUN"
            },
            {
              "isin": "US88160R1014",
              ...
            },
            {
              ...
            }
          ],
          "previous": "https://data.lemon.markets/v1/ohlc/d1?isin=US88160R1014&from=2021-11-01&limit=10&page=1",
          "next": "https://data.lemon.markets/v1/ohlc/d1?isin=US88160R1014&from=2021-11-01&limit=10&page=3",
          "total": 999,
          "page": 2,
          "pages": 10
        }
        """

        # URL for data granularity
        if x1 == 'd1':
            request_ohlc_1 = "https://data.lemon.markets/v1/ohlc/d1/?"

        elif x1 == 'm1':
            request_ohlc_1 = "https://data.lemon.markets/v1/ohlc/m1/?"

        else:
            request_ohlc_1 = "https://data.lemon.markets/v1/ohlc/h1/?"

        request_ohlc = request_ohlc_1 + "isin={isin}&from={from_}&to={to_}".format(isin=isin, from_=from_, to_=to_)

        # Get request
        request = requests.get(request_ohlc, headers={"Authorization": f"Bearer {self.market_api_key}"})

        return request.json()

    def quotes(self, isin: str, mic: str = '', decimals: bool = True, epoch: bool = False, sorting: str = '',
                limit: int = '', page: int = '') -> dict:
        """Returns the latest quote for an instrument.

        Arguments:
        ----
        isin {str} -- the International Securities Identification Number for the security, can only specify exactly
        one ISIN.

        mic {str} -- the Market Identifier Code to filter for a specific Trading Venue. Currently, only XMUN is
        supported.

        decimals {bool} --  to specify the numbers format you want to get your response in. This can be either decimals
        or int. Default is true.

        epoch {bool} -- to specify the date format you want to get your response in. The default value is false, meaning
        that the API will return ISO string dates.

        sorting {str} -- to sort the API response, either ascending (as) or descending (desc)

        limit {int} -- to define the limit of displayed results on one page. The default value is 100, the maximum
        number is 250.

        page {int} -- Use it to define the specific results page you wish to display.

        Returns:
        ----
        dict -- A dictionary containing the isin, bid volume (b_v), ask volume (a_v), bid price (b), ask price (a),
        timestamp the quote occurred at (t) and the Market Identifier Code of the Trading Venue the quote occured at
        (mic). For example:

        {
          "time": "2022-02-14T20:44:03.759+00:00",
          "results":
          [
            {
              "isin": "US88160R1014",
              "b_v": 87,
              "a_v": 87,
              "b": 921.1,
              "a": 921.1,
              "t": "2021-10-28T08:51:03.669+00:00",
              "mic": "XMUN"
            }
          ],
          "previous": null,
          "next": null,
          "total": 1,
          "page": 1,
          "pages": 1
        }
        """

        # Quotes URL
        request_quotes = "https://data.lemon.markets/v1/quotes/latest/?isin={isin}&mic={mic}&decimals={decimals}&" \
                         "epoch={epoch}&sorting={sorting}&limit={limit}&page={page}".format(isin=isin,
                                                                                            mic=mic,
                                                                                            decimals=decimals,
                                                                                            epoch=epoch,
                                                                                            sorting=sorting,
                                                                                            limit=limit,
                                                                                            page=page)

        # Get Request
        request = requests.get(request_quotes, headers={"Authorization": f"Bearer {self.market_api_key}"})

        return request.json()

    def instruments(self, isin: str) -> dict:
        """Returns instrument information

        Arguments:
        ----
        isin {str} -- the International Securities Identification Number for the security, can only specify exactly
        one ISIN.

        Returns:
        ----
        dict -- A dictionary containing instrument information such as  ISIN, Symbol and Type. For Example:

        {
          "time": "2022-02-14T20:44:03.759+00:00",
          "results":
          [
            {
              "isin": "US19260Q1076",
              "wkn": "A2QP7J",
              "name": "COINBASE GLB.CL.A -,00001",
              "title": "COINBASE GLOBAL INC",
              "symbol": "1QZ",
              "type": "stock",
              "venues":
              [
                {
                  "name": "Börse München - Gettex",
                  "title": "Gettex",
                  "mic": "XMUN",
                  "is_open": true,
                  "tradable": true,
                  "currency": "EUR"
                }
              ]
            }
          ],
          "previous": "https://data.lemon.markets/v1/instruments?limit=100&page=1",
          "next": "https://data.lemon.markets/v1/instruments?limit=100&page=3",
          "total": 26283,
          "page": 2,
          "pages": 263
        }
        """

        # Instruments URL
        request_instruments = "https://data.lemon.markets/v1/instruments/?isin={isin}".format(isin=isin)

        # Get Request
        request = requests.get(request_instruments, headers={"Authorization": f"Bearer {self.market_api_key}"})

        return request.json()

