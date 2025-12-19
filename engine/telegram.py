import json
import requests

BOT_TOKEN = "8570409684:AAEQBhKv0zMZaEXWcoCUGiJsKRspE5JuleM"
CHAT_ID = "818760257"

SETTINGS_FILE = "../settings.json"

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def handle(text):
    settings = load_settings()

    if text == "/on":
        settings["enabled"] = True
        save_settings(settings)
        send("✅ تم تشغيل البوت")

    elif text == "/off":
        settings["enabled"] = False
        save_settings(settings)
        send("⛔ تم إيقاف البوت")

    elif text.startswith("/tf"):
        try:
            tf = text.split()[1]
            settings["timeframe"] = tf
            save_settings(settings)
            send(f"⏱ تم تغيير الفريم إلى {tf}")
        except:
            send("❌ استخدم: /tf 1m")

    elif text.startswith("/pairs"):
        try:
            pairs = text.replace("/pairs", "").strip().split(",")
            settings["pairs"] = [p.strip().upper() for p in pairs]
            save_settings(settings)
            send(f"💱 تم تحديث الأزواج:\n{', '.join(settings['pairs'])}")
        except:
            send("❌ استخدم: /pairs EURUSD,GBPUSD")

    elif text == "/status":
        msg = f"""
📊 حالة البوت:
• تشغيل: {settings.get('enabled')}
• فريم: {settings.get('timeframe')}
• أزواج: {settings.get('pairs')}
"""
        send(msg)

    else:
        send("❓ أمر غير معروف")
