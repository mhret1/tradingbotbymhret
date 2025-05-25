from src.performance_tracker import log_trade_result
from src.notifier import send_telegram_message

def execute_mock_trade(trade):
    print(f"✅ Simulated trade: {trade['direction'].upper()} {trade['symbol']} @ {trade['entry']}")
    result = "win"
    pnl = 85.0 if result == "win" else -50

    log_trade_result(trade, result=result, pnl=pnl)

    send_telegram_message(trade)

# Optional manual test
if __name__ == "__main__":
    trade = {
        "symbol": "XAUUSD",
        "direction": "buy",
        "entry": 2340.0,
        "sl": 2338.0,
        "tp": 2344.0,
        "rr": 2.0
    }
    execute_mock_trade(trade)