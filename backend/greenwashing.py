ECO_BUZZWORDS = [
    "eco-friendly", "sustainable", "green", "natural",
    "biodegradable", "carbon neutral", "planet-friendly",
    "chemical-free", "non-toxic", "clean", "organic"
]

def extract_eco_claims(text):
    if not text:
        return []
    text_lower = text.lower()
    return [w for w in ECO_BUZZWORDS if w in text_lower]

def greenwashing_risk(claims, certifications):
    if not claims:
        return {"risk": "Low", "reason": "No eco-claims found"}
    verified = len(certifications)
    ratio = verified / (len(claims) + 1)
    if ratio < 0.2:
        return {"risk": "High", "reason": f"{len(claims)} eco-claims but only {verified} certifications"}
    elif ratio < 0.5:
        return {"risk": "Medium", "reason": "Some claims lack certification backing"}
    return {"risk": "Low", "reason": "Claims are backed by certifications"}