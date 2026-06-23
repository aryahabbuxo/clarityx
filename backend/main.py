from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from evidence_engine import EvidenceEngine
from greenwashing import greenwashing_risk
from ingredient_resolver import resolve_ingredients
from product_data import get_product_identity
from providers.gs1_provider import Gs1Provider
from scoring import score_evidence_graph


app = FastAPI()
SCORE_SCHEMA_VERSION = 1

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ClarityX evidence engine is running"}


@app.get("/product/{barcode}")
def product(barcode: str):
    identity = get_product_identity(barcode)
    if not identity:
        return {"error": "Product not found"}

    canonical_ingredients = resolve_ingredients(identity.get("ingredients", ""))
    gs1 = Gs1Provider().verify(barcode, identity.get("manufacturer", ""))
    graph = EvidenceEngine().build_graph(
        product_id=barcode,
        ingredients=canonical_ingredients,
        traceability_evidence=gs1["evidence"],
    )
    score_result = score_evidence_graph(graph)
    graph.persist()

    greenwashing = greenwashing_risk(marketing_claims=[], graph=graph)

    numeric_scores = {
        "regulatory_compliance": score_result["scores"]["RegulatoryComplianceScore"]["score"],
        "ingredient_safety": score_result["scores"]["IngredientSafetyScore"]["score"],
        "nutritional_quality": score_result["scores"]["NutritionalQualityScore"]["score"],
        "certification_credibility": score_result["scores"]["CertificationCredibilityScore"]["score"],
        "heritage_authenticity": score_result["scores"]["HeritageAuthenticityScore"]["score"],
        "transparency": score_result["scores"]["TransparencyScore"]["score"],
        "traceability_confidence": score_result["scores"]["TraceabilityConfidenceScore"]["score"],
    }

    return {
        "identity": identity,
        "name": identity["product_name"],
        "brand": identity["manufacturer"],
        "score_schema_version": SCORE_SCHEMA_VERSION,
        "score": score_result["score"],
        "confidence": score_result["confidence"],
        "scores": numeric_scores,
        "score_details": score_result["scores"],
        "source": "Evidence graph",
        "evidence": score_result["evidence"]["evidence"],
        "evidence_graph": score_result["evidence"],
        "ingredients": [ingredient.to_dict() for ingredient in canonical_ingredients],
        "traceability": {
            "gtin_validity": gs1["gtin_validity"],
            "manufacturer_verification": gs1["manufacturer_verification"],
            "traceability_confidence": gs1["traceability_confidence"],
            "source": gs1["source"],
        },
        "greenwashing": greenwashing,
        "data_sources": {
            "identity": identity["source"],
            "evidence": ["EFSA", "FDA", "Codex", "FSSAI", "REACH", "CDSCO", "AYUSH", "NIN", "GS1"],
        },
        "principle": "Identity databases identify products; regulatory databases evaluate ingredients; scores are generated from evidence.",
    }


@app.get("/longevity/{barcode}")
def longevity_endpoint(barcode: str):
    identity = get_product_identity(barcode)
    if not identity:
        return {"error": "Product not found"}
    return {
        "product": identity.get("product_name", "Unknown"),
        "longevity": {"label": "Not assessed", "reason": "No verified, attributable review source is connected."},
    }
