import pandas as pd
import ta
from src.sweep_detector import detect_liquidity_sweep
from src.fvg_detector import detect_fvg
from src.bos_detector import detect_bos_flexible
from src.bias_detector import detect_bias

def passes_filters(trade: dict, candles: pd.DataFrame, candles_1h: pd.DataFrame) -> bool:
    """
    Applies all smart money filters:
    ✅ RSI + Liquidity Sweep + FVG + BoS
    Returns True if trade passes all conditions
    """
    print("🔍 Starting filter checks...")

    # --- Copy for safety
    candles = candles.copy()

    # ✅ Multi-timeframe bias filter
    bias = detect_bias(candles_1h)
    print(f"📊 HTF Bias (1H): {bias.upper()}")
    if bias == "neutral":
        print("❌ Rejected: Bias is neutral — waiting for confirmation")
        return False
    
    if trade["direction"] != bias:
        print(f"❌ Rejected: Trade direction is {trade['direction']} but bias is {bias}")
        return False
    print("✅ Bias aligns with trade direction")


    # ✅ 1. RSI Filter
    candles["rsi"] = ta.momentum.RSIIndicator(close=candles["close"]).rsi()
    rsi_now = candles["rsi"].iloc[-1]
    print(f"📈 RSI: {rsi_now:.2f}")

    if trade["direction"].lower() == "buy" and rsi_now > 70:
        print("❌ Rejected: RSI overbought")
        return False
    if trade["direction"].lower() == "sell" and rsi_now < 30:
        print("❌ Rejected: RSI oversold")
        return False

    # ✅ 2. Liquidity Sweep
    sweep, sweep_lookback, _ = detect_liquidity_sweep(candles, min_lookback=3, max_lookback=10)
    print(f"💧 Sweep Detected: {sweep} | Lookback: {sweep_lookback}")

    if not sweep:
        print("❌ Rejected: No Liquidity Sweep")
        return False

    # ✅ 3. Fair Value Gap
    fvg_zones = detect_fvg(candles)
    print(f"🧊 FVG Zones Detected: {len(fvg_zones)}")

    if not fvg_zones:
        print("❌ Rejected: No FVG zone")
        return False

    # ✅ 4. Break of Structure
    bos, bos_lookback, _ = detect_bos_flexible(candles, min_lookback=3, max_lookback=10)
    print(f"🔼 BoS Detected: {bos} | Lookback: {bos_lookback}")

    if not bos:
        print("❌ Rejected: No Break of Structure")
        return False

    
    print("✅ Trade PASSES all filters")
    return True
