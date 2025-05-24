import pandas as pd

def detect_bos_flexible(candles: pd.DataFrame, min_lookback: int = 3, max_lookback: int = 10):
    for lookback in range(min_lookback, max_lookback + 1):
        recent = candles.tail(lookback + 1)
        highs = recent["high"].tolist()

        current_high = highs[-1]
        previous_highs = highs[:-1]

        if current_high > max(previous_highs):
            return True, lookback, recent

    return False, None, candles.tail(max_lookback + 1)
