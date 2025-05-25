import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.bos_detector import detect_bos_flexible
from src.bias_detector import detect_bias

# Load candle data (1m)
df_1h = pd.read_csv("data/sample_1h_bias_buy_csv.csv")  # this should be 1H candles
df_1h["time"] = pd.to_datetime(df_1h["time"])

df = pd.read_csv("data/sample_backtest.csv")
df["time"] = pd.to_datetime(df["time"])
df = df[df["symbol"] == "XAUUSD"].reset_index(drop=True)

# Run BoS detection
bos, lookback_used, recent = detect_bos_flexible(df, min_lookback=3, max_lookback=10)

print("✅ BoS Detected" if bos else "❌ No BoS Detected")
if bos:
    print(f"Lookback used: {lookback_used}")
    print(recent.tail(3))

bias = detect_bias(df_1h)
print(f"📊 Bias: {bias}")