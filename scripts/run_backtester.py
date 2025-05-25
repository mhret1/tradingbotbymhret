import pandas as pd
from datetime import datetime
import os

# Load historical candle data
df = pd.read_csv("data/backtest_candles.csv")

# Backtest configuration
LOOKAHEAD_CANDLES = 5
RR = 2.0
results = []

# Backtest loop
for i in range(20, len(df) - LOOKAHEAD_CANDLES):
    candles = df.iloc[:i].copy()

    trade = {
        "symbol": "XAUUSD",
        "direction": "buy",  # TODO: use real bias detector
        "entry": df.iloc[i]["close"],
        "sl": df.iloc[i - 1]["low"],
        "tp": df.iloc[i]["close"] + RR * (df.iloc[i]["close"] - df.iloc[i - 1]["low"]),
        "rr": RR,
        "timestamp": df.iloc[i]["timestamp"]
    }

    # ✅ For now, we assume all setups are valid. Replace this with your real filter:
    # if passes_filters(trade, candles): 
    if True:
        future = df.iloc[i + 1 : i + 1 + LOOKAHEAD_CANDLES]
        result = "open"

        for _, row in future.iterrows():
            if row["low"] <= trade["sl"]:
                result = "loss"
                break
            if row["high"] >= trade["tp"]:
                result = "win"
                break

        pnl = RR * 100 if result == "win" else -100
        results.append({
            **trade,
            "result": result,
            "pnl": pnl
        })

# Save results
os.makedirs("logs", exist_ok=True)
results_path = "logs/backtest_results.csv"
pd.DataFrame(results).to_csv(results_path, index=False)

print(f"✅ Backtest finished. {len(results)} trades saved to {results_path}")
