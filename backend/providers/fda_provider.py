from providers.regulatory_provider import RegulatoryProvider


class FdaProvider(RegulatoryProvider):
    name = "FDA"
    source_url = "https://open.fda.gov/apis/"
    dataset_version = "fda-food-substances-local-reference-2026-06"

    DATA = {
        "citric acid": {"regulation": "Food substance listing", "status": "GRAS", "confidence": 0.86},
        "sodium benzoate": {"regulation": "Food preservative listing", "status": "GRAS", "confidence": 0.82},
        "ascorbic acid": {"regulation": "Food substance listing", "status": "GRAS", "confidence": 0.86},
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

