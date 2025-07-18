import pandas as pd
from datetime import datetime

def round_to_nearest_strike(price, strike_gap):
    return round(price / strike_gap) * strike_gap

def get_nearest_expiry(symbol):
    try:
        df = pd.read_csv("contract_master.csv")
        df = df[df['name'] == symbol]
        df = df[df['instrumenttype'] == "OPTIDX"]
        expiry_dates = pd.to_datetime(df['expiry'].unique())
        expiry_dates = sorted([d for d in expiry_dates if d >= datetime.now()])
        if expiry_dates:
            return expiry_dates[0].strftime("%d-%b-%Y").upper()
        else:
            return None
    except Exception as e:
        print("[ERROR] in get_nearest_expiry:", e)
        return None

def select_option(symbol, spot_price, option_type="CE", strike_gap=50):
    try:
        expiry = get_nearest_expiry(symbol)
        if not expiry:
            print(f"[ERROR] No expiry found for {symbol}")
            return None, None

        strike = round_to_nearest_strike(spot_price, strike_gap)

        df = pd.read_csv("contract_master.csv")
        df = df[df['name'] == symbol]
        df = df[df['instrumenttype'] == "OPTIDX"]
        df = df[df['expiry'] == expiry]
        df = df[df['strike'] == strike]
        df = df[df['optiontype'] == option_type]

        if df.empty:
            print(f"[WARNING] No matching option found for {symbol} {expiry} {strike} {option_type}")
            return expiry, None

        return expiry, df.iloc[0]['token']
    except Exception as e:
        print("[ERROR] in select_option:", e)
        return None, None

# Example usage:
# expiry, token = select_option("NIFTY", 24000, "CE", 50)
# print("Expiry:", expiry, "Token:", token)
