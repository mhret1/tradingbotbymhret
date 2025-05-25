import pandas as pd

def detect_bos_flexible(candles, min_lookback=3, max_lookback=10):
    for lookback in range(min_lookback, max_lookback + 1):
        recent = candles.tail(lookback + 1)
        lows = recent["low"].tolist()

        for i in range(1, len(recent)):
            current_low = lows[i]
            previous_lows = lows[:i]

            if current_low < min(previous_lows):
                return True, lookback, recent

    return False, None, candles.tail(max_lookback + 1)
