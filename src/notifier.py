import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(trade): 
    message = (
        f"📈 *{trade['symbol']}* | *{trade['direction'].upper()}*\n"
        f"🎯 Entry: `{trade['entry']}`\n"
        f"🛡 SL: `{trade['sl']}` | 💰 TP: `{trade['tp']}`\n"
        f"📊 R:R: `{trade['rr']}`"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"[Telegram Error] {str(e)}")
