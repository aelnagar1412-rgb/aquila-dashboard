import json
import time
import os
from datetime import datetime
import pytz

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
EG_TIMEZONE = pytz.timezone("Africa/Cairo")

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def egypt_time():
    return datetime.now(EG_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")

def run_engine():
    print("🚀 Aquila Engine Started")

    while True:
        settings = load_settings()

        if not settings["enabled"]:
            print("⏸ Bot Disabled - waiting...")
            time.sleep(5)
            continue

        print("✅ Bot Enabled")
        print("🕒 Time (EG):", egypt_time())
        print("⏱ Timeframe:", settings["timeframe"])
        print("📈 Pairs:", settings["pairs"])

        for pair in settings["pairs"]:
            print(f"📢 Signal → {pair} | BUY | {egypt_time()}")

        time.sleep(60)

if __name__ == "__main__":
    run_engine()
