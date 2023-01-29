import datetime
import logging
import traceback
from pathlib import Path
from typing import List, Optional
import yfinance as yf
import pandas as pd
import psycopg2

from transportlib.transport import BaseTransport

from transportlib.utils import dump_dataframe_as_csv, safe_convert_iso_str_to_datetime, get_from_env


def get_tickers_from_ccass(
        host= None,
        user=None,
        password=None,
        port=None,
        database=None,

):
    logging.info("Fetching tickers from Ccass stock codes")
    host = get_from_env(curr_val=host, env_key='POSTGRES_HOST', default_val=None)
    port = get_from_env(curr_val=port, env_key='POSTGRES_PORT', default_val=None)
    user = get_from_env(curr_val=user, env_key='POSTGRES_USER', default_val=None)
    password = get_from_env(curr_val=password, env_key='POSTGRES_PASSWORD', default_val=None)
    database = get_from_env(curr_val=database, env_key='POSTGRES_DATABASE', default_val=None)

    conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    cur = conn.cursor()

    get_tickers_from_ccass = '''
    SELECT substring(sehk_code,2)||'.hk'  from l0.hkex_ccass_stock hcs where sehk_code < '10000'
    '''
    logging.info('Running SQL')
    logging.info(get_tickers_from_ccass)

    cur.execute(get_tickers_from_ccass)
    result = [tup[0] for tup in cur.fetchall()]

    return result

class HistoricalStockPriceTransport(BaseTransport):

    def __init__(
            self,
            tickers: Optional[List[str]] = None,
            *args,
            **kwargs,
    ):
        super(HistoricalStockPriceTransport, self).__init__(*args, **kwargs)

        self.start_datetime = safe_convert_iso_str_to_datetime(self.watermark_val_prev)
        self.end_datetime = safe_convert_iso_str_to_datetime(self.watermark_val_curr)

        if tickers is None:
            logging.info("Tickers set to None. Fetching tickers all available HK tickers.")
            tickers = get_tickers_from_ccass()

        logging.info("Going to run for the below tickers.")
        logging.info(tickers)

        self.tickers = tickers

    def run(self):
        for ticker in self.tickers:
            logging.info(f'running ticker {ticker}')

            try:
                hist_df: pd.DataFrame = yf.download(
                tickers=ticker,
                start=self.start_datetime,
                end=self.end_datetime,
            )
            except KeyboardInterrupt as e:
                # stop and end
                logging.error(traceback.format_exc())
                break
            except Exception as e:
                # Can throw all sorts of errors
                logging.error(traceback.format_exc())
                continue
            else:
                hist_df = hist_df.reset_index()
                hist_df.insert(0, 'ticker', ticker)
                hist_df = hist_df.rename(
                    columns=
                    {
                        'Date': 'date',
                        'Open': 'open',
                        'High': 'high',
                        'Low': 'low',
                        'Close': 'close',
                        'Adj Close': 'adj_close',
                        'Volume': 'volume',
                    }
                )

                # hist_df = pd.concat([hist_df, hist_df])
                dump_dataframe_as_csv(dataframe=hist_df, csv_file_path=self.csv_file_path)

