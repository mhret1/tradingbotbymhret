import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from datetime import datetime
from src.trade_filter import passes_filters
from src.performance_tracker import log_trade_result

# Clean start
LOG_PATH = "logs/trade_log.csv"
if os.path.exists(LOG_PATH):
    os.remove(LOG_PATH)

# Load candle data
df_m1 = pd.read_csv("data/xauusd_m1.csv")
df_m1["timestamp"] = pd.to_datetime(df_m1["Local time"])
df_m1 = df_m1.rename(columns=lambda c: c.strip().lower())

df_1h = pd.read_csv("data/xauusd_1h.csv")
df_1h["timestamp"] = pd.to_datetime(df_1h["Local time"])
df_1h = df_1h.rename(columns=lambda c: c.strip().lower())

LOOKAHEAD = 60
RR = 2.0
SL_BUFFER = 2.0
results = []

for i in range(50, len(df_m1) - LOOKAHEAD):
    candles = df_m1.iloc[:i].copy()
    last_candle = df_m1.iloc[i]
    candles_1h_trimmed = df_1h[df_1h["timestamp"] <= last_candle["timestamp"]].tail(100).copy()
    if len(candles_1h_trimmed) < 20:
        continue

    trade = {
        "symbol": "XAUUSD",
        "timestamp": last_candle["timestamp"],
        "entry": last_candle["close"],
        "direction": "buy" if last_candle["close"] > last_candle["open"] else "sell",
        "rr": RR
    }

    if passes_filters(trade, candles, candles_1h_trimmed):
        entry = trade["entry"]
        direction = trade["direction"]
        sl = entry - SL_BUFFER if direction == "buy" else entry + SL_BUFFER
        tp = entry + RR * SL_BUFFER if direction == "buy" else entry - RR * SL_BUFFER

        result = "timeout"
        pnl = 0.0
        future = df_m1.iloc[i+1:i+1+LOOKAHEAD]

        for _, row in future.iterrows():
            if direction == "buy":
                if row["low"] <= sl:
                    result = "loss"
                    pnl = -SL_BUFFER
                    break
                if row["high"] >= tp:
                    result = "win"
                    pnl = RR * SL_BUFFER
                    break
            else:
                if row["high"] >= sl:
                    result = "loss"
                    pnl = -SL_BUFFER
                    break
                if row["low"] <= tp:
                    result = "win"
                    pnl = RR * SL_BUFFER
                    break

        log_trade_result({
            "symbol": trade["symbol"],
            "timestamp": trade["timestamp"],
            "direction": direction,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "rr": RR,
            "result": result,
            "pnl": pnl
        }, result, pnl)

        results.append(result)

print(f"✅ Backtest complete — Trades: {len(results)}")
