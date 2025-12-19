import requests
import time
from telegram_control import handle

BOT_TOKEN = "8570409684:AAEQBhKv0zMZaEXWcoCUGiJsKRspE5JuleM"
offset = 0

while True:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}"
    res = requests.get(url).json()

    for update in res["result"]:
        offset = update["update_id"] + 1
        if "message" in update:
            text = update["message"]["text"]
            handle(text)

    time.sleep(2)
