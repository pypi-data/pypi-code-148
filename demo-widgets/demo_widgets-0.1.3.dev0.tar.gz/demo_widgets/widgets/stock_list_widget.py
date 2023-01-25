#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Eric.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from concurrent.futures import ThreadPoolExecutor

from ipywidgets import DOMWidget
from traitlets import Unicode, List
from .._frontend import module_name, module_version
import yfinance as yf

def get_stock_price(stock_symbol):
    return {
        "stock_symbol": stock_symbol,
        "stock_price": yf.Ticker(stock_symbol).info["currentPrice"]
    }


class StockListWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('StockListModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('StockListView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    
    input_label = Unicode('Stock Symbol').tag(sync=True)
    button_text = Unicode('Add Stock').tag(sync=True)
    stock_symbol = Unicode('').tag(sync=True)
    stocks = List([
        { "stock_symbol": "AAPL", "stock_price": 0 },
        { "stock_symbol": "MSFT", "stock_price": 0 },
        { "stock_symbol": "MU", "stock_price": 0 }
    ]).tag(sync=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_msg(self._handle_stock_lookup_msg)

    
    def _handle_stock_lookup_msg(self, _, content, buffers):
        match content["name"]:
            case "add-stock":
                self.stock_symbol = content["stock_symbol"]
                stock_ticker = yf.Ticker(self.stock_symbol)
                stocks_list = self.stocks.copy()
                stocks_list.append({
                    "stock_symbol": self.stock_symbol,
                    "stock_price": stock_ticker.info["currentPrice"]
                })
                self.stocks = stocks_list
            case "remove-stock":
                self.stock_symbol = content["stock_symbol"]
                stocks_list = [
                    stock for stock in self.stocks
                    if stock["stock_symbol"] !=  self.stock_symbol
                ]
                self.stocks = stocks_list   
            case "refresh-stocks":
                with ThreadPoolExecutor(max_workers=4) as executor:
                    stocks_list = list(executor.map(
                        get_stock_price,
                        [ stock['stock_symbol'] for stock in self.stocks ]
                    ))
                    self.stocks = stocks_list
                    print("updated stocks: ", self.stocks)               

