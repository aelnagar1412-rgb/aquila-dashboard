import time
import json
import os
from datetime import datetime, timedelta
import pytz

from telegram import send_message
from strategy import (
    rsi_ema_strategy,
    trend_pullback_strategy,
    breakout_strategy
)
from ai_engine import ai_decision

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

EG_TZ = pytz.timezone("Africa/Cairo")

def egypt_now():
    return datetime.now(EG_TZ)

def calc_expiry(start_time, timeframe):
    minutes = int(timeframe.replace("m", ""))
    return start_time + timedelta(minutes=minutes)

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

print("🚀 Aquila AI Engine Started")

last_sent = {}

while True:
    settings = load_settings()

    if not settings.get("enabled", False):
        time.sleep(5)
        continue

    timeframe = settings["timeframe"]
    pairs = settings["pairs"]

    for pair in pairs:
        now = egypt_now()
        key = f"{pair}_{now.strftime('%Y%m%d%H%M')}"
        if key in last_sent:
            continue

        # ===== بيانات وهمية (بدلها ببيانات حقيقية لاحقًا) =====
        rsi = 28
        price = 1.1000
        ema20 = 1.0995
        ema50 = 1.0980
        candle = "green"
        high10 = 1.1010
        low10 = 1.0950
        volume = 120
        avg_volume = 100
        # =======================================================

        s1 = rsi_ema_strategy(rsi, price, ema50, candle)
        s2 = trend_pullback_strategy(ema20, ema50, rsi)
        s3 = breakout_strategy(price, high10, low10, rsi, volume, avg_volume)

        signals = [s1, s2, s3]
        decision, strength = ai_decision(signals)

        if decision and strength >= 66:
            entry_time = now
            expiry_time = calc_expiry(entry_time, timeframe)

            message = (
                "🚨 إشارة تداول AI قوية\n\n"
                f"📊 الزوج: {pair}\n"
                f"⏱ الفريم: {timeframe}\n"
                f"🎯 الصفقة: {decision}\n\n"
                "🧠 AI Analysis:\n"
                f"• RSI + EMA {'✅' if s1 else '❌'}\n"
                f"• Trend Pullback {'✅' if s2 else '❌'}\n"
                f"• Breakout {'✅' if s3 else '❌'}\n\n"
                f"🔥 قوة الإشارة: {strength}%\n\n"
                f"🕒 الدخول: {entry_time.strftime('%I:%M:%S %p')} 🇪🇬\n"
                f"⏳ الانتهاء: {expiry_time.strftime('%I:%M:%S %p')} 🇪🇬\n\n"
                "⚠️ التزم بإدارة رأس المال\n"
                "🤖 Aquila AI Trader"
            )

            send_message(message)
            last_sent[key] = True
            print(f"✅ Signal sent for {pair}")

        time.sleep(2)

    time.sleep(30)
