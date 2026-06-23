from __future__ import annotations

from collections import defaultdict
from statistics import mean

from evidence_graph import EvidenceGraph
from models.evidence import EvidenceRecord, ScoreContribution


POSITIVE_STATUSES = {
    "APPROVED",
    "PERMITTED",
    "GRAS",
    "LISTED",
    "COMPLIANT",
    "REFERENCED",
    "IDENTIFIED",
}

RESTRICTED_STATUSES = {"RESTRICTED", "LIMITED", "CONDITIONAL"}
NEGATIVE_STATUSES = {"PROHIBITED", "BANNED", "NOT_PERMITTED"}


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


class ConfidenceEngine:
    SOURCE_CONFIDENCE = {
        frozenset({"EFSA", "FDA", "FSSAI"}): 0.95,
        frozenset({"EFSA", "FDA"}): 0.85,
        frozenset({"EFSA"}): 0.70,
    }

    @classmethod
    def confidence_for(cls, records: list[EvidenceRecord]) -> float:
        known_sources = {record.source for record in records if record.status != "UNKNOWN"}
        if not known_sources:
            return 0.20
        for sources, confidence in cls.SOURCE_CONFIDENCE.items():
            if sources.issubset(known_sources):
                return confidence
        return round(min(0.80, 0.45 + (0.08 * len(known_sources))), 2)


class EvidenceScore:
    name = "EvidenceScore"
    sources: set[str] = set()
    evidence_types: set[str] = set()
    positive_weight = 8
    restricted_weight = -8
    negative_weight = -20
    baseline = 70

    def __init__(self, graph: EvidenceGraph):
        self.graph = graph

    def relevant_records(self) -> list[EvidenceRecord]:
        records = []
        for record in self.graph.records:
            source_match = not self.sources or record.source in self.sources
            type_match = not self.evidence_types or record.evidence_type in self.evidence_types
            if source_match and type_match:
                records.append(record)
        return records

    def contribution_for(self, record: EvidenceRecord) -> float:
        status = record.status.upper()
        if status in POSITIVE_STATUSES:
            return self.positive_weight * record.confidence
        if status in RESTRICTED_STATUSES:
            return self.restricted_weight * record.confidence
        if status in NEGATIVE_STATUSES:
            return self.negative_weight * record.confidence
        return 0

    def score(self) -> dict:
        records = self.relevant_records()
        score = self.baseline
        source_breakdown: dict[str, float] = defaultdict(float)

        for record in records:
            contribution = self.contribution_for(record)
            score += contribution
            source_breakdown[record.source] += contribution
            self.graph.add_contribution(ScoreContribution(
                score_name=self.name,
                ingredient=record.ingredient,
                source=record.source,
                regulation=record.regulation,
                confidence=record.confidence,
                contribution=round(contribution, 2),
                references=record.references,
            ))

        known = [record for record in records if record.status != "UNKNOWN"]
        return {
            "score": round(clamp(score), 1),
            "confidence": ConfidenceEngine.confidence_for(records),
            "evidence": [record.to_dict() for record in known],
            "source": ", ".join(sorted({record.source for record in known})) or "No regulator evidence",
            "references": sorted({ref for record in known for ref in record.references}),
            "source_breakdown": {key: round(value, 2) for key, value in source_breakdown.items()},
        }


class RegulatoryComplianceScore(EvidenceScore):
    name = "RegulatoryComplianceScore"
    sources = {"FDA", "Codex", "FSSAI", "REACH", "CDSCO"}
    evidence_types = {"compliance", "regulatory", "cosmetic_safety"}
    baseline = 72


class IngredientSafetyScore(EvidenceScore):
    name = "IngredientSafetyScore"
    sources = {"EFSA", "FDA", "REACH"}
    evidence_types = {"food_safety", "cosmetic_safety", "regulatory"}
    baseline = 68


class NutritionalQualityScore(EvidenceScore):
    name = "NutritionalQualityScore"
    sources = {"NIN"}
    evidence_types = {"nutrition"}
    baseline = 60
    positive_weight = 6
    restricted_weight = 0
    negative_weight = 0


class CertificationCredibilityScore(EvidenceScore):
    name = "CertificationCredibilityScore"
    sources = {"Codex", "FSSAI", "CDSCO"}
    evidence_types = {"certification", "compliance"}
    baseline = 50


class HeritageAuthenticityScore(EvidenceScore):
    name = "HeritageAuthenticityScore"
    sources = {"AYUSH"}
    evidence_types = {"heritage"}
    baseline = 50
    positive_weight = 12
    restricted_weight = 0
    negative_weight = 0


class TransparencyScore(EvidenceScore):
    name = "TransparencyScore"
    baseline = 40

    def score(self) -> dict:
        records = self.graph.records
        known = [record for record in records if record.status != "UNKNOWN"]
        ingredients = {record.ingredient for record in records}
        covered = {record.ingredient for record in known}
        coverage = (len(covered) / len(ingredients)) if ingredients else 0
        source_count = len({record.source for record in known})
        value = clamp(35 + coverage * 45 + min(source_count * 3, 20))
        for record in known:
            self.graph.add_contribution(ScoreContribution(
                score_name=self.name,
                ingredient=record.ingredient,
                source=record.source,
                regulation=record.regulation,
                confidence=record.confidence,
                contribution=round(value / max(len(known), 1), 2),
                references=record.references,
            ))
        return {
            "score": round(value, 1),
            "confidence": ConfidenceEngine.confidence_for(records),
            "evidence": [record.to_dict() for record in known],
            "source": ", ".join(sorted({record.source for record in known})) or "No regulator evidence",
            "references": sorted({ref for record in known for ref in record.references}),
            "source_breakdown": {"coverage": round(coverage, 2), "sources": source_count},
        }


class TraceabilityConfidenceScore(EvidenceScore):
    name = "TraceabilityConfidenceScore"
    sources = {"GS1"}
    evidence_types = {"traceability"}
    baseline = 30
    positive_weight = 45
    restricted_weight = 0
    negative_weight = -10


SCORE_CLASSES = (
    RegulatoryComplianceScore,
    IngredientSafetyScore,
    NutritionalQualityScore,
    CertificationCredibilityScore,
    HeritageAuthenticityScore,
    TransparencyScore,
    TraceabilityConfidenceScore,
)


def score_evidence_graph(graph: EvidenceGraph) -> dict:
    scores = {score_cls.name: score_cls(graph).score() for score_cls in SCORE_CLASSES}
    composite = round(mean(item["score"] for item in scores.values()), 1)
    confidence = round(mean(item["confidence"] for item in scores.values()), 2)
    return {
        "score": composite,
        "confidence": confidence,
        "scores": scores,
        "evidence": graph.to_dict(),
    }
