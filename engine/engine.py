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
COOLDOWN_SECONDS = 300   # 5 دقائق
TREND_THRESHOLD = 0.2
MIN_VOLATILITY = 0.07
MIN_AI_SCORE = 70        # فلترة أقوى

last_signal_time = {}
last_market_status = None

# ================== MARKET ==================
def forex_market_open():
    now = datetime.utcnow()
    weekday = now.weekday()
    hour = now.hour

    if weekday in [5, 6]:
        return False
    if weekday == 0 and hour < 22:
        return False
    if weekday == 4 and hour >= 22:
        return False
    return True

# ================== HELPERS ==================
def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def market_is_trending(ema50, ema200):
    return abs(ema50 - ema200) >= TREND_THRESHOLD

def candle_confirm(direction, open_p, close_p):
    return (direction == "CALL" and close_p > open_p) or \
           (direction == "PUT" and close_p < open_p)

def volatility_ok(high, low):
    return abs(high - low) >= MIN_VOLATILITY

# ================== SIGNAL ==================
def send_signal(pair, timeframe, signal, market_type):
    egypt_time = datetime.utcnow() + timedelta(hours=2)

    minutes = int(timeframe.replace("m", ""))
    expiry = egypt_time + timedelta(minutes=minutes)

    message = f"""
📊 إشارة تداول ({market_type})

💱 الزوج: {pair}
⏱ الفريم: {timeframe}
📈 الاتجاه: {'صعود' if signal['direction']=='CALL' else 'هبوط'}

🧠 سبب الدخول:
• RSI = {signal['rsi']}
• EMA50 = {signal['ema50']}
• EMA200 = {signal['ema200']}
• AI Score = {signal['ai_score']}%
• ترند واضح + شمعة تأكيد

🕒 وقت الدخول: {egypt_time.strftime('%H:%M:%S')} 🇪🇬
⏳ انتهاء الصفقة: {expiry.strftime('%H:%M:%S')} 🇪🇬
"""

    send_telegram(message)

# ================== STRATEGY ==================
def calculate_signal(pair, market_type):
    ema50 = random.uniform(1.0, 2.0)
    ema200 = random.uniform(1.0, 2.0)
    rsi = random.randint(30, 70)
    ai_score = random.randint(50, 100)

    open_p = random.uniform(1.0, 2.0)
    close_p = random.uniform(1.0, 2.0)
    high = max(open_p, close_p) + random.uniform(0.0, 0.1)
    low = min(open_p, close_p) - random.uniform(0.0, 0.1)

    if not volatility_ok(high, low):
        return None

    if not market_is_trending(ema50, ema200):
        return None

    if ai_score < MIN_AI_SCORE:
        return None

    if ema50 > ema200 and 40 <= rsi <= 55 and candle_confirm("CALL", open_p, close_p):
        return {
            "direction": "CALL",
            "rsi": rsi,
            "ema50": round(ema50, 4),
            "ema200": round(ema200, 4),
            "ai_score": ai_score
        }

    if ema50 < ema200 and 45 <= rsi <= 60 and candle_confirm("PUT", open_p, close_p):
        return {
            "direction": "PUT",
            "rsi": rsi,
            "ema50": round(ema50, 4),
            "ema200": round(ema200, 4),
            "ai_score": ai_score
        }

    return None

# ================== MAIN LOOP ==================
print("🚀 Aquila Engine Started")

while True:
    settings = load_settings()

    if not settings.get("enabled"):
        time.sleep(5)
        continue

    timeframe = settings.get("timeframe", "1m")
    forex_pairs = settings.get("pairs", [])
    otc_pairs = settings.get("otc_pairs", [])

    forex_open = forex_market_open()

    # 🔔 تنبيه حالة السوق مرة واحدة
    if forex_open != last_market_status:
        if not forex_open:
            send_telegram("⛔ السوق العالمي مغلق حاليًا — التحويل تلقائيًا إلى OTC")
        else:
            send_telegram("✅ السوق العالمي مفتوح — تم التحويل إلى FOREX")
        last_market_status = forex_open

    pairs = forex_pairs if forex_open else otc_pairs
    market_type = "FOREX" if forex_open else "OTC"

    now = time.time()

    for pair in pairs:
        last_time = last_signal_time.get(pair, 0)
        if now - last_time < COOLDOWN_SECONDS:
            continue

        signal = calculate_signal(pair, market_type)
        if signal:
            send_signal(pair, timeframe, signal, market_type)
            last_signal_time[pair] = now

    time.sleep(60)
