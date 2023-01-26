from typing import Optional
import requests
import random
from bs4 import BeautifulSoup
from .tickers import Tickers
from .filter import prefixer, is_filter_value_allowed, filter_exists
from .utils import get_number_of_pages, get_tickers_table, construct_table_from_data


class Screener:
    def __init__(self) -> None:
        """Screener that scrapes data from https://finviz.com
        """

        self.url = "https://finviz.com/screener.ashx?v=111"
        self.headers = [
            {
                'User-Agent': "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            },
            {
                "User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)",

            },

            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",

            },

            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/107.0.5304.110 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",

            }

        ]

    def get_header(self):
        return random.choice(self.headers)

    def query(self, filters: dict, limit: Optional[bool] = True) -> dict:

        url = self.url + self._construct_url(filters)
        data, total = self._get_page(url=url)

        tickers = Tickers(tickers=data)

        if limit and len(data) < limit:

            for page_idx in range(1, int(total)):
                tickers.add_tickers(self._get_page(url=url, page_idx=page_idx))
                if len(tickers) >= limit:
                    break

        return tickers

    def _get_page(self, url: str, page_idx: Optional[int] = None):
        """scrape data from a page given the page index and url

        Args:
            url (str): url of the page
            page_idx (Optional[int], optional): page index. Defaults to None.


        Returns:
            dict: data scraped from page
        """

        if page_idx and page_idx > 1:
            url += f"&r={20*(page_idx-1) + 1}"

        try:
            data = requests.get(
                url, headers=self.get_header()).content.decode()
            soup = BeautifulSoup(data, "html.parser")

            number_of_pages = get_number_of_pages(soup)

            # scrape data

            headers, table = get_tickers_table(soup)

            data = construct_table_from_data(headers, table)

            return data, number_of_pages

        except Exception as e:
            print("An error occured in geting the page...")
            raise e

    def _construct_url(self, filters: dict) -> str:
        """construct query url based on filters

        Args:
            filters (dict): dict of filters and the needed values

        Returns:
            str: query string
        """
        url = "&f="

        for category in filters:
            category_filters = filters[category]

            for filter_name in list(category_filters.keys()):

                if not filter_exists(filter_name):
                    raise ValueError(f"Invalid filter {filter_name}")

                filter_value = category_filters[filter_name]

                if not is_filter_value_allowed(filter_name, filter_value):
                    raise ValueError(
                        f"Invalid value `{filter_value}` for filter `{filter_name}`")

                url += prefixer(filter_name, filter_value) + ','

        url = url[:-1]  # remove that unecessary last ","

        return url
