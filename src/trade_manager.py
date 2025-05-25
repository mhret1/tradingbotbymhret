import pandas as pd

def mock_open_positions_from_csv(path="data/mock_open_positions.csv"):
    """
    Simulates open MT5 positions by reading from a CSV.
    Expected columns: symbol, direction, entry, sl, tp, rr
    """
    df = pd.read_csv(path)
    return df.to_dict("records")

def move_sl_to_breakeven(position):
    print(f"✅ [Simulated] Moved SL to breakeven for {position['symbol']} | {position['direction'].upper()} | Entry: {position['entry']}")

def check_trades_for_breakeven():
    positions = mock_open_positions_from_csv()
    if not positions:
        print("ℹ️ No open positions (mock).")
        return

    for pos in positions:
        entry = float(pos["entry"])
        sl = float(pos["sl"])
        rr_target = abs(entry - sl)
        current_price = float(pos["mock_price"])  # current simulated price

        if pos["direction"] == "buy":
            move = current_price - entry
        else:
            move = entry - current_price

        if move >= rr_target:
            print(f"🔁 Mock RR=1 hit for {pos['symbol']} | Moving SL to breakeven...")
            move_sl_to_breakeven(pos)
        else:
            print(f"⏳ No SL move for {pos['symbol']} | Price: {current_price} | Needed: {rr_target}")

if __name__ == "__main__":
    check_trades_for_breakeven()
