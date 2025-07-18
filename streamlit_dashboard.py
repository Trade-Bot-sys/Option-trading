# streamlit_dashboard_ai_bot.py

import streamlit as st
import json
from angelone_api import get_available_funds, get_option_portfolio
#from ai_signal_generator import load_ai_model
from telegram_alerts import send_telegram_message
from main import run_trading_bot  # This will run your full trading logic

st.set_page_config(page_title="Smart AI Option Trading Bot", layout="wide")

st.title("📈 Smart AI Trading Dashboard (Angel One)")

# ✅ 3. Show Available Funds
funds = get_available_funds()
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
portfolio = get_option_portfolio()
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
