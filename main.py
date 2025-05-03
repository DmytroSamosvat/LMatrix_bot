import requests
import time

ETHERSCAN_API_KEY = 'ZDV8KUJFE2RCTZM51EMR5C68D1E5ZAIFXW'
TELEGRAM_BOT_TOKEN = '7336046458:AAFOOYXtQaLPxaY77z__3s-3nvZjbxmWB4E'
TELEGRAM_CHAT_ID = '123889552'

whale_wallets = [
    "0xdD8a88a848C4D23A43eFc43b9cEe92ad43F273",
    "0xf97c79d7e252b59d4fcf2cfa40c3a7a5e69f5fb4",
    "0x2e509178d104eaf7e804aa8e459a959d9711435",
    "0xDc76CD25977E0a5Ae17155770273aD58648900D3",
    "0x7ef1b4fe9d98d77ae2816ac82f5e3c21c28e56d9"
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram error:", e)

def check_whales():
    for wallet in whale_wallets:
        url = f'https://api.etherscan.io/api?module=account&action=txlist&address={wallet}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}'
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('status') != '1':
                continue
            for tx in data['result'][:3]:
                value_eth = int(tx['value']) / 10**18
                if value_eth >= 10:
                    alert = f"🚨 Whale TX: {value_eth:.2f} ETH\nFrom: {tx['from']}\nTo: {tx['to']}"
                    send_telegram_message(alert)
        except Exception as e:
            print("Fetch error:", e)

print("🤖 Whale bot started.")
while True:
    check_whales()
    time.sleep(600)
