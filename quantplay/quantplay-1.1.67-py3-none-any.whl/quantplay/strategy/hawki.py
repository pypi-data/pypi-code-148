from quantplay.strategy.base import QuantplayAlgorithm
from quantplay.utils.constant import TickInterval
from quantplay.service import market
from quantplay.order_execution.mean_price import MeanPriceExecutionAlgo
import numpy as np
import pandas as pd


class HawkI(QuantplayAlgorithm):
    def __init__(self):

        # Mandatory Attributes
        self.interval = TickInterval.minute
        self.entry_time = "^(09|10):.*$"
        self.exit_time = "15:25"
        self.strategy_trigger_times = [self.entry_time]
        self.exchange_to_trade_on = "NFO"
        self.option_nearest_expiry_offset = 0
        self.stream_symbols_by_security_type = {"EQ": ["NIFTY 50"]}
        self.columns_for_uuid = ["date", "symbol"]
        self.exact_number_of_orders_per_uuid = 2
        self.strategy_type = "intraday"
        self.strategy_tag = "hawki"
        self.execution_algo = MeanPriceExecutionAlgo(7)

        # Optional Attribute
        self.data_required_for_days = 20
        self.option_chain_depth = 20
        self.backtest_after_date = "2021-06-01"

        super(HawkI, self).__init__()

    def add_vwap(self, option_data):
        option_data = option_data.sort_values(["symbol", "date"])
        option_data.loc[:, "vwap"] = option_data.close
        option_data.loc[:, "vwap"] = option_data["vwap"] * option_data["volume"]
        option_data.loc[:, "vwap"] = (
            option_data.groupby(["symbol", "date_only"])["vwap"].cumsum()
            / option_data.groupby(["symbol", "date_only"])["volume"].cumsum()
        )
        return option_data

    def get_trades(self, market_data):
        market_data.loc[:, "date_only"] = pd.to_datetime(market_data.date.dt.date)
        market_data.loc[:, "day_of_week"] = market_data.date.dt.day_name()

        equity_data = market_data[market_data.security_type == "EQ"]
        option_data = market_data[market_data.security_type == "OPT"]

        unique_equity_symbols = list(equity_data.symbol.unique())
        assert len(unique_equity_symbols) == 1
        assert set(unique_equity_symbols) == {"NIFTY 50"}

        option_data = self.add_vwap(option_data)

        option_data.loc[:, "is_less_than_vwap"] = np.where(
            option_data.close < option_data.vwap, 1, 0
        )
        option_data.loc[:, "vwap_score"] = option_data.is_less_than_vwap.rolling(20).sum()

        trades = market.get_trades(equity_data, entry_time_regex=self.entry_time)
        option_data = market.get_trades(option_data, entry_time_regex=self.entry_time)

        trades = self.add_expiry(trades, security_type="OPT")
        trades = trades[trades.date.dt.year >= 2019]

        trades = trades[trades.strike_gap > 0]

        trades.loc[:, "atm_price"] = (
            round(trades.close / trades.strike_gap) * trades.strike_gap
        )
        trades.loc[:, "atm_price"] = trades.atm_price.astype(int)

        market.add_columns_in_option_data(
            option_data, columns=["equity_symbol", "option_type"]
        )

        pe_options = option_data[option_data.option_type == "PE"]
        ce_options = option_data[option_data.option_type == "CE"]

        filtered_otm_option_data = []

        nifty_strike_pct_threshold_by_week_day = {
            "Friday": 2,
            "Monday": 2,
            "Tuesday": 1.5,
            "Wednesday": 1,
            "Thursday": 0.65,
        }

        nifty_close_threshold_by_week_day = {
            "Friday": 10,
            "Monday": 10,
            "Tuesday": 10,
            "Wednesday": 10,
            "Thursday": 8,
        }

        for option_type, option_data in [("PE", pe_options), ("CE", ce_options)]:
            option_data = pd.merge(
                option_data,
                trades[
                    ["date", "symbol", "atm_price", "strike_gap", "expiry_date"]
                ].rename(columns={"symbol": "equity_symbol"}),
                how="left",
                left_on=["date", "equity_symbol"],
                right_on=["date", "equity_symbol"],
            )

            option_data = option_data[~option_data.expiry_date.isna()]
            option_data = market.filter_contracts_matching_expiry_date(option_data)

            market.add_columns_in_option_data(option_data, columns=["strike_price"])

            option_data.loc[:, "strike_pct_away_from_atm"] = (
                option_data.strike_price / option_data.atm_price - 1
            ) * 100

            option_data.loc[:, "days_since_expiry"] = (
                option_data.expiry_date - option_data.date_only
            ).dt.days

            option_data.loc[:, "close_threshold"] = option_data.day_of_week.map(
                nifty_close_threshold_by_week_day
            )

            if option_type == "CE":
                option_data.loc[:, "strike_pct_threshold"] = option_data.day_of_week.map(
                    nifty_strike_pct_threshold_by_week_day
                )

                option_data = option_data[
                    (
                        option_data.strike_pct_away_from_atm
                        >= option_data.strike_pct_threshold
                    )
                    & (option_data.close >= option_data.close_threshold)
                ]
            else:
                option_data.loc[:, "strike_pct_threshold"] = -option_data.day_of_week.map(
                    nifty_strike_pct_threshold_by_week_day
                )
                option_data = option_data[
                    (
                        option_data.strike_pct_away_from_atm
                        <= option_data.strike_pct_threshold
                    )
                    & (option_data.close >= option_data.close_threshold)
                ]

            option_data = option_data[option_data.vwap_score == 20]

            option_data.loc[:, "vwap_close_pct_return"] = (
                option_data.vwap / option_data.close - 1
            ) * 100

            option_data = (
                option_data.sort_values(["vwap_close_pct_return"], ascending=False)
                .groupby(["date", "equity_symbol"])
                .head(1)
            )

            # option_data = (
            #     option_data.sort_values(["close"], ascending=False)
            #     .groupby(["date", "equity_symbol"])
            #     .head(1)
            # )

            option_data = option_data.drop(
                columns=[
                    "strike_pct_away_from_atm",
                    "days_since_expiry",
                    "strike_pct_threshold",
                    "close_threshold",
                ]
            )

            filtered_otm_option_data.append(option_data)

        trades = pd.concat(filtered_otm_option_data, axis=0)
        trades = trades.rename(
            columns={"equity_symbol": "symbol", "symbol": "tradingsymbol"}
        )

        trades = trades[
            trades.day_of_week.isin(["Tuesday", "Wednesday", "Thursday", "Friday"])
        ]

        trades.loc[:, "transaction_type"] = "SELL"
        trades.loc[:, "quantity"] = 100
        trades.loc[:, "stoploss"] = 1

        trades = self.filter_uuids_not_matching_count(trades)

        return (
            trades.sort_values("date")
            .groupby(["symbol", "date_only", "option_type"])
            .head(1)
            .reset_index()
        )


if __name__ == "__main__":
    HawkI().backtest()
