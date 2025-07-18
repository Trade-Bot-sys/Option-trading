import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
import os

from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

MODEL_PATH = "ai_model_xgb.pkl"

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
        print(f"[ERROR] Model file not found: {MODEL_PATH}")
        return None
    return joblib.load(MODEL_PATH)

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
        print("[ERROR] in generate_ai_signals:", e)
        return df, []

def get_latest_ai_signal(df):
    df, signals = generate_ai_signals(df)
    if not signals:
        return "HOLD"
    return df.iloc[-1]['ai_signal']
