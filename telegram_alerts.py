import requests
import datetime

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = "TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"

def send_telegram_message(message: str):
    """Sends a message to your Telegram bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Telegram Error: {response.text}")
    except Exception as e:
        print(f"Telegram Exception: {e}")

def alert_trade(symbol, action, price, quantity, reason=None):
    """Alert for a trade entry"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"📢 <b>{action.upper()} Signal</b>\n🕒 {now}\n📈 Symbol: <b>{symbol}</b>\n💰 Price: ₹{price:.2f}\n📦 Qty: {quantity}"
    if reason:
        msg += f"\n🧠 Reason: {reason}"
    send_telegram_message(msg)

def alert_profit_loss(symbol, entry_price, exit_price, qty):
    """Alert for closing trade with PnL"""
    pnl = (exit_price - entry_price) * qty
    status = "✅ Profit" if pnl > 0 else "🔻 Loss"
    msg = (
        f"{status} Booked\n"
        f"📈 Symbol: <b>{symbol}</b>\n"
        f"💵 Entry: ₹{entry_price:.2f}\n"
        f"💼 Exit: ₹{exit_price:.2f}\n"
        f"📦 Qty: {qty}\n"
        f"📊 P&L: ₹{pnl:.2f}"
    )
    send_telegram_message(msg)

def alert_daily_summary(total_trades, win_trades, loss_trades, net_pnl):
    """Daily summary alert (4:30 PM)"""
    win_rate = (win_trades / total_trades) * 100 if total_trades else 0
    msg = (
        f"📋 <b>Daily Trade Summary</b>\n"
        f"📆 {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
        f"🔁 Total Trades: {total_trades}\n"
        f"✅ Wins: {win_trades}\n"
        f"❌ Losses: {loss_trades}\n"
        f"📈 Win Rate: {win_rate:.2f}%\n"
        f"💰 Net P&L: ₹{net_pnl:.2f}"
    )
    send_telegram_message(msg)
