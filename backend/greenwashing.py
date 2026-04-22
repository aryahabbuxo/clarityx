ECO_BUZZWORDS = [
    "eco-friendly", "sustainable", "green", "natural", "biodegradable",
    "carbon neutral", "planet-friendly", "chemical-free", "non-toxic",
    "clean", "pure", "gentle", "soft", "fresh", "organic", "bio",
    "earth-friendly", "environmentally friendly", "zero waste",
    "recycled", "renewable", "plant-based", "cruelty-free"
]

VERIFIED_CERTS = [
    "en:organic", "en:fair-trade", "en:rainforest-alliance",
    "en:ecocert", "en:fsc", "en:eu-organic", "en:utz-certified",
    "en:cruelty-free", "en:vegan", "en:leaping-bunny"
]

SUSPICIOUS_BRANDS = [
    "nestle", "coca-cola", "coca cola", "pepsi", "unilever",
    "loreal", "l'oreal", "procter", "gamble", "chevron",
    "bp", "shell", "exxon", "philip morris"
]

def extract_eco_claims(text):
    if not text:
        return []
    text_lower = text.lower()
    return [w for w in ECO_BUZZWORDS if w in text_lower]

def greenwashing_risk(claims, certifications, brand, packaging, ingredients):
    risk_points = 0
    reasons = []

    verified = [c for c in certifications if c in VERIFIED_CERTS]
    
    if claims:
        if len(verified) == 0:
            risk_points += 3
            reasons.append(f"{len(claims)} eco-claims but zero verified certifications")
        elif len(claims) > len(verified) * 2:
            risk_points += 2
            reasons.append("claims outnumber certifications significantly")

    if any(b in brand.lower() for b in SUSPICIOUS_BRANDS):
        risk_points += 2
        reasons.append("brand has known sustainability controversies")

    packaging_lower = packaging.lower()
    ingredients_lower = ingredients.lower()
    
    if "plastic" in packaging_lower and len(verified) == 0:
        risk_points += 1
        reasons.append("plastic packaging with no eco certification")
    
    if ("palm oil" in ingredients_lower or "huile de palme" in ingredients_lower) and len(verified) == 0:
        risk_points += 2
        reasons.append("contains palm oil with no sustainability certification")

    if len(certifications) == 0 and len(ingredients) > 50:
        risk_points += 1
        reasons.append("no certifications found")

    if risk_points >= 4:
        risk = "High"
    elif risk_points >= 2:
        risk = "Medium"
    else:
        risk = "Low"

    reason = "; ".join(reasons) if reasons else "No major greenwashing signals detected"
    return {"risk": risk, "reason": reason, "risk_points": risk_points}