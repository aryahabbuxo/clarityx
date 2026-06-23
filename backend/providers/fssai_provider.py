from providers.regulatory_provider import RegulatoryProvider


class FssaiProvider(RegulatoryProvider):
    name = "FSSAI"
    source_url = "https://www.fssai.gov.in/"
    dataset_version = "fssai-additive-compliance-local-v1-2026-06"
    evidence_type = "compliance"

    DATA = {
        "citric acid": {"regulation": "Additive permission local table", "status": "PERMITTED", "confidence": 0.82},
        "sodium benzoate": {"regulation": "Additive restriction local table", "status": "RESTRICTED", "confidence": 0.80},
        "ascorbic acid": {"regulation": "Additive permission local table", "status": "PERMITTED", "confidence": 0.82},
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

