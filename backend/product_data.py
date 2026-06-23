from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import requests


_HEADERS = {"User-Agent": "ClarityX/2.0 evidence-engine"}


def _identity_from_off_product(product: dict, barcode: str, source: str) -> dict:
    return {
        "barcode": barcode,
        "gtin": barcode,
        "product_name": product.get("product_name", "") or product.get("generic_name", "") or "Unknown",
        "manufacturer": product.get("brands", "") or product.get("manufacturing_places", "") or "Unknown",
        "ingredients": product.get("ingredients_text", "") or "",
        "category": ", ".join(product.get("categories_tags") or []) or product.get("categories", "") or "Unknown",
        "source": source,
    }


def _fetch_open_food_facts(barcode: str) -> dict | None:
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, headers=_HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                return _identity_from_off_product(data["product"], barcode, "Open Food Facts")
    except Exception as exc:
        print(f"[OFF] identity lookup failed for {barcode}: {exc}")
    return None


def _fetch_open_beauty_facts(barcode: str) -> dict | None:
    url = f"https://world.openbeautyfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, headers=_HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                return _identity_from_off_product(data["product"], barcode, "Open Beauty Facts")
    except Exception as exc:
        print(f"[OBF] identity lookup failed for {barcode}: {exc}")
    return None


def get_product_identity(barcode: str) -> dict | None:
    """Layer 1: identify a product only. No score inputs are derived here."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        off_future = executor.submit(_fetch_open_food_facts, barcode)
        obf_future = executor.submit(_fetch_open_beauty_facts, barcode)
        off = off_future.result()
        obf = obf_future.result()

    return off or obf


def get_product(barcode: str) -> dict | None:
    return get_product_identity(barcode)

