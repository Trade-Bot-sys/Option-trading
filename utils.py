import json
import requests
from datetime import datetime

def load_symbol_tokens(filepath='symbol_tokens.json'):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_to_log(stock, action, price, quantity):
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {stock} | {action} | {price} | Qty: {quantity}\n"
    with open("trade_log.txt", "a") as f:
        f.write(log_entry)

def send_telegram_alert(bot_token, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram Error:", e)

def save_access_token_to_json(token_data, filepath="access_token.json"):
    with open(filepath, 'w') as f:
        json.dump(token_data, f)
