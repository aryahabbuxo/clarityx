def sustainability_score(certifications, packaging, ingredients_text):
    # Base is low — environmental credibility must be earned through evidence,
    # not assumed. Approach informed by SUVA/ENVA environmental valuation principle
    # that impact must be verified, not self-declared.
    score = 20
    good_certs = ["en:organic", "en:fair-trade", "en:rainforest-alliance", "en:fsc", "en:ecocert", "en:eu-organic"]
    for cert in certifications:
        if cert in good_certs: score += 15
    p = packaging.lower()
    if "recycl" in p: score += 10
    if "glass" in p or "verre" in p: score += 8
    if "plastic" in p: score -= 15
    i = ingredients_text.lower()
    # Palm oil is a significant deforestation/biodiversity risk without certification
    if ("palm oil" in i or "huile de palme" in i) and not any(c in certifications for c in good_certs):
        score -= 15
    if "organic" in i: score += 8
    return max(0, min(100, score))

def health_score(ingredients_text):
    # Start neutral (50). Ingredient evidence moves the score up or down.
    # A product with no data is not assumed healthy.
    score = 50
    bad = ["palm oil", "huile de palme", "high fructose", "corn syrup", "hydrogenated",
           "aspartame", "saccharin", "bha", "bht", "carrageenan"]
    good = ["organic", "whole grain", "vitamin", "fibre", "fiber", "protein"]
    i = ingredients_text.lower()
    for item in bad:
        if item in i: score -= 8
    for item in good:
        if item in i: score += 5
    return max(0, min(100, score))

def transparency_score(certifications, ingredients_text, packaging):
    # Rewards verifiable, detailed disclosure. Minimal data = minimal trust.
    # Aligned with transparency-as-signal principle from NLP/greenwashing literature:
    # claims require substantiation (certifications + detailed ingredient disclosure).
    score = 10
    if len(certifications) >= 1: score += 20
    if len(certifications) >= 3: score += 15
    if len(ingredients_text) > 100: score += 20
    if len(ingredients_text) > 300: score += 15
    if packaging and len(packaging) > 5: score += 15
    return min(100, score)

def social_score(certifications, brand):
    # Neutral baseline (40). Fair trade and ethical sourcing certs are
    # the strongest positive signals for supply-chain social impact.
    score = 40
    cert_weights = {"en:fair-trade": 25, "en:rainforest-alliance": 15, "en:organic": 10}
    for cert in certifications:
        if cert in cert_weights: score += cert_weights[cert]
    bad_brands = ["nestle", "coca-cola", "coca cola", "pepsi", "unilever", "kraft"]
    if any(b in brand.lower() for b in bad_brands): score -= 15
    return max(0, min(100, score))

def waspas_score(scores, weights, lam=0.5):
    wsm = sum(w * s for w, s in zip(weights, scores))
    wpm = 1
    for w, s in zip(weights, scores):
        wpm *= (max(s, 1) / 100) ** w
    wpm *= 100
    return round(lam * wsm + (1 - lam) * wpm, 1)
