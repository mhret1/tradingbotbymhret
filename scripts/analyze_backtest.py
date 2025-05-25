import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.notifier import send_telegram_message  # assumes you're using this for alerts

def analyze_backtest(path="logs/backtest_results.csv"):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print("❌ Backtest results not found.")
        return

    if df.empty:
        print("⚠️ Backtest results are empty.")
        return

    wins = df[df["result"] == "win"]
    losses = df[df["result"] == "loss"]
    open_trades = df[df["result"] == "open"]

    total = len(df)
    win_rate = len(wins) / (len(wins) + len(losses)) * 100 if len(wins) + len(losses) > 0 else 0
    net_pnl = df["pnl"].sum()
    avg_pnl = df["pnl"].mean()
    avg_rr = df["rr"].mean()

    # Print to console
    print("\n📊 Backtest Performance Summary")
    print("-" * 30)
    print(f"📈 Total Trades:     {total}")
    print(f"✅ Wins:             {len(wins)}")
    print(f"❌ Losses:           {len(losses)}")
    print(f"🔄 Open Trades:      {len(open_trades)}")
    print(f"🎯 Win Rate:         {win_rate:.2f}%")
    print(f"💰 Net PnL:          {net_pnl:.2f}")
    print(f"💡 Avg R:R:          {avg_rr:.2f}")
    print(f"📉 Avg PnL:          {avg_pnl:.2f}")
    print("-" * 30)

    # Format Telegram message
    summary = (
        f"📊 *Backtest Summary*\n"
        f"--------------------------\n"
        f"📈 Total Trades: `{total}`\n"
        f"✅ Wins: `{len(wins)}` | ❌ Losses: `{len(losses)}`\n"
        f"🎯 Win Rate: `{win_rate:.2f}%`\n"
        f"💰 Net PnL: `{net_pnl:.2f}`\n"
        f"📉 Avg PnL: `{avg_pnl:.2f}` | 💡 Avg R:R: `{avg_rr:.2f}`"
    )

    # Send to Telegram
    send_telegram_message(summary)

if __name__ == "__main__":
    analyze_backtest()
