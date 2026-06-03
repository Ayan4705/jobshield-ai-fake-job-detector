import re


# ---------------- RULE ENGINE ----------------
def rule_engine(job_text):

    text = job_text.lower()

    score = 0
    reasons = []

    # High-risk scam phrases
    suspicious_words = {
        "registration fee": 40,
        "security deposit": 40,
        "processing fee": 40,
        "training fee": 35,
        "document verification fee": 40,
        "activation fee": 35,
        "whatsapp only": 25,
        "telegram": 25,
        "urgent hiring": 15,
        "limited seats": 20,
        "no interview": 25,
        "no experience needed": 15,
        "earn money fast": 30,
        "instant joining": 25,
        "work from home": 10
    }

    # Check suspicious phrases
    for phrase, weight in suspicious_words.items():

        if phrase in text:
            score += weight
            reasons.append(
                f"Contains suspicious phrase: '{phrase}'"
            )

    # ---------------- PAYMENT DETECTION ----------------
    payment_pattern = (
        r"(pay|fee|deposit|purchase|training|"
        r"registration|processing|verification)"
        r".{0,30}(₹|\d{3,6})"
    )

    if re.search(payment_pattern, text):
        score += 50
        reasons.append(
            "Job asks candidate for money/payment"
        )

    # ---------------- HIGH SALARY CHECK ----------------
    salary_match = re.findall(
        r"₹\s?([\d,]+)|(\d+)\s?lpa",
        text
    )

    if salary_match:
        score += 5

    # Freshers + huge salary
    if (
        ("fresher" in text or
         "no experience" in text)
        and
        re.search(r"₹\s?[5-9]\d{4,}", text)
    ):
        score += 30
        reasons.append(
            "Unrealistically high salary "
            "for freshers"
        )

    return min(score, 100), reasons


# ---------------- HYBRID SCORE ----------------
def hybrid_score(ml_prob, rule_score):

    final_score = (
        (ml_prob * 100 * 0.6)
        + (rule_score * 0.4)
    )

    return final_score