import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.notifier import send_telegram_message

send_telegram_message({
    "symbol": "XAUUSD",
    "direction": "buy",
    "entry": 2340.0,
    "sl": 2338.0,
    "tp": 2344.0,
    "rr": 2.0
})
