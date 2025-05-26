
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.notifier import send_breakeven_alert

from datetime import datetime

mock_positions = [
    {
        "ticket": 101,
        "symbol": "XAUUSD",
        "type": "buy",
        "entry": 2340.0,
        "sl": 2338.0,
        "tp": 2350.0,
        "volume": 0.1,
        "open_time": "2024-05-28 10:15:00"
    },
    {
        "ticket": 102,
        "symbol": "XAUUSD",
        "type": "sell",
        "entry": 2345.0,
        "sl": 2347.0,
        "tp": 2335.0,
        "volume": 0.2,
        "open_time": "2024-05-28 10:20:00"
    }
]

current_price = {
    "XAUUSD": 2341.5  # Fake live price
}

def check_and_apply_breakeven(positions, price_feed):
    updated_positions = []
    for pos in positions:
        symbol = pos["symbol"]
        direction = pos["type"]
        entry = pos["entry"]
        sl = pos["sl"]
        ticket = pos["ticket"]
        current = price_feed.get(symbol)

        should_be = entry

        if direction == "buy" and current > entry + 1 and sl < entry:
            print(f"✅ [BUY #{ticket}] Breakeven hit. Moving SL from {sl} to {entry}")
            pos["sl"] = should_be
            updated_positions.append(pos)
            send_breakeven_alert(pos)

        elif direction == "sell" and current < entry - 1 and sl > entry:
            print(f"✅ [SELL #{ticket}] Breakeven hit. Moving SL from {sl} to {entry}")
            pos["sl"] = should_be
            updated_positions.append(pos)
            send_breakeven_alert(pos)

        else:
            print(f"⏳ [#{ticket}] No breakeven condition met.")
    return updated_positions

if __name__ == "__main__":
    print("📊 Simulating breakeven manager...")
    updated = check_and_apply_breakeven(mock_positions, current_price)
    print("\n📝 Updated Positions:")
    for p in updated:
        print(f" - Ticket #{p['ticket']}: SL moved to {p['sl']}")