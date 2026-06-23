from providers.regulatory_provider import RegulatoryProvider


class NinProvider(RegulatoryProvider):
    name = "NIN"
    source_url = "https://www.nin.res.in/"
    dataset_version = "nin-local-nutrient-reference-v1-2026-06"
    evidence_type = "nutrition"

    DATA = {
        "sugar": {"regulation": "Local nutrient reference table", "status": "REFERENCED", "confidence": 0.70, "details": {"nutrient": "free sugar"}},
        "salt": {"regulation": "Local nutrient reference table", "status": "REFERENCED", "confidence": 0.70, "details": {"nutrient": "sodium"}},
        "ascorbic acid": {"regulation": "Local nutrient reference table", "status": "REFERENCED", "confidence": 0.72, "details": {"nutrient": "vitamin C"}},
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

