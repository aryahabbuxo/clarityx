from providers.regulatory_provider import RegulatoryProvider


class CodexProvider(RegulatoryProvider):
    name = "Codex"
    source_url = "https://www.fao.org/fao-who-codexalimentarius/en/"
    dataset_version = "codex-gsfa-local-reference-2026-06"
    evidence_type = "compliance"

    DATA = {
        "citric acid": {"regulation": "INS 330 acidity regulator", "status": "PERMITTED", "confidence": 0.88, "details": {"INS": "330"}},
        "sodium benzoate": {"regulation": "INS 211 preservative with category limits", "status": "RESTRICTED", "confidence": 0.86, "details": {"INS": "211"}},
        "ascorbic acid": {"regulation": "INS 300 antioxidant", "status": "PERMITTED", "confidence": 0.88, "details": {"INS": "300"}},
    }

    def _lookup(self, ingredient):
        record = self.DATA.get(ingredient.canonical_name)
        return self.from_local_record(ingredient.canonical_name, record) if record else self.unknown(ingredient.canonical_name)

