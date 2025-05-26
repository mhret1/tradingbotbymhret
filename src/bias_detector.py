import pandas as pd

def detect_bias(candles: pd.DataFrame, lookback: int=5)-> str:
    closes = candles["close"].tail(lookback + 1).tolist()
    if len(candles) < 20:
        return "neutral" 
    
    current_close = closes[-1]
    previous_closes = closes[:-1]

    if current_close > max(previous_closes):
        return "buy"
    elif current_close < min(previous_closes):
        return "sell"
    else:
        return "neutral"