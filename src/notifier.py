import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_breakeven_alert(position):
    message = (
        f"🔁 *SL moved to Breakeven!*\n"
        f"📌 Ticket: `{position['ticket']}`\n"
        f"📈 Symbol: `{position['symbol']}`\n"
        f"🔹 Type: `{position['type'].upper()}`\n"
        f"🎯 Entry: `{position['entry']}` → SL: `{position['sl']}`"
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
        print(f"[Telegram Error] {e}")
