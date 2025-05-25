import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.trade_filter import passes_filters
from src.trade_simulator import simulate_trade

# ✅ Load 1m/5m (lower timeframe)
df_ltf = pd.read_csv("data/sample_backtest.csv")
df_ltf["time"] = pd.to_datetime(df_ltf["time"])

# ✅ Load 1H timeframe (for bias)
df_htf = pd.read_csv("data/sample_1h_bias_buy_csv.csv")
df_htf["time"] = pd.to_datetime(df_htf["time"])

# ✅ Sample trade that matches buy bias
trade_info = {
    "symbol": "XAUUSD",
    "direction": "sell",
    "entry": 2342.0,
    "sl": 2345.0,
    "tp": 2337.5,
    "rr": 2.0
}

# ✅ Run the bot
print("🚀 Starting trade filter + bias check...")
if passes_filters(trade_info, df_ltf, df_htf):
    print("✅ Trade passed all filters — executing...")
    simulate_trade(trade_info)
else:
    print("🚫 Trade rejected.")
