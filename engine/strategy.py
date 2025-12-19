import random

def analyze_market(pair, timeframe):
    """
    Dummy strategy (مرحلة أولى)
    هتتبدل بتحليل حقيقي بعد شوية
    """

    # محاكاة إشارة
    signal = random.choice(["BUY", "SELL", None])

    if signal:
        return {
            "pair": pair,
            "timeframe": timeframe,
            "signal": signal
        }

    return None
