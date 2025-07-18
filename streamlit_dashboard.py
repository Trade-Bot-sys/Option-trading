# streamlit_dashboard_ai_bot.py

import streamlit as st
import json
from angel_one_api import get_profile, get_funds, get_portfolio
from ai_signal_generator import load_ai_model
from telegram_alert import send_telegram_message
from main import run_bot  # This will run your full trading logic

st.set_page_config(page_title="Smart AI Option Trading Bot", layout="wide")

st.title("📈 Smart AI Trading Dashboard (Angel One)")

# ✅ 1. Load access token
try:
    with open("access_token.json") as f:
        access_data = json.load(f)
        client = access_data.get("client_code")
except Exception as e:
    st.error("❌ Access token not found or invalid.")
    st.stop()

# ✅ 2. API Connection Check
profile = get_profile()
if profile:
    st.success(f"✅ Connected to Angel One - Welcome {profile.get('name', 'Trader')}")
else:
    st.error("❌ Failed to connect to Angel One API.")
    st.stop()

# ✅ 3. Show Available Funds
funds = get_funds()
if funds:
    st.info(f"💰 Available Margin: ₹{funds.get('available_margin', '0')}")
else:
    st.warning("⚠️ Could not fetch funds info.")

# ✅ 4. Load AI Model
model = load_ai_model()
if model:
    st.success("✅ AI model loaded successfully.")
    send_telegram_message("✅ AI model loaded successfully in Streamlit dashboard.")
else:
    st.error("❌ Failed to load AI model.")
    send_telegram_message("❌ AI model load failed in Streamlit dashboard.")
    st.stop()

# ✅ 5. Show Portfolio (Options)
portfolio = get_portfolio()
if portfolio:
    st.subheader("📊 Live Option Portfolio")
    df = portfolio[portfolio['tradingsymbol'].str.contains('CE|PE', na=False)]
    st.dataframe(df)
else:
    st.warning("⚠️ No active positions or failed to fetch portfolio.")

# ✅ 6. Telegram Alert Test
if st.button("📤 Send Telegram Test Alert"):
    send_telegram_message("📤 Telegram Alert Test: Connected successfully!")
    st.success("✅ Test alert sent.")

# ✅ 7. Manual Bot Trigger
if st.button("🚀 Run AI Option Trading Bot Now"):
    st.info("🟡 Running bot logic... check logs or Telegram for trades.")
    run_bot()
    st.success("✅ Bot executed. Check logs and Telegram for results.")

st.markdown("---")
st.caption("Made with ❤️ for automated smart option trading using AI.")
