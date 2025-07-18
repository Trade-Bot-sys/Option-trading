import pandas as pd
import json
import requests
from datetime import datetime

# Your saved GitHub personal token & Gist ID
GITHUB_TOKEN = "your_github_token_here"
GIST_ID = "your_gist_id_here"
GIST_FILENAME = "symbol_tokens.json"

# Function to extract NIFTY/BANKNIFTY option tokens
def extract_symbol_tokens_from_contract(contract_file='contract_master.csv'):
    try:
        df = pd.read_csv(contract_file)
        df = df[df['instrumenttype'].isin(['OPTIDX'])]
        df = df[df['name'].isin(['NIFTY', 'BANKNIFTY'])]

        df['expiry'] = pd.to_datetime(df['expiry'])
        df = df[df['expiry'] == df['expiry'].min()]  # Use nearest expiry

        symbol_dict = {}
        for _, row in df.iterrows():
            key = f"{row['name']}_{row['strike']}_{row['optiontype']}"
            symbol_dict[key] = row['token']

        return symbol_dict

    except Exception as e:
        print("❌ Error processing contract file:", e)
        return {}

# Function to update existing Gist
def update_existing_gist(content_dict):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "files": {
            GIST_FILENAME: {
                "content": json.dumps(content_dict, indent=4)
            }
        }
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        gist_url = response.json()['html_url']
        print(f"✅ Gist updated successfully: {gist_url}")
        return gist_url
    else:
        print("❌ Failed to update gist:", response.json())
        return None

# === Main Trigger ===
if __name__ == "__main__":
    symbol_data = extract_symbol_tokens_from_contract()
    if symbol_data:
        update_existing_gist(symbol_data)
