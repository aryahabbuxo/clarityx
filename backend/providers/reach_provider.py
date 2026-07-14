from providers.regulatory_provider import RegulatoryProvider


class ReachProvider(RegulatoryProvider):
    name = "REACH"
    source_url = "https://echa.europa.eu/information-on-chemicals"
    dataset_version = "reach-local-reference-2026-06"
    evidence_type = "cosmetic_safety"

    DATA = {
        "citric acid": {"regulation": "ECHA chemical information record", "status": "LISTED", "confidence": 0.78},
        "sodium benzoate": {"regulation": "ECHA chemical information record", "status": "LISTED", "confidence": 0.78},
        "water": {"regulation": "Cosmetic ingredient identity", "status": "LISTED", "confidence": 0.70},
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

