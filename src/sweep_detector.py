import pandas as pd

def detect_liquidity_sweep(candles, min_lookback=3, max_lookback=10):
    for lookback in range(min_lookback, max_lookback + 1):
        recent = candles.tail(lookback + 1)
        highs = recent["high"].tolist()

        for i in range(1, len(recent)):
            current_high = highs[i]
            previous_highs = highs[:i]

            if current_high > max(previous_highs):
                close = recent.iloc[i]["close"]
                open_ = recent.iloc[i]["open"]
                if close < open_:  # bearish sweep
                    return True, lookback, recent

    return False, None, candles.tail(max_lookback + 1)



