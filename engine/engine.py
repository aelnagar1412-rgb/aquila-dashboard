import json
import time
from strategy import analyze
from ai_engine import ai_decision

SETTINGS_FILE = "/root/aquila-dashboard/settings.json"

def load_settings():
    with open(SETTINGS_FILE) as f:
        return json.load(f)

print("🚀 Aquila AI Engine Running")

while True:
    s = load_settings()

    if not s["enabled"]:
        time.sleep(5)
        continue

    for pair in s["pairs"]:
        data = analyze(pair, s["timeframe"], s["risk"])
        if not data:
            continue

        decision = ai_decision(data)
        if decision:
            print(f"""
📢 AI SIGNAL
💱 {decision['pair']}
⏱ {decision['timeframe']}
📊 RSI: {decision['rsi']}
🚀 {decision['direction']}
🕒 {decision['time']} 🇪🇬
""")

    time.sleep(60)
