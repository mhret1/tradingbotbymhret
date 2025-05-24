import pandas as pd

def get_recent_candles(symbol="XAUUSD", timeframe="m1"):
    df = pd.read_csv("data/sample_backtest.csv")
    df = df[df["symbol"] == symbol]
    return df.tail(50).copy()