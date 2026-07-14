from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


UNKNOWN = "UNKNOWN"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class EvidenceRecord:
    ingredient: str
    source: str
    regulation: str
    status: str = UNKNOWN
    confidence: float = 0.2
    references: list[str] = field(default_factory=list)
    evidence_type: str = "regulatory"
    details: dict[str, Any] = field(default_factory=dict)
    retrieved_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScoreContribution:
    score_name: str
    ingredient: str
    source: str
    regulation: str
    confidence: float
    contribution: float
    references: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

