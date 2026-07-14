from models.evidence import EvidenceRecord


class Gs1Provider:
    name = "GS1"
    source_url = "https://www.gs1.org/services/verified-by-gs1"

    def verify(self, barcode: str, manufacturer: str = "") -> dict:
        valid = self._valid_gtin(barcode)
        confidence = 0.70 if valid else 0.30
        status = "COMPLIANT" if valid else "UNKNOWN"
        return {
            "gtin_validity": valid,
            "manufacturer_verification": "UNKNOWN",
            "traceability_confidence": confidence,
            "source": self.source_url,
            "evidence": EvidenceRecord(
                ingredient="product identity",
                source=self.name,
                regulation="Verified by GS1 GTIN check digit",
                status=status,
                confidence=confidence,
                references=[self.source_url],
                evidence_type="traceability",
                details={"gtin": barcode, "manufacturer": manufacturer or "UNKNOWN"},
            ),
        }

    def _valid_gtin(self, barcode: str) -> bool:
        digits = [int(char) for char in str(barcode) if char.isdigit()]
        if len(digits) not in {8, 12, 13, 14}:
            return False
        body, check = digits[:-1], digits[-1]
        total = 0
        for index, digit in enumerate(reversed(body)):
            total += digit * (3 if index % 2 == 0 else 1)
        return (10 - (total % 10)) % 10 == check

