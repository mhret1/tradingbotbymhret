
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.notifier import send_telegram_message


LOG_PATH = "logs/trade_log.csv"
if not os.path.exists(LOG_PATH):
    print("❌ No trade log found.")
    exit()

df = pd.read_csv(LOG_PATH)
if df.empty:
    print("⚠️ Log is empty.")
    exit()

total = len(df)
wins = df[df["result"] == "win"]
losses = df[df["result"] == "loss"]
timeouts = df[df["result"] == "timeout"]

win_rate = len(wins) / (len(wins) + len(losses)) * 100 if (len(wins)+len(losses)) > 0 else 0
total_pnl = df["pnl"].sum()
avg_rr = df["rr"].mean()
avg_pnl = df["pnl"].mean()

summary = (
    f"📊 *Backtest Summary*\n"
    f"------------------------------\n"
    f"📈 Total Trades:     {total}\n"
    f"✅ Wins:             {len(wins)}\n"
    f"❌ Losses:           {len(losses)}\n"
    f"⏱ Timeouts:         {len(timeouts)}\n"
    f"🎯 Win Rate:         {win_rate:.2f}%\n"
    f"💰 Net PnL:          {total_pnl:.2f}\n"
    f"📉 Avg PnL:          {avg_pnl:.2f}\n"
    f"💡 Avg R:R:          {avg_rr:.2f}"
)

print(summary)
send_telegram_message(summary)
