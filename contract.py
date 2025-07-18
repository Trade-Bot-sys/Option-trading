import requests
import zipfile
import io
import pandas as pd
import os

# Environment variables assumed set in Render
GIST_ID = os.getenv("GIST_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def download_contract_master():
    try:
        print("[INFO] Downloading Angel One Contract Master...")
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.zip"
        response = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall()
        csv_file = [name for name in z.namelist() if name.endswith(".csv")][0]
        df = pd.read_csv(csv_file)
        df.to_csv("contract_master.csv", index=False)
        print("[SUCCESS] Contract Master downloaded and saved as 'contract_master.csv'")
        upload_to_gist("contract_master.csv")
        return df
    except Exception as e:
        print("[ERROR] Failed to download contract master:", e)
        return None

def upload_to_gist(file_path):
    try:
        if not GIST_ID or not GITHUB_TOKEN:
            print("[WARNING] Gist credentials not set, skipping upload.")
            return
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        url = f"https://api.github.com/gists/{GIST_ID}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }
        data = {
            "files": {
                "contract_master.csv": {
                    "content": content
                }
            }
        }
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            print("[SUCCESS] Uploaded contract_master.csv to Gist.")
        else:
            print("[ERROR] Failed to upload Gist:", response.status_code, response.text)
    except Exception as e:
        print("[ERROR] Gist upload failed:", e)

def get_token(symbol, expiry_date, strike_price, option_type="CE"):
    try:
        df = pd.read_csv("contract_master.csv")
        df = df[df['name'] == symbol]
        df = df[df['instrumenttype'] == "OPTIDX"]
        df = df[df['optiontype'] == option_type]
        df = df[df['strike'] == float(strike_price)]
        df = df[df['expiry'] == expiry_date]
        if df.empty:
            print(f"[WARNING] No match for {symbol} {strike_price} {option_type} {expiry_date}")
            return None
        return df.iloc[0]['token']
    except Exception as e:
        print("[ERROR] in get_token:", e)
        return None

if __name__ == "__main__":
    download_contract_master()
