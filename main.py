import time
import json
from datetime import datetime
from contract import download_contract_master, load_contracts
from option_trading import get_atm_strikes
from strategy_ai import get_trade_signal
from telegram_alerts import send_telegram_alert
from utils import place_order, monitor_trade
from config import BROKER, SYMBOL, LOT_SIZE

def run_trading_bot(live_mode=True):
    # Load Access Token
    try:
        with open("access_token.json") as f:
            access_data = json.load(f)
            access_token = access_data.get("access_token")
    except Exception as e:
        send_telegram_alert(f"❌ Failed to load access_token.json: {e}")
        return

    # Step 1: Download latest contract master
    download_contract_master()

    # Step 2: Load contracts
    contracts = load_contracts()

    # Step 3: Get ATM CE/PE for NIFTY
    atm_ce, atm_pe = get_atm_strikes(contracts)

    # Step 4: Predict trade signal using AI (Buy CE / Buy PE / Hold)
    signal = get_trade_signal()

    # Step 5: Decide which option to trade
    if signal == "BUY_CE":
        option_to_trade = atm_ce
    elif signal == "BUY_PE":
        option_to_trade = atm_pe
    else:
        send_telegram_alert("📉 No trade today as per AI signal.")
        return

    # Step 6: Place Order (Live or Test)
    if live_mode:
        order_response = place_order(option_to_trade, access_token)
        if order_response.get("status") == "success":
            order_id = order_response["order_id"]
            msg = f"✅ LIVE Trade Executed: {signal} on {option_to_trade['symbol']} (Order ID: {order_id})"
            send_telegram_alert(msg)

            # Step 7: Monitor SL/TP
            monitor_trade(option_to_trade, order_id, access_token)
        else:
            send_telegram_alert("❌ LIVE Order failed to place.")
    else:
        # Test Mode
        msg = f"🧪 TEST Trade: {signal} on {option_to_trade['symbol']}. No real order placed."
        print(msg)
        send_telegram_alert(msg)

# 👉 If running directly
if __name__ == "__main__":
    run_trading_bot(live_mode=True)
