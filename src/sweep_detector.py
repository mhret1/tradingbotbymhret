import pandas as pd

def detect_liquidity_sweep(candles: pd.DataFrame, min_lookback=3, max_lookback=10):
    for lookback in range(min_lookback, max_lookback + 1):
        recent = candles.tail(lookback + 1)
        lows = recent["low"].tolist()

        for i in range(1, len(recent)):
            current_low = lows[i]
            previous_lows = lows[:i]

            if current_low < min(previous_lows):
                close = recent.iloc[i]["close"]
                open_ = recent.iloc[i]["open"]
                if close > open_:
                    return True, lookback, recent

    return False, None, candles.tail(max_lookback + 1)


