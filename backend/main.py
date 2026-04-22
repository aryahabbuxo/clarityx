from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from product_data import get_product
from scoring import sustainability_score, health_score, transparency_score, social_score, waspas_score
from greenwashing import extract_eco_claims, greenwashing_risk
from nlp import longevity_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ClarityX is running!"}

@app.get("/product/{barcode}")
def product(barcode: str, w1: float=0.25, w2: float=0.25, w3: float=0.25, w4: float=0.25):
    p = get_product(barcode)
    if not p:
        return {"error": "Product not found"}
    
    certs = p.get("labels_tags", [])
    ingredients = p.get("ingredients_text", "") or ""
    packaging = p.get("packaging", "") or ""
    brand = p.get("brands", "") or ""
    description = (p.get("generic_name", "") or "") + " " + (p.get("product_name", "") or "")

    s1 = sustainability_score(certs, packaging, ingredients)
    s2 = health_score(ingredients)
    s3 = transparency_score(certs, ingredients, packaging)
    s4 = social_score(certs, brand)
    composite = waspas_score([s1, s2, s3, s4], [w1, w2, w3, w4])
    
    claims = extract_eco_claims(description + " " + ingredients + " " + packaging)
    gw = greenwashing_risk(claims, certs, brand, packaging, ingredients)
    
    test_reviews = [
        f"This {p.get('product_name','product')} lasted a long time, great quality",
        f"The {p.get('product_name','product')} broke after one week, very cheap",
        f"Still using this after 6 months, very durable and sturdy",
        f"Fell apart quickly, not worth the money",
        f"Excellent product, months later still working perfectly"
    ]
    longevity = longevity_score(test_reviews)

    return {
        "name": p.get("product_name", "Unknown"),
        "brand": brand,
        "scores": {
            "sustainability": s1,
            "health": s2,
            "transparency": s3,
            "social": s4
        },
        "composite": composite,
        "greenwashing": gw,
        "longevity": longevity
    }

@app.get("/longevity/{barcode}")
def longevity_endpoint(barcode: str):
    p = get_product(barcode)
    if not p:
        return {"error": "Product not found"}
    test_reviews = [
        f"This {p.get('product_name','product')} lasted a long time, great quality",
        f"The {p.get('product_name','product')} broke after one week, very cheap",
        f"Still using this after 6 months, very durable and sturdy",
        f"Fell apart quickly, not worth the money",
        f"Excellent product, months later still working perfectly"
    ]
    result = longevity_score(test_reviews)
    return {
        "product": p.get("product_name", "Unknown"),
        "longevity": result
    }