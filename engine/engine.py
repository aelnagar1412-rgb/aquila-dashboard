import time
import json
import random
import requests
from datetime import datetime, timedelta

# ================== TELEGRAM ==================
BOT_TOKEN = "8570409684:AAEQBhKv0zMZaEXWcoCUGiJsKRspE5JuleM"
CHAT_ID = "818760257"

# ================== FILES ==================
SETTINGS_FILE = "../settings.json"

# ================== ENGINE SETTINGS ==================
COOLDOWN_SECONDS = 180
TREND_THRESHOLD = 0.15
MIN_VOLATILITY = 0.05

last_signal_time = {}

# ================== HELPERS ==================
def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def market_is_trending(ema50, ema200):
    return abs(ema50 - ema200) >= TREND_THRESHOLD

def candle_confirm(direction, open_p, close_p):
    if direction == "CALL" and close_p > open_p:
        return True
    if direction == "PUT" and close_p < open_p:
        return True
    return False

def session_allowed():
    utc_hour = datetime.utcnow().hour
    return (8 <= utc_hour <= 17) or (13 <= utc_hour <= 22)

def volatility_ok(high, low):
    return abs(high - low) >= MIN_VOLATILITY

# ================== TELEGRAM ==================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

# ================== SIGNAL ==================
def send_signal(pair, timeframe, signal):
    egypt_time = datetime.utcnow() + timedelta(hours=2)

    if timeframe == "1m":
        expiry = egypt_time + timedelta(minutes=1)
    elif timeframe == "3m":
        expiry = egypt_time + timedelta(minutes=3)
    elif timeframe == "5m":
        expiry = egypt_time + timedelta(minutes=5)
    else:
        expiry = egypt_time + timedelta(minutes=1)

    direction = signal["direction"]
    rsi = signal["rsi"]
    ema50 = signal["ema50"]
    ema200 = signal["ema200"]

    message = f"""
📊 إشارة تداول (Pocket Option)

💱 الزوج: {pair}
⏱ الفريم: {timeframe}
📈 الاتجاه: {'صعود' if direction == 'CALL' else 'هبوط'}

🧠 سبب الدخول:
• RSI = {rsi}
• EMA50 = {ema50}
• EMA200 = {ema200}
• ترند واضح + شمعة تأكيد

🕒 وقت الدخول: {egypt_time.strftime('%H:%M:%S')} 🇪🇬
⏳ انتهاء الصفقة: {expiry.strftime('%H:%M:%S')} 🇪🇬
"""

    send_telegram(message)

# ================== STRATEGY ==================
def calculate_signal(pair):
    # --- Simulated indicators (replace later with real data) ---
    ema50 = random.uniform(1.0, 2.0)
    ema200 = random.uniform(1.0, 2.0)
    rsi = random.randint(30, 70)

    open_p = random.uniform(1.0, 2.0)
    close_p = random.uniform(1.0, 2.0)
    high = max(open_p, close_p) + random.uniform(0.0, 0.1)
    low = min(open_p, close_p) - random.uniform(0.0, 0.1)

    if not session_allowed():
        return None

    if not volatility_ok(high, low):
        return None

    if not market_is_trending(ema50, ema200):
        return None

    if ema50 > ema200 and 40 <= rsi <= 55:
        if candle_confirm("CALL", open_p, close_p):
            return {
                "direction": "CALL",
                "rsi": rsi,
                "ema50": round(ema50, 4),
                "ema200": round(ema200, 4)
            }

    if ema50 < ema200 and 45 <= rsi <= 60:
        if candle_confirm("PUT", open_p, close_p):
            return {
                "direction": "PUT",
                "rsi": rsi,
                "ema50": round(ema50, 4),
                "ema200": round(ema200, 4)
            }

    return None

# ================== MAIN LOOP ==================
print("🚀 Aquila Engine Started")

while True:
    settings = load_settings()

    if not settings.get("enabled"):
        print("⏸ Bot Disabled")
        time.sleep(5)
        continue

    timeframe = settings.get("timeframe", "1m")
    pairs = settings.get("pairs", [])

    now = time.time()

    for pair in pairs:
        last_time = last_signal_time.get(pair, 0)
        if now - last_time < COOLDOWN_SECONDS:
            continue

        signal = calculate_signal(pair)
        if signal:
            send_signal(pair, timeframe, signal)
            last_signal_time[pair] = now

    time.sleep(60)
