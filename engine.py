import time
from utils import load_settings

def run_engine():
    print("🚀 Aquila Engine Started")

    while True:
        settings = load_settings()

        if not settings.get("enabled"):
            time.sleep(2)
            continue

        timeframe = settings.get("timeframe", "1m")
        pairs = settings.get("pairs", [])

        for pair in pairs:
            print(f"📊 Analyzing {pair} on {timeframe}")
            # هنا هنضيف الاستراتيجية بعدين

        time.sleep(60)
