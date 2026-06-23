from providers.regulatory_provider import RegulatoryProvider


class CdscoProvider(RegulatoryProvider):
    name = "CDSCO"
    source_url = "https://cdsco.gov.in/"
    # Bumped to v2 — auto-invalidates any v1 UNKNOWN cache entries on next lookup
    dataset_version = "cdsco-cosmetic-compliance-local-v2-2026-06"
    evidence_type = "compliance"

    DATA = {
        # ── Original entries ───────────────────────────────────────────────────
        "water": {
            "regulation": "Indian cosmetic compliance local table",
            "status": "COMPLIANT",
            "confidence": 0.66,
        },
        "aloe vera": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.66,
        },

        # ── Heritage botanicals used in Indian cosmetics (Drugs & Cosmetics Act) ─
        "neem": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.70,
            "details": {"botanical_identity": "Azadirachta indica"},
        },
        "turmeric": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.70,
            "details": {"botanical_identity": "Curcuma longa"},
        },
        "shikakai": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.68,
            "details": {"botanical_identity": "Acacia concinna"},
        },
        "amla": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.68,
            "details": {"botanical_identity": "Emblica officinalis"},
        },
        "bhringraj": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.66,
            "details": {"botanical_identity": "Eclipta alba"},
        },
        "tulsi": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.66,
            "details": {"botanical_identity": "Ocimum sanctum"},
        },
        "brahmi": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.65,
            "details": {"botanical_identity": "Bacopa monnieri"},
        },
        "hibiscus": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.65,
            "details": {"botanical_identity": "Hibiscus rosa-sinensis"},
        },
        "ashwagandha": {
            "regulation": "Indian cosmetic botanical identity local table",
            "status": "COMPLIANT",
            "confidence": 0.65,
            "details": {"botanical_identity": "Withania somnifera"},
        },
        "coconut oil": {
            "regulation": "Indian cosmetic compliance local table",
            "status": "COMPLIANT",
            "confidence": 0.72,
            "details": {"botanical_identity": "Cocos nucifera"},
        },
        "sesame oil": {
            "regulation": "Indian cosmetic compliance local table",
            "status": "COMPLIANT",
            "confidence": 0.70,
            "details": {"botanical_identity": "Sesamum indicum"},
        },
        "castor oil": {
            "regulation": "Indian cosmetic compliance local table",
            "status": "COMPLIANT",
            "confidence": 0.70,
            "details": {"botanical_identity": "Ricinus communis"},
        },
        "glycerin": {
            "regulation": "Indian cosmetic compliance local table",
            "status": "COMPLIANT",
            "confidence": 0.72,
        },
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)
