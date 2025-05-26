import csv
import os
from datetime import datetime
import pandas as pd
from src.notifier import send_telegram_message
LOG_PATH = "logs/trade_log.csv"

def log_trade_result(trade, result: str, pnl: float):
    os.makedirs("logs", exist_ok=True)

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        trade["symbol"],
        trade["direction"],
        trade["entry"],
        trade["sl"],
        trade["tp"],
        trade["rr"],
        result,
        round(pnl, 2)
    ]

    headers = ["timestamp", "symbol", "direction", "entry", "sl", "tp", "rr", "result", "pnl"]

    file_exists = os.path.isfile(LOG_PATH)

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(row)

    print(f"📝 Logged {result.upper()} | PnL: {pnl}")

def analyze_performance():
    if not os.path.exists(LOG_PATH):
        print("❌ No trade log found.")
        return

    df = pd.read_csv(LOG_PATH)
    if df.empty:
        print("⚠️ Log is empty.")
        return

    total_trades = len(df)
    wins = df[df["result"] == "win"]
    losses = df[df["result"] == "loss"]
    open_trades = df[df["result"] == "open"]

    win_rate = len(wins) / (len(wins) + len(losses)) * 100 if (len(wins) + len(losses)) > 0 else 0
    total_pnl = df["pnl"].sum()
    avg_rr = df["rr"].mean()
    avg_pnl = df["pnl"].mean()

    summary = (
        f"📊 *Session Performance*\n"
        f"--------------------------\n"
        f"📈 Total Trades: `{total_trades}`\n"
        f"✅ Wins: `{len(wins)}` | ❌ Losses: `{len(losses)}`\n"
        f"🎯 Win Rate: `{win_rate:.2f}%`\n"
        f"💰 Net PnL: `{total_pnl:.2f}`\n"
        f"📉 Avg PnL: `{avg_pnl:.2f}` | 💡 Avg R:R: `{avg_rr:.2f}`"
    )

    print(summary)
