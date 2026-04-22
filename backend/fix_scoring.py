content = """def sustainability_score(certifications, packaging, ingredients_text):
    score = 50
    good_certs = ["en:organic", "en:fair-trade", "en:rainforest-alliance", "en:fsc", "en:ecocert", "en:eu-organic"]
    for cert in certifications:
        if cert in good_certs: score += 15
    p = packaging.lower()
    if "recycl" in p: score += 10
    if "glass" in p or "verre" in p: score += 10
    if "plastic" in p: score -= 20
    i = ingredients_text.lower()
    if "palm oil" in i or "huile de palme" in i: score -= 15
    if "organic" in i: score += 10
    return max(0, min(100, score))

def health_score(ingredients_text):
    score = 75
    bad = ["palm oil", "huile de palme", "high fructose", "corn syrup", "hydrogenated", "aspartame", "saccharin", "bha", "bht", "carrageenan"]
    good = ["organic", "whole grain", "vitamin", "fibre", "fiber", "protein"]
    i = ingredients_text.lower()
    for item in bad:
        if item in i: score -= 10
    for item in good:
        if item in i: score += 5
    return max(0, min(100, score))

def transparency_score(certifications, ingredients_text, packaging):
    score = 30
    if len(certifications) >= 1: score += 15
    if len(certifications) >= 3: score += 10
    if len(ingredients_text) > 100: score += 15
    if len(ingredients_text) > 200: score += 10
    if packaging and len(packaging) > 5: score += 10
    return min(100, score)

def social_score(certifications, brand):
    score = 40
    good_certs = ["en:fair-trade", "en:rainforest-alliance", "en:organic"]
    for cert in certifications:
        if cert in good_certs: score += 20
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
"""

with open('scoring.py', 'w') as f:
    f.write(content)
print('scoring.py written successfully')