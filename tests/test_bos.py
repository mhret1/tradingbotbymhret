import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.bos_detector import detect_bos_flexible

# Load candle data (1m)
df = pd.read_csv("data/sample_backtest.csv")
df["time"] = pd.to_datetime(df["time"])
df = df[df["symbol"] == "XAUUSD"].reset_index(drop=True)

# Run BoS detection
bos, lookback_used, recent = detect_bos_flexible(df, min_lookback=3, max_lookback=10)

print("✅ BoS Detected" if bos else "❌ No BoS Detected")
if bos:
    print(f"Lookback used: {lookback_used}")
    print(recent.tail(3))
