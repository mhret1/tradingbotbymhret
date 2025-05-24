import pandas as pd
from datetime import datetime
TRADE_LOG_PATH = "logs/trade_log.csv"

def log_trade(trade):
    with open("logs/trade_log.txt","a") as f:
        f.write(f"{datetime.now()} | {trade['symbol']} | {trade['direction'].upper()} | " f"Entry: {trade['entry']} | SL: {trade['sl']} | TP: {trade['tp']} | RR: {trade['rr']}\n")

def simulate_trade(trade: dict):
    from random import choice
    result = choice(["win", "loss"])


    rr = trade.get("rr", 2.0)
    pnl = (trade["tp"] - trade["entry"]) if result == "win" else (trade["sl"] - trade["entry"])
    pnl = round(pnl if trade["direction"] == "buy" else -pnl, 2)

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": trade["symbol"],
        "direction": trade["direction"],
        "entry": trade["entry"],
        "sl": trade["sl"],
        "tp": trade["tp"],
        "rr": rr,
        "result": result,
        "pnl": pnl
    }

    # Append to CSV log
    df = pd.DataFrame([record])
    df.to_csv(TRADE_LOG_PATH, mode='a', header=not pd.io.common.file_exists(TRADE_LOG_PATH), index=False)

    print(f"📄 Trade logged: {record}")
    return record
