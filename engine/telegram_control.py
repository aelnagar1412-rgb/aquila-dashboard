import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def handle(command: str):
    settings = load_settings()

    if command == "/start_bot":
        settings["enabled"] = True
        save_settings(settings)
        return "✅ Bot Enabled"

    elif command == "/stop_bot":
        settings["enabled"] = False
        save_settings(settings)
        return "⛔ Bot Disabled"

    elif command == "/status":
        status = "✅ Enabled" if settings["enabled"] else "⛔ Disabled"
        pairs = ", ".join(settings["pairs"])
        tf = settings["timeframe"]
        return f"📊 Status: {status}\n⏱ TF: {tf}\n📈 Pairs: {pairs}"

    else:
        return "❓ Unknown command"
