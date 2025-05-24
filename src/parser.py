def parse_alert(data):
    try:
        return{
            "symbol": data["symbol"],
            "direction": data["direction"],
            "entry": float(data["entry"]),
            "sl": float(data["sl"]),
            "tp": float(data["tp"]),
            "rr":float(data.get("rr", 2.0)),
            
        }
    except(KeyError, ValueError):
        return None