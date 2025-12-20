# ai_engine.py
# Aquila AI Decision Engine

from datetime import datetime
import pytz


CONFIDENCE_THRESHOLD = 75  # أقل نسبة ثقة مسموحة


def ai_decision(
    trend: str,
    momentum: str,
    volatility: str,
    time_bias: str = "NORMAL"
):
    """
    ترجع:
    (decision: bool, confidence: int, reason: str)
    """

    score = 0
    reasons = []

    # Trend
    if trend == "UP":
        score += 30
        reasons.append("الاتجاه صاعد")
    elif trend == "DOWN":
        score += 30
        reasons.append("الاتجاه هابط")
    else:
        reasons.append("الاتجاه غير واضح")

    # Momentum
    if momentum == "STRONG":
        score += 30
        reasons.append("الزخم قوي")
    elif momentum == "WEAK":
        score += 10
        reasons.append("الزخم ضعيف")

    # Volatility
    if volatility == "NORMAL":
        score += 25
        reasons.append("التذبذب مناسب")
    elif volatility == "HIGH":
        score += 10
        reasons.append("التذبذب عالي")

    # Time Bias
    if time_bias == "GOOD":
        score += 15
        reasons.append("التوقيت مناسب")
    else:
        reasons.append("التوقيت عادي")

    confidence = min(score, 100)

    if confidence >= CONFIDENCE_THRESHOLD:
        decision = True
    else:
        decision = False

    return decision, confidence, " + ".join(reasons)


def egypt_time():
    tz = pytz.timezone("Africa/Cairo")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
