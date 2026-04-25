def rule_engine(transaction):
    score = 0
    reasons = []

    # Rule 1: High amount
    if transaction["Amount"] > 10000:
        score += 0.6
        reasons.append("High transaction amount")

    # Rule 2: Odd time
    if transaction["Time"] < 10000:
        score += 0.3
        reasons.append("Transaction at unusual time")

    # Rule 3: Very large amount
    if transaction["Amount"] > 50000:
        score += 0.8
        reasons.append("Very large transaction")

    return min(score, 1.0), reasons