import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from datetime import datetime
from src.trade_filter import passes_filters  # ✅ your smart-money filter

# Wipe log
LOG_PATH = "logs/backtest_results.csv"
if os.path.exists(LOG_PATH):
    os.remove(LOG_PATH)

# Load candles
df_m1 = pd.read_csv("data/xauusd_m1.csv")
df_1h = pd.read_csv("data/xauusd_1h.csv")
df_m1['timestamp'] = pd.to_datetime(df_m1['timestamp'])
df_1h['timestamp'] = pd.to_datetime(df_1h['timestamp'])

LOOKAHEAD_CANDLES = 60
RR = 2.0
results = []

for i in range(50, len(df_m1) - LOOKAHEAD_CANDLES):
    candles = df_m1.iloc[:i].copy()
    last_candle = df_m1.iloc[i]

    candles_1h_trimmed = df_1h[df_1h['timestamp'] <= last_candle['timestamp']].tail(100).copy()

    trade = {
        "symbol": "XAUUSD",
        "direction": "buy" if last_candle["close"] > last_candle["open"] else "sell",
        "entry": last_candle["close"],
        "sl": last_candle["low"] - 2,
        "tp": last_candle["close"] + RR * 2 if last_candle["close"] > last_candle["open"]
              else last_candle["close"] - RR * 2,
        "rr": RR,
        "timestamp": last_candle["timestamp"]
    }

    if passes_filters(trade, candles, candles_1h_trimmed):
        future = df_m1.iloc[i+1 : i+1+LOOKAHEAD_CANDLES]
        result = "open"

        for _, row in future.iterrows():
            if trade["direction"] == "buy":
                if row["low"] <= trade["sl"]:
                    result = "loss"
                    break
                if row["high"] >= trade["tp"]:
                    result = "win"
                    break
            else:
                if row["high"] >= trade["sl"]:
                    result = "loss"
                    break
                if row["low"] <= trade["tp"]:
                    result = "win"
                    break

        pnl = RR * 100 if result == "win" else -100
        results.append({ **trade, "result": result, "pnl": pnl })

# Save results
os.makedirs("logs", exist_ok=True)
pd.DataFrame(results).to_csv(LOG_PATH, index=False)
print(f"✅ Backtest finished. {len(results)} trades saved to {LOG_PATH}")
