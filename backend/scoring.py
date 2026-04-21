def sustainability_score(certifications, packaging):
    score = 40
    good_certs = ["en:organic", "en:fair-trade", "en:rainforest-alliance"]
    for cert in certifications:
        if cert in good_certs:
            score += 20
    if "recycl" in packaging.lower():
        score += 20
    if "plastic" in packaging.lower():
        score -= 15
    if "glass" in packaging.lower() or "verre" in packaging.lower():
        score += 10
    return max(0, min(100, score))

def health_score(ingredients_text):
    score = 80
    bad = ["palm oil", "huile de palme", "high fructose", "hydrogenated"]
    for item in bad:
        if item in ingredients_text.lower():
            score -= 15
    return max(0, score)

def transparency_score(certifications, ingredients_text):
    score = 50
    if len(certifications) > 0: score += 20
    if len(ingredients_text) > 50: score += 20
    if len(certifications) > 3: score += 10
    return min(100, score)

def social_score(certifications):
    score = 50
    if "en:fair-trade" in certifications: score += 30
    if "en:organic" in certifications: score += 20
    return min(100, score)

def waspas_score(scores, weights, lam=0.5):
    wsm = sum(w * s for w, s in zip(weights, scores))
    wpm = 1
    for w, s in zip(weights, scores):
        wpm *= (max(s, 1) / 100) ** w
    wpm *= 100
    return round(lam * wsm + (1 - lam) * wpm, 1)