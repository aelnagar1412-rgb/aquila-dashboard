from telegram import Bot
from datetime import datetime
import pytz

TOKEN = "8536113760:AAH5trng6DFqHnOnjnqEaE-3_WpXjYZnXik"
CHAT_ID = "818760257"  # هنملأها بعد خطوة بسيطة

bot = Bot(token=TOKEN)

egypt_tz = pytz.timezone("Africa/Cairo")
now = datetime.now(egypt_tz).strftime("%H:%M")

message = f"""
🦅 Aquila AI — رسالة اختبار

📊 السوق: الفوركس
💱 الزوج: EUR/USD
⏱ الفريم: 1 دقيقة
🕒 وقت الدخول (مصر 🇪🇬): {now}

📈 الاتجاه: شراء
🔥 قوة الصفقة: 8.8 / 10

🧠 قرار الذكاء الاصطناعي: الصفقة قوية
📌 لا توجد أخبار مؤثرة

⚠️ تداول يدوي — اختبار النظام فقط
"""

bot.send_message(chat_id=CHAT_ID, text=message)
