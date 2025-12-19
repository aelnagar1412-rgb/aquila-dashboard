import time
import json
import os
from telegram import send_signal

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "settings.json")


def load_settings():
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)


def analyze_market(pair, timeframe):
    """
    تحليل تجريبي (placeholder)
    هيتبدل بعدين باستراتيجية حقيقية
    """
    import random
    return random.choice(["BUY", "SELL", None])


def run_engine():
    print("🚀 Aquila Engine Started")

    while True:
        settings = load_settings()

        if not settings.get("enabled", False):
            print("⏸ Bot Disabled - waiting...")
            time.sleep(5)
            continue

        timeframe = settings.get("timeframe", "1m")
        pairs = settings.get("pairs", [])

        print("✅ Bot Enabled")
        print(f"⏱ Timeframe: {timeframe}")
        print(f"📊 Pairs: {pairs}")

        for pair in pairs:
            signal_type = analyze_market(pair, timeframe)

            if signal_type:
                signal = {
                    "pair": pair,
                    "timeframe": timeframe,
                    "signal": signal_type
                }

                print(
                    f"📢 SIGNAL → {signal_type} | {pair} | {timeframe}"
                )
                send_signal(signal)

            time.sleep(1)

        time.sleep(5)


if __name__ == "__main__":
    run_engine()
