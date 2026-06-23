from __future__ import annotations

from evidence_graph import EvidenceGraph


def extract_marketing_claims(claims: list[str] | None = None) -> list[str]:
    """Accept explicit claims only; do not infer claims from OFF/OBF metadata."""
    return [claim.strip() for claim in (claims or []) if claim and claim.strip()]


def greenwashing_risk(marketing_claims: list[str], graph: EvidenceGraph) -> dict:
    verified_sources = {
        record.source
        for record in graph.known_records()
        if record.evidence_type in {"compliance", "certification", "traceability"}
    }
    unverified_claims = extract_marketing_claims(marketing_claims)
    risk_points = max(0, len(unverified_claims) - len(verified_sources))

    if risk_points >= 3:
        risk = "High"
    elif risk_points >= 1:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "risk": risk,
        "risk_points": risk_points,
        "formula": "Unverified Marketing Claims minus Verified Regulatory Evidence",
        "unverified_claims": unverified_claims,
        "verified_regulatory_sources": sorted(verified_sources),
        "reason": "Risk is based only on explicit unverified claims and regulator evidence coverage.",
    }

