import requests
import time
from telegram_control import handle

BOT_TOKEN = "8570409684:AAEQBhKv0zMZaEXWcoCUGiJsKRspE5JuleM"
CHAT_ID = "818760257"

LAST_UPDATE_ID = None

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def listen():
    global LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    while True:
        params = {"timeout": 30}
        if LAST_UPDATE_ID:
            params["offset"] = LAST_UPDATE_ID + 1

        r = requests.get(url, params=params).json()

        for update in r.get("result", []):
            LAST_UPDATE_ID = update["update_id"]
            msg = update.get("message", {})
            text = msg.get("text")

            if text:
                response = handle(text)
                send_message(response)

        time.sleep(2)

if __name__ == "__main__":
    print("📡 Telegram Listener Started")
    listen()
