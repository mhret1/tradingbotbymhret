import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.performance_tracker import log_trade_result, analyze_performance

# Log a test trade
log_trade_result({
    "symbol": "XAUUSD",
    "direction": "buy",
    "entry": 2340.0,
    "sl": 2338.0,
    "tp": 2344.0,
    "rr": 2.0
}, result="win", pnl=80.0)

# Analyze and send summary
analyze_performance()
