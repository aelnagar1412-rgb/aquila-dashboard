def ai_decision(trend, momentum, volatility):
    score = 0

    if trend == "UP":
        score += 40
    elif trend == "DOWN":
        score += 40

    if momentum == "STRONG":
        score += 35

    if volatility == "NORMAL":
        score += 25

    confidence = min(score, 100)

    if confidence >= 75:
        return True, confidence
    else:
        return False, confidence
