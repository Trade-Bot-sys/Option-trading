import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
import os
import requests

from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

# Constants
MODEL_GIST_URL = "https://gist.githubusercontent.com/Trade-Bot-sys/c4a038ffd89d3f8b13f3f26fb3fb72ac/raw/nifty25_model.pkl"
MODEL_PATH = "nifty25_model.pkl"
model = None
ai_enabled = False

def fetch_model_from_gist(gist_url):
    response = requests.get(gist_url)
    if response.status_code == 200:
        with open(MODEL_PATH, 'wb') as f:
            f.write(response.content)
        return joblib.load(MODEL_PATH)
    else:
        raise Exception("Failed to download model from Gist.")

try:
    model = fetch_model_from_gist(MODEL_GIST_URL)
    ai_enabled = True
    print("✅ AI model loaded from Gist.")
except Exception as e:
    print(f"⚠️ AI model load failed: {e}. Fallback to rule-based strategies.")
    ai_enabled = False

# Telegram constants (set your actual values)
TELEGRAM_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def download_model_from_gist():
    try:
        response = requests.get(MODEL_GIST_URL)
        if response.status_code == 200:
            with open(MODEL_PATH, 'wb') as f:
                f.write(response.content)
            send_telegram_alert("✅ AI model downloaded from Gist and ready.")
        else:
            send_telegram_alert("❌ Failed to download AI model from Gist.")
    except Exception as e:
        send_telegram_alert(f"❌ Model download error: {e}")

def add_indicators(df):
    df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
    macd = MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    boll = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['boll_upper'] = boll.bollinger_hband()
    df['boll_lower'] = boll.bollinger_lband()
    df = df.dropna()
    return df

def load_ai_model():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Downloading from Gist...")
        download_model_from_gist()

    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            send_telegram_alert("✅ AI Model loaded successfully.")
            return model
        except Exception as e:
            send_telegram_alert(f"❌ Error loading model: {e}")
            return None
    else:
        send_telegram_alert("❌ AI Model load failed.")
        return None

def generate_ai_signals(df):
    try:
        df = add_indicators(df)
        model = load_ai_model()
        if model is None:
            return df, []

        features = ['rsi', 'macd', 'macd_signal', 'boll_upper', 'boll_lower']
        df['signal'] = model.predict(df[features])
        df['ai_signal'] = df['signal'].map({0: 'SELL', 1: 'HOLD', 2: 'BUY'})
        return df, df['ai_signal'].tolist()
    except Exception as e:
        print(f"[ERROR] in generate_ai_signals: {e}")
        send_telegram_alert(f"❌ Error in signal generation: {e}")
        return df, []

def get_latest_ai_signal(df):
    df, signals = generate_ai_signals(df)
    if not signals:
        return "HOLD"
    return df.iloc[-1]['ai_signal']
