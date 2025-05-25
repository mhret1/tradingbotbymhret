import pandas as pd
from src.trade_filter import passes_filters
from src.performance_tracker import log_trade_result
from datetime import datetime

df = pd.read_csv("data/backtest_candles.csv")
results = []

LOOKAHEAD_CANDLES = 10  # candles to simulate forward
RR_TARGET = 2.0

for i in range(20, len(df) - LOOKAHEAD_CANDLES):
    candles = df.iloc[:i].copy()
    trade = {
        "symbol": "XAUUSD",
        "direction": "buy",  # TODO: add bias logic
        "entry": df.iloc[i].close,
        "sl": df.iloc[i - 1].low,
        "tp": df.iloc[i].close + RR_TARGET * (df.iloc[i].close - df.iloc[i - 1].low),
        "rr": RR_TARGET,
    }

    # Fake candle window for each component
    if passes_filters(trade, candles):
        entry_price = trade["entry"]
        sl = trade["sl"]
        tp = trade["tp"]
        outcome = "loss"

        future = df.iloc[i + 1 : i + 1 + LOOKAHEAD_CANDLES]
        for _, row in future.iterrows():
            if row.low <= sl:
                outcome = "loss"
                break
            elif row.high >= tp:
                outcome = "win"
                break

        pnl = RR_TARGET * 100 if outcome == "win" else -100
        results.append({
            **trade,
            "result": outcome,
            "pnl": pnl,
            "timestamp": df.iloc[i].timestamp
        })

# Log results to CSV
pd.DataFrame(results).to_csv("logs/backtest_results.csv", index=False)

print(f"✅ Backtest complete: {len(results)} trades simulated.")
