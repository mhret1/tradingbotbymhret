import pandas as pd
import ta
import ta.momentum
from src.fvg_detector import detect_fvg
def passes_filters(trade, candles: pd.DataFrame):
    # Check if the trade alert passes your filter conditions
    recent =  candles.tail(20).copy()
    
    # RSI filter
    recent["rsi"] = ta.momentum.RSIIndicator(close = recent["close"]).rsi()
    current_rsi = recent["rsi"].iloc[-1]
    if trade["direction"] == "buy" and current_rsi > 70:
        return False  # overbought, avoid buys
    if trade["direction"] == "sell" and current_rsi < 30:
        return False
    
    fvg_zones = detect_fvg(candles)
    if not fvg_zones:
        print("❌ Rejected: No FVG detected")
        return False
    return True