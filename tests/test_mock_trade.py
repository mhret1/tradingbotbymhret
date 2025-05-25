
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# scripts/test_full_bot.py
from src.mock_trade_executor import execute_mock_trade
from src.trade_manager import check_trades_for_breakeven
from src.performance_tracker import analyze_performance

# Step 1: Simulate trade execution
trade = {
    "symbol": "XAUUSD",
    "direction": "buy",
    "entry": 2340.0,
    "sl": 2338.0,
    "tp": 2344.0,
    "rr": 2.0
}
execute_mock_trade(trade)

# Step 2: Simulate breakeven logic (using mock price)
check_trades_for_breakeven()


analyze_performance()