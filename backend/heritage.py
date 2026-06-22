"""Conservative traditional-use facts for recognised product ingredients."""

from __future__ import annotations

import re


# Curated cross-reference fields used by the AYUSH, TDU Ayurhaar and IMPD
# catalogues. Facts describe heritage and product use; they do not claim cures.
HERITAGE_INGREDIENTS = (
    ("Turmeric", ("turmeric", "curcuma longa", "haldi"), "Haridra", "a warming culinary spice and a common botanical in skin-care blends", "has a long history in Ayurvedic food and wellness traditions", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Ashwagandha", ("ashwagandha", "withania somnifera", "indian ginseng"), "Ashwagandha", "a well-known Ayurvedic root botanical", "is traditionally associated with restorative wellness practices", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Tulsi", ("tulsi", "holy basil", "ocimum tenuiflorum", "ocimum sanctum"), "Tulasi", "an aromatic leaf used in teas and personal-care formulas", "has been valued in Indian household and Ayurvedic traditions", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Neem", ("neem", "azadirachta indica"), "Nimba", "a botanical frequently used in soaps, oral-care, and scalp-care products", "is documented in longstanding Indian botanical traditions", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Amla", ("amla", "amalaki", "phyllanthus emblica", "emblica officinalis", "indian gooseberry"), "Amalaki", "a tart fruit used in food, hair-care, and botanical blends", "is a classic ingredient in Ayurvedic formulations", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Aloe vera", ("aloe vera", "aloe barbadensis"), "Kumari", "a moisture-rich plant extract used in gels, lotions, and hair care", "appears in several traditional botanical practices", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Shikakai", ("shikakai", "acacia concinna"), "Shikakai", "a naturally saponin-rich pod traditionally used for hair cleansing", "is part of South Asian plant-based hair-care traditions", ("TDU Ayurhaar", "IMPD")),
    ("Bhringraj", ("bhringraj", "bhringaraj", "eclipta alba", "eclipta prostrata"), "Bhringaraja", "a leafy botanical often included in traditional hair oils", "is documented in Ayurvedic hair-care traditions", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Coconut", ("coconut", "cocos nucifera", "coconut oil"), "Narikela", "a plant oil and food ingredient used for texture, nourishment, and conditioning", "has deep roots in coastal Indian food and self-care traditions", ("TDU Ayurhaar", "IMPD")),
    ("Ginger", ("ginger", "zingiber officinale", "shunthi"), "Shunthi", "a pungent rhizome used in foods, drinks, and traditional spice blends", "has been used across Ayurvedic culinary traditions", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Licorice", ("licorice", "liquorice", "glycyrrhiza glabra", "yashtimadhu"), "Yashtimadhu", "a naturally sweet root used in herbal blends and flavouring", "is recorded in Ayurvedic materia medica", ("AYUSH", "TDU Ayurhaar", "IMPD")),
    ("Fenugreek", ("fenugreek", "trigonella foenum-graecum", "methi"), "Methika", "a fragrant seed used in food and traditional hair-care preparations", "is familiar in Indian culinary and botanical traditions", ("AYUSH", "TDU Ayurhaar", "IMPD")),
)


def heritage_facts(ingredients: str, limit: int = 3) -> list[dict]:
    """Match API-supplied ingredient text to heritage knowledge records."""
    text = (ingredients or "").lower()
    facts = []
    for name, aliases, sanskrit, role, traditional_use, sources in HERITAGE_INGREDIENTS:
        match = next((a for a in aliases if re.search(r"(?<![a-z])" + re.escape(a) + r"(?![a-z])", text)), None)
        if match:
            facts.append({
                "ingredient": name,
                "matched_as": match,
                "sanskrit_name": sanskrit,
                "fun_fact": f"{name} ({sanskrit}) is {role}; it {traditional_use}.",
                "sources": list(sources),
                "disclaimer": "Traditional-use information only; it is not medical advice or a claim that this product treats a condition.",
            })
        if len(facts) == limit:
            break
    return facts
