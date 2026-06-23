from providers.regulatory_provider import RegulatoryProvider


class AyushProvider(RegulatoryProvider):
    name = "AYUSH"
    source_url = "https://www.ayush.gov.in/"
    dataset_version = "ayush-heritage-local-reference-v1-2026-06"
    evidence_type = "heritage"

    DATA = {
        "turmeric": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.78,
            "details": {"botanical_identity": "Curcuma longa", "sanskrit_name": "Haridra", "claim_policy": "No efficacy or medical claims generated"},
        },
        "neem": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.76,
            "details": {"botanical_identity": "Azadirachta indica", "sanskrit_name": "Nimba", "claim_policy": "No efficacy or medical claims generated"},
        },
        "aloe vera": {
            "regulation": "Botanical identity heritage reference",
            "status": "IDENTIFIED",
            "confidence": 0.74,
            "details": {"botanical_identity": "Aloe barbadensis", "sanskrit_name": "Kumari", "claim_policy": "No efficacy or medical claims generated"},
        },
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

