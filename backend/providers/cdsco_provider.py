from providers.regulatory_provider import RegulatoryProvider


class CdscoProvider(RegulatoryProvider):
    name = "CDSCO"
    source_url = "https://cdsco.gov.in/"
    dataset_version = "cdsco-cosmetic-compliance-local-v1-2026-06"
    evidence_type = "compliance"

    DATA = {
        "water": {"regulation": "Indian cosmetic compliance local table", "status": "COMPLIANT", "confidence": 0.66},
        "aloe vera": {"regulation": "Indian cosmetic botanical identity local table", "status": "COMPLIANT", "confidence": 0.66},
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

