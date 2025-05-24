from datetime import datetime

def log_trade(trade):
    with open("logs/trade_log.txt","a") as f:
        f.write(f"{datetime.now()} | {trade['symbol']} | {trade['direction'].upper()} | " f"Entry: {trade['entry']} | SL: {trade['sl']} | TP: {trade['tp']} | RR: {trade['rr']}\n")