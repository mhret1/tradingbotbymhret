import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.trade_manager import check_trades_for_breakeven

check_trades_for_breakeven()
