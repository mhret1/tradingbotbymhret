import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.trade_filter import passes_filters
from src.trade_simulator import simulate_trade

# ✅ Load sample candle data
df = pd.read_csv("data/sample_backtest.csv")
df["time"] = pd.to_datetime(df["time"])
df = df[df["symbol"] == "XAUUSD"].reset_index(drop=True)

# ✅ Define a trade (must match the symbol + timing of the data)
trade_info = {
    "symbol": "XAUUSD",
    "direction": "buy",
    "entry": 2342.0,
    "sl": 2339.5,
    "tp": 2346.0,
    "rr": 2.0
}

print("🚀 Running trade through filters...")

# ✅ Run filters
if passes_filters(trade_info, df):
    print("✅ Trade PASSED — logging simulated result")
    simulate_trade(trade_info)
else:
    print("❌ Trade REJECTED by strategy filters")
