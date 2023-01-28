import pandas as pd
from candlestick_patterns import candlestick
print(candlestick)
df = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close'])
df.loc[0] = ['2018-01-01', 100, 110, 90, 100]
df.loc[1] = ['2018-01-02', 7205.01,	7435, 7157.12,	7202]
df.loc[2] = ['2018-01-03', 7202,	7275.86, 7076.42,	7254.74]
df.loc[3] = ['2018-01-04', 130, 140, 120, 130]
df = candlestick.inverted_hammer(df, target='result')
print(df)
