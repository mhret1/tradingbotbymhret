import pandas as pd

def detect_fvg(candles: pd.DataFrame):
    fvg_zones = []
    for i in range(2, len(candles)):
        prev_high = candles.iloc[i-2]["high"]
        curr_low = candles.iloc[i]["low"]
        if curr_low > prev_high:
            fvg_zones.append({
                "start": candles.iloc[i-2]["timestamp"],
                "end": candles.iloc[i]["timestamp"],
                "zone_top": candles.iloc[i]["low"],
                "zone_bottom": candles.iloc[i-2]["high"]
            })
    return fvg_zones