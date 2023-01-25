import pandas as pd
from robot import PyRobot
from pprint import pprint as pp

# Data Frame Settings
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.expand_frame_repr', False)

# Initialize the robot.
trading_robot = PyRobot(
    market_api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsZW1vbi5tYXJrZXRzIiwiaXNzIjoibGVtb24ubWFya2V0cyIsInN1YiI6InVzcl9xeVBZWkJCVFRRZlFmd3JMQllCMWRxUnd3WFZtR0taRnpNIiwiZXhwIjoxNjg0NDQwNDU1LCJpYXQiOjE2Njg4ODg0NTUsImp0aSI6ImFwa19xeVBZWktLdHRkWTVxbkZtRFNnMkZ3cW5SWHdYcmw3MkxaIiwibW9kZSI6Im1hcmtldF9kYXRhIn0.470Fy8pmTk4KUkoZ-0aPg2nliOKyQpBjgO_U1wjUae4',
    paper_trading_api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsZW1vbi5tYXJrZXRzIiwiaXNzIjoibGVtb24ubWFya2V0cyIsInN1YiI6InVzcl9xeVBZWkJCVFRRZlFmd3JMQllCMWRxUnd3WFZtR0taRnpNIiwiZXhwIjoxNjg0NDQwNDE2LCJpYXQiOjE2Njg4ODg0MTYsImp0aSI6ImFwa19xeVBZWkpKSEh3TmdmdDFwME1zUTNKOGxMTHhRTW05U2ROIiwibW9kZSI6InBhcGVyIn0.bkktSa6Z-STRR_SqMk3WwjzqKE-BKpOHHfQxj5z7Svc'
)

# Robot

pp(trading_robot.account_information) # Account information
# pp(trading_robot.withdraw_money(amount=25)) # Withdraw money
# pp(trading_robot.withdrawal_information) # Retrieve withdrawals
# pp(trading_robot.bank_statements()) # Bank Statements - from beginning
# pp(trading_robot.bank_statements(from_='2022-12-01')) # Bank Statements -  from a specific Date
# pp(trading_robot.bank_statements(from_='2022-11-18', to_='2022-11-29')) # Bank Statements - from and to a specific date
# pp(trading_robot.instrument_historical_prices(isin='US19260Q1076 ', unit='m1', from_date='2022-09-05 00:35:08',to_date='2022-09-05 22:35:08.217174')) # Instrument Historical Prices - minute
# pp(trading_robot.instrument_historical_prices(isin='US19260Q1076 ', unit='h1', from_date='2022-09-05 00:35:08',to_date='2022-09-05 22:35:08.217174')) # Instrument Historical Prices - hour
# pp(trading_robot.instrument_historical_prices(isin='US19260Q1076 ', unit='d1', from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174')) # Instrument Historical Prices - daily
# pp(trading_robot.instrument_quote(isin='US19260Q1076')) # Instrument quote

# Trade

# pp(trading_robot.trade.new_order(isin="US88160R1014", side="buy", quantity=2, expires_at="1D")) # Market Order - Buy 2 Tesla shares.
# pp(trading_robot.trade.new_order(isin="US19260Q1076", side="sell", quantity=2, expires_at="1D")) # Market Order - Sell 2 Coinbase shares.
# pp(trading_robot.trade.new_order(isin="US19260Q1076", side="buy", quantity=2, expires_at="1D", stop_price=55)) # Stop Price Order - Buy 2 Coinbase shares.
# pp(trading_robot.trade.new_order(isin="US19260Q1076", side="sell", quantity=2, expires_at="1D", stop_price=55)) # Stop Price Order - Sell 2 Coinbase shares.
# pp(trading_robot.trade.new_order(isin="US19260Q1076", side="buy", quantity=2, expires_at="1D", limit_price=100)) # Limit Price Order - Buy 2 Coinbase shares.
# pp(trading_robot.trade.new_order(isin="US19260Q1076", side="sell", quantity=2, expires_at="1D", limit_price=55)) # Limit Price Order - Sell 2 Coinbase shares.
# pp(trading_robot.trade.new_order(isin="US19260Q1076", side="sell", quantity=2, expires_at="1D", limit_price=55, stop_price=50)) # Stop Limit Price Order - Sell 2 Coinbase shares.
# pp(trading_robot.trade.new_order(isin="US19260Q1076", side="sell", quantity=2, expires_at="1D", limit_price=55, stop_price=50)) # Stop Limit Price Order - buy 2 Coinbase shares.
# pp(trading_robot.trade.retrieve_orders) # Retrieving Order
# pp(trading_robot.trade.activate_order(order_id='ord_ryCQZddWW4qHgSYFsGDlmHkk03xgKFhqw7')) # Activating Order - Successful
# pp(trading_robot.trade.activate_order(order_id='ord_ryCPbggddhnV6Fmg94D9wz0Qm1MwgXNpl4')) # Activating Order - Unsuccessful
# pp(trading_robot.trade.cancel_order(order_id='ord_ryCPbggddhnV6Fmg94D9wz0Qm1MwgXNpl4')) # Cancel Order

# Portfolio

# pp(trading_robot.portfolio.portfolio_metrics) # Portfolio metrics
# pp(trading_robot.portfolio.portfolio_orders) # Portfolio orders
# pp(trading_robot.portfolio.current_instrument_quotes) # Portfolio instrument quotes
# pp(trading_robot.portfolio.current_instrument_historical_prices(unit='m1', from_date='2022-09-05 00:35:08.217174',to_date='2022-09-05 18:35:08.217174')) # Hisotrial Price - minutes
# pp(trading_robot.portfolio.current_instrument_historical_prices(unit='h1', from_date='2022-09-05 00:35:08.217174',to_date='2022-09-05 18:35:08.217174')) # Hisotrial Price - hours
# pp(trading_robot.portfolio.current_instrument_historical_prices(unit='d1', from_date='2022-09-05 00:35:08.217174',to_date='2022-09-30 18:35:08.217174')) # Hisotrial Price - days

# Indicators

# pp(trading_robot.indicators.change_in_price(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174')) # Change in Price
# pp(trading_robot.indicators.sma(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # SMA
# pp(trading_robot.indicators.ema(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # EMA
# pp(trading_robot.indicators.rsi(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # RSI
# pp(trading_robot.indicators.rate_of_change(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # Rate of Change
# pp(trading_robot.indicators.bollinger_bands(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # Bollinger Bands
# pp(trading_robot.indicators.stochastic_oscillator(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # Stochastic Oscillator
# pp(trading_robot.indicators.force_index(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # Force Index
# pp(trading_robot.indicators.ease_of_movement(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # Ease Of Movement
# pp(trading_robot.indicators.std(isin='US19260Q1076',unit='d1',from_date='2022-09-05 00:35:08',to_date='2022-09-30 22:35:08.217174', period=7)) # Standard Deviation







