def rsi_ema_strategy(rsi, price, ema50, candle):
    if rsi < 30 and price > ema50 and candle == "green":
        return "CALL"
    if rsi > 70 and price < ema50 and candle == "red":
        return "PUT"
    return None


def trend_pullback_strategy(ema20, ema50, rsi):
    if ema20 > ema50 and 40 <= rsi <= 50:
        return "CALL"
    if ema20 < ema50 and 50 <= rsi <= 60:
        return "PUT"
    return None


def breakout_strategy(price, high10, low10, rsi, volume, avg_volume):
    if price > high10 and rsi > 55 and volume > avg_volume:
        return "CALL"
    if price < low10 and rsi < 45 and volume > avg_volume:
        return "PUT"
    return None
