from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models.evidence import EvidenceRecord, utc_now


CACHE_DIR = Path(__file__).resolve().parents[1] / "cache"


class RegulatoryProvider:
    name = "RegulatoryProvider"
    source_url = ""
    dataset_version = "local-2026-06"
    evidence_type = "regulatory"

    def lookup(self, ingredient) -> EvidenceRecord:
        cache_key = self.cache_key(ingredient.canonical_name)
        cached = self.read_cache(cache_key)
        if cached:
            return EvidenceRecord(**cached["normalized_response"])

        try:
            record = self._lookup(ingredient)
        except Exception as exc:
            record = EvidenceRecord(
                ingredient=ingredient.canonical_name,
                source=self.name,
                regulation="Provider lookup failed",
                status="UNKNOWN",
                confidence=0.2,
                references=[self.source_url] if self.source_url else [],
                evidence_type=self.evidence_type,
                details={"error": str(exc), "version": self.dataset_version},
            )
        self.write_cache(cache_key, raw_response=record.to_dict(), normalized_response=record.to_dict())
        return record

    def _lookup(self, ingredient) -> EvidenceRecord:
        return self.unknown(ingredient.canonical_name)

    def unknown(self, ingredient_name: str) -> EvidenceRecord:
        return EvidenceRecord(
            ingredient=ingredient_name,
            source=self.name,
            regulation="No matching regulator record",
            status="UNKNOWN",
            confidence=0.2,
            references=[self.source_url] if self.source_url else [],
            evidence_type=self.evidence_type,
            details={"version": self.dataset_version},
        )

    def from_local_record(self, ingredient_name: str, record: dict[str, Any]) -> EvidenceRecord:
        return EvidenceRecord(
            ingredient=ingredient_name,
            source=self.name,
            regulation=record["regulation"],
            status=record["status"],
            confidence=record.get("confidence", 0.7),
            references=record.get("references", [self.source_url]),
            evidence_type=record.get("evidence_type", self.evidence_type),
            details={**record.get("details", {}), "version": self.dataset_version},
        )

    def cache_key(self, ingredient_name: str) -> Path:
        safe = "".join(ch if ch.isalnum() else "_" for ch in ingredient_name.lower()).strip("_")
        return CACHE_DIR / f"{self.name.lower()}__{safe or 'unknown'}.json"

    def read_cache(self, path: Path) -> dict | None:
        if not path.exists():
            return None
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            # Invalidate cache if the dataset version has changed — ensures that
            # expanding a provider's DATA dict takes effect immediately without
            # requiring manual cache purges.
            if data.get("version") != self.dataset_version:
                return None
            return data
        except (OSError, json.JSONDecodeError):
            return None

    def write_cache(self, path: Path, raw_response: dict, normalized_response: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "provider": self.name,
            "raw_response": raw_response,
            "normalized_response": normalized_response,
            "timestamp": utc_now(),
            "version": self.dataset_version,
        }
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
