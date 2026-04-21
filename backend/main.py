from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from product_data import get_product

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
def product(barcode: str):
    p = get_product(barcode)
    if not p:
        return {"error": "Product not found"}
    return {
        "name": p.get("product_name", "Unknown"),
        "brand": p.get("brands", "Unknown"),
        "certifications": p.get("labels_tags", []),
        "ingredients": p.get("ingredients_text", ""),
        "packaging": p.get("packaging", "")
    }