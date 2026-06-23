from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from models.evidence import EvidenceRecord, ScoreContribution


GRAPH_PATH = Path(__file__).resolve().parent / "evidence" / "evidence_graph.jsonl"


class EvidenceGraph:
    """System of record for regulator evidence and score contributions."""

    def __init__(self, product_id: str, persist_path: Path = GRAPH_PATH):
        self.product_id = product_id
        self.persist_path = persist_path
        self.records: list[EvidenceRecord] = []
        self.contributions: list[ScoreContribution] = []

    def add_records(self, records: Iterable[EvidenceRecord]) -> None:
        for record in records:
            self.records.append(record)

    def add_contribution(self, contribution: ScoreContribution) -> None:
        self.contributions.append(contribution)

    def by_ingredient(self) -> dict[str, list[EvidenceRecord]]:
        grouped: dict[str, list[EvidenceRecord]] = defaultdict(list)
        for record in self.records:
            grouped[record.ingredient].append(record)
        return dict(grouped)

    def by_source(self) -> dict[str, list[EvidenceRecord]]:
        grouped: dict[str, list[EvidenceRecord]] = defaultdict(list)
        for record in self.records:
            grouped[record.source].append(record)
        return dict(grouped)

    def known_records(self) -> list[EvidenceRecord]:
        return [record for record in self.records if record.status != "UNKNOWN"]

    def persist(self) -> None:
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        payload = self.to_dict()
        with self.persist_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "evidence": [record.to_dict() for record in self.records],
            "score_contributions": [item.to_dict() for item in self.contributions],
        }

