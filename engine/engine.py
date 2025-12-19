import time
import json
import random
from datetime import datetime

SETTINGS_FILE = "../settings.json"

COOLDOWN_SECONDS = 180
TREND_THRESHOLD = 0.15
MIN_VOLATILITY = 0.05  # minimum candle range

last_signal_time = {}

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def send_signal(pair, timeframe, direction):
    print(f"📢 Signal | {pair} | {timeframe} | {direction}")

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

def calculate_signal(pair):
    # --- Simulated indicators (replace with real feed later) ---
    ema_50 = random.uniform(1.0, 2.0)
    ema_200 = random.uniform(1.0, 2.0)
    rsi = random.randint(30, 70)

    open_p = random.uniform(1.0, 2.0)
    close_p = random.uniform(1.0, 2.0)
    high = max(open_p, close_p) + random.uniform(0.0, 0.1)
    low = min(open_p, close_p) - random.uniform(0.0, 0.1)

    # Session filter
    if not session_allowed():
        return None

    # Volatility filter
    if not volatility_ok(high, low):
        return None

    # Trend filter
    if not market_is_trending(ema_50, ema_200):
        return None

    # CALL
    if ema_50 > ema_200 and 40 <= rsi <= 55:
        if candle_confirm("CALL", open_p, close_p):
            return "CALL"

    # PUT
    if ema_50 < ema_200 and 45 <= rsi <= 60:
        if candle_confirm("PUT", open_p, close_p):
            return "PUT"

    return None

print("🚀 Aquila Engine Started")

while True:
    settings = load_settings()

    if not settings.get("enabled"):
        print("⏸ Bot Disabled - waiting...")
        time.sleep(5)
        continue

    timeframe = settings.get("timeframe", "1m")
    pairs = settings.get("pairs", [])

    print("✅ Bot Enabled")
    print("⏱ Timeframe:", timeframe)
    print("💱 Pairs:", pairs)

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
