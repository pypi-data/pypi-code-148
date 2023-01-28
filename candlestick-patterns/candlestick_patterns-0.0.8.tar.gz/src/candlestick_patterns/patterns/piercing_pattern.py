from candlestick_patterns.patterns.candlestick_finder import CandlestickFinder


class PiercingPattern(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 2, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]
        prev_candle = self.data.iloc[idx + 1 * self.multi_coeff]

        close = candle[self.close_column]
        open = candle[self.open_column]


        prev_close = prev_candle[self.close_column]
        prev_open = prev_candle[self.open_column]

        prev_low = prev_candle[self.low_column]


        return (
            prev_close < prev_open
            and open < prev_low
            and prev_open > close > prev_close + ((prev_open - prev_close) / 2)
        )
