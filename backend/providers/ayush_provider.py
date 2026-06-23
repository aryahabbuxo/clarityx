from providers.regulatory_provider import RegulatoryProvider


_CLAIM_POLICY = "No efficacy or medical claims generated"


class AyushProvider(RegulatoryProvider):
    name = "AYUSH"
    source_url = "https://www.ayush.gov.in/"
    dataset_version = "ayush-heritage-local-reference-v2-2026-06"
    evidence_type = "heritage"

    DATA = {
        # ── Original three ────────────────────────────────────────────────────
        "turmeric": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.85,
            "details": {
                "botanical_identity": "Curcuma longa",
                "sanskrit_name": "Haridra",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "neem": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.85,
            "details": {
                "botanical_identity": "Azadirachta indica",
                "sanskrit_name": "Nimba",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "aloe vera": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.82,
            "details": {
                "botanical_identity": "Aloe barbadensis",
                "sanskrit_name": "Kumari",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },

        # ── Newly added heritage ingredients ──────────────────────────────────
        "shikakai": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.85,
            "details": {
                "botanical_identity": "Acacia concinna",
                "sanskrit_name": "Shikakai",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "amla": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.88,
            "details": {
                "botanical_identity": "Emblica officinalis",
                "sanskrit_name": "Amalaki",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "ashwagandha": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.87,
            "details": {
                "botanical_identity": "Withania somnifera",
                "sanskrit_name": "Ashwagandha",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "tulsi": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.86,
            "details": {
                "botanical_identity": "Ocimum sanctum",
                "sanskrit_name": "Tulasi",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "bhringraj": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.83,
            "details": {
                "botanical_identity": "Eclipta alba",
                "sanskrit_name": "Bhringraj",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "licorice": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.84,
            "details": {
                "botanical_identity": "Glycyrrhiza glabra",
                "sanskrit_name": "Yashtimadhu",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "fenugreek": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.83,
            "details": {
                "botanical_identity": "Trigonella foenum-graecum",
                "sanskrit_name": "Methika",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "ginger": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.86,
            "details": {
                "botanical_identity": "Zingiber officinale",
                "sanskrit_name": "Sunthi",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "brahmi": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.84,
            "details": {
                "botanical_identity": "Bacopa monnieri",
                "sanskrit_name": "Brahmi",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "hibiscus": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.80,
            "details": {
                "botanical_identity": "Hibiscus rosa-sinensis",
                "sanskrit_name": "Jaswand",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "coconut oil": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.82,
            "details": {
                "botanical_identity": "Cocos nucifera",
                "sanskrit_name": "Narikela taila",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "sesame oil": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.82,
            "details": {
                "botanical_identity": "Sesamum indicum",
                "sanskrit_name": "Tila taila",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
        "castor oil": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.80,
            "details": {
                "botanical_identity": "Ricinus communis",
                "sanskrit_name": "Eranda taila",
                "traditional_system": "Ayurveda",
                "claim_policy": _CLAIM_POLICY,
            },
        },
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)
