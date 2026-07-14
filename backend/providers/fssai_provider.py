from providers.regulatory_provider import RegulatoryProvider


class FssaiProvider(RegulatoryProvider):
    name = "FSSAI"
    source_url = "https://www.fssai.gov.in/"
    # Bumped to v2 — auto-invalidates any v1 UNKNOWN cache entries on next lookup
    dataset_version = "fssai-additive-compliance-local-v2-2026-06"
    evidence_type = "compliance"

    DATA = {
        # ── Original additive entries ──────────────────────────────────────────
        "citric acid": {
            "regulation": "Additive permission local table",
            "status": "PERMITTED",
            "confidence": 0.82,
        },
        "sodium benzoate": {
            "regulation": "Additive restriction local table",
            "status": "RESTRICTED",
            "confidence": 0.80,
        },
        "ascorbic acid": {
            "regulation": "Additive permission local table",
            "status": "PERMITTED",
            "confidence": 0.82,
        },

        # ── FSSAI-regulated spices and botanicals (FSS Act 2006, Schedule 5) ──
        "turmeric": {
            "regulation": "FSSAI spice and condiment standard",
            "status": "PERMITTED",
            "confidence": 0.80,
            "details": {"botanical_identity": "Curcuma longa", "category": "Spice"},
        },
        "ginger": {
            "regulation": "FSSAI spice and condiment standard",
            "status": "PERMITTED",
            "confidence": 0.80,
            "details": {"botanical_identity": "Zingiber officinale", "category": "Spice"},
        },
        "fenugreek": {
            "regulation": "FSSAI spice and condiment standard",
            "status": "PERMITTED",
            "confidence": 0.78,
            "details": {"botanical_identity": "Trigonella foenum-graecum", "category": "Spice"},
        },
        "licorice": {
            "regulation": "FSSAI flavouring and botanical standard",
            "status": "PERMITTED",
            "confidence": 0.76,
            "details": {"botanical_identity": "Glycyrrhiza glabra", "category": "Flavouring"},
        },
        "amla": {
            "regulation": "FSSAI fruit and vegetable standard",
            "status": "PERMITTED",
            "confidence": 0.78,
            "details": {"botanical_identity": "Emblica officinalis", "category": "Fruit"},
        },
        "neem": {
            "regulation": "FSSAI botanical ingredient standard",
            "status": "PERMITTED",
            "confidence": 0.72,
            "details": {"botanical_identity": "Azadirachta indica", "category": "Botanical"},
        },
        "ashwagandha": {
            "regulation": "FSSAI health supplement botanical standard",
            "status": "PERMITTED",
            "confidence": 0.74,
            "details": {"botanical_identity": "Withania somnifera", "category": "Health supplement botanical"},
        },
        "tulsi": {
            "regulation": "FSSAI flavouring and botanical standard",
            "status": "PERMITTED",
            "confidence": 0.74,
            "details": {"botanical_identity": "Ocimum sanctum", "category": "Botanical"},
        },
        "sugar": {
            "regulation": "FSSAI sugar and sweetener standard",
            "status": "PERMITTED",
            "confidence": 0.84,
        },
        "salt": {
            "regulation": "FSSAI salt standard",
            "status": "PERMITTED",
            "confidence": 0.84,
        },
        "coconut oil": {
            "regulation": "FSSAI edible oil standard",
            "status": "PERMITTED",
            "confidence": 0.82,
            "details": {"botanical_identity": "Cocos nucifera", "category": "Edible oil"},
        },
        "sesame oil": {
            "regulation": "FSSAI edible oil standard",
            "status": "PERMITTED",
            "confidence": 0.82,
            "details": {"botanical_identity": "Sesamum indicum", "category": "Edible oil"},
        },
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)
