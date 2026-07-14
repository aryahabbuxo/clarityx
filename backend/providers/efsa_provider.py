from providers.regulatory_provider import RegulatoryProvider


class EfsaProvider(RegulatoryProvider):
    name = "EFSA"
    source_url = "https://www.efsa.europa.eu/en/data-report/chemical-hazards-database-openfoodtox"
    dataset_version = "openfoodtox-local-reference-2026-06"
    evidence_type = "food_safety"

    DATA = {
        "citric acid": {
            "regulation": "OpenFoodTox reference value available",
            "status": "APPROVED",
            "confidence": 0.94,
            "details": {"ADI": "not specified", "NOAEL": "not specified", "toxicology_endpoints": ["acidity regulator"]},
        },
        "sodium benzoate": {
            "regulation": "OpenFoodTox hazard and reference value record",
            "status": "RESTRICTED",
            "confidence": 0.90,
            "details": {"ADI": "0-5 mg/kg bw/day", "NOAEL": "provider reference required", "toxicology_endpoints": ["preservative exposure"]},
        },
        "ascorbic acid": {
            "regulation": "OpenFoodTox reference value available",
            "status": "APPROVED",
            "confidence": 0.92,
            "details": {"ADI": "not specified", "NOAEL": "not specified", "toxicology_endpoints": ["antioxidant"]},
        },
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

