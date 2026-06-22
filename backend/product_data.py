import os
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# ── API Keys ──────────────────────────────────────────────────────────────────
# Prefer environment variable so the key stays out of source control.

load_dotenv()
GO_UPC_API_KEY = os.environ.get("GO_UPC_API_KEY", "")

_HEADERS = {"User-Agent": "ClarityX/1.0"}


# ── Source fetchers ───────────────────────────────────────────────────────────

def _fetch_open_food_facts(barcode: str) -> dict | None:
    """
    Open Food Facts – broadest coverage, richest nutrition / eco-score data.
    Returns the product dict on success, None otherwise.
    """
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        r = requests.get(url, headers=_HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == 1:
                product = data["product"]
                product["_source"] = "open-food-facts"
                return product
    except Exception as e:
        print(f"[OFF] Error fetching {barcode}: {e}")
    return None


def _fetch_open_beauty_facts(barcode: str) -> dict | None:
    """
    Open Beauty Facts – cosmetics and personal-care products.
    Schema is identical to OFF so no normalisation is needed.
    Returns the product dict on success, None otherwise.
    """
    url = f"https://world.openbeautyfacts.org/api/v2/product/{barcode}.json"
    try:
        r = requests.get(url, headers=_HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == 1:
                product = data["product"]
                product["_source"] = "open-beauty-facts"
                return product
    except Exception as e:
        print(f"[OBF] Error fetching {barcode}: {e}")
    return None


def _fetch_go_upc(barcode: str) -> dict | None:
    """
    Go-UPC – general product database covering food, electronics, and more.
    API key is quota-limited to 150 requests, so this is used only as a
    last resort when both OFF and OBF return nothing.
    Returns a normalised product dict on success, None otherwise.
    """
    if not GO_UPC_API_KEY:
        return None

    url = f"https://api.go-upc.com/product/{barcode}"
    try:
        r = requests.get(
            url,
            headers={**_HEADERS, "Authorization": f"Bearer {GO_UPC_API_KEY}"},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("ok") and data.get("product"):
                return _normalize_go_upc(data["product"])
            if data.get("limitReached"):
                print("[GoUPC] Monthly quota exhausted.")
    except Exception as e:
        print(f"[GoUPC] Error fetching {barcode}: {e}")
    return None


def _normalize_go_upc(p: dict) -> dict:
    """
    Map a Go-UPC product response to the OFF-compatible schema that main.py
    expects.  Go-UPC exposes extra metadata in a `specs` list of
    {"key": ..., "value": ...} dicts, which we flatten to a lookup dict.
    """
    # Flatten the specs list → easy key-based lookup
    specs: dict = {}
    for item in (p.get("specs") or []):
        key = item.get("key", "").lower().strip()
        val = item.get("value", "")
        if key and val:
            specs[key] = val

    # Resolve ingredient and packaging text from multiple possible spec keys
    ingredients = (
        p.get("ingredients")
        or specs.get("ingredients")
        or specs.get("ingredient list")
        or ""
    )
    packaging = (
        specs.get("packaging")
        or specs.get("material")
        or specs.get("container")
        or ""
    )

    return {
        "product_name":    p.get("name", ""),
        "generic_name":    p.get("description") or p.get("alias") or "",
        "brands":          p.get("brand", ""),
        "ingredients_text": ingredients,
        "labels_tags":     [],   # Go-UPC has no certification tags
        "packaging":       packaging,
        "image_url":       p.get("imageUrl", ""),
        "_source":         "go-upc",
    }


def _fetch_upcitemdb(barcode: str) -> dict | None:
    """Query UPCitemdb's quota-limited trial endpoint as a general fallback."""
    try:
        r = requests.get(
            "https://api.upcitemdb.com/prod/trial/lookup",
            params={"upc": barcode}, headers=_HEADERS, timeout=10
        )
        if r.status_code == 200:
            items = r.json().get("items") or []
            if items:
                return _normalize_upcitemdb(items[0])
        elif r.status_code == 429:
            print("[UPCitemdb] Daily trial quota exhausted.")
    except Exception as e:
        print(f"[UPCitemdb] Error fetching {barcode}: {e}")
    return None


def _normalize_upcitemdb(p: dict) -> dict:
    return {
        "product_name": p.get("title", ""),
        "generic_name": p.get("description", ""),
        "brands": p.get("brand", ""),
        "ingredients_text": p.get("ingredients", ""),
        "labels_tags": [],
        "packaging": p.get("size", ""),
        "image_url": (p.get("images") or [""])[0],
        "_source": "upcitemdb",
    }


def enrich_with_openfda(product: dict) -> dict:
    """Add medicine-label ingredients when a resolved product name matches OpenFDA.

    OpenFDA has no UPC/EAN barcode lookup, so this is an enrichment after a
    catalogue identifies the product, never a potentially unrelated fallback.
    """
    name = (product.get("product_name") or "").strip()
    if not name:
        return product
    try:
        r = requests.get(
            "https://api.fda.gov/drug/label.json",
            params={"search": f'openfda.brand_name.exact:"{name}"', "limit": 1},
            headers=_HEADERS, timeout=8,
        )
        results = r.json().get("results") if r.status_code == 200 else None
        if not results:
            return product
        label = results[0]
        active = "; ".join(label.get("active_ingredient") or [])
        inactive = "; ".join(label.get("inactive_ingredient") or [])
        label_text = "; ".join(part for part in (active, inactive) if part)
        if label_text:
            product["ingredients_text"] = " ; ".join(
                part for part in (product.get("ingredients_text", ""), label_text) if part
            )
        product["_source"] = f"{product.get('_source', '')} + openfda".strip(" +")
        product["openfda_label"] = {"active_ingredients": active, "inactive_ingredients": inactive}
    except Exception as e:
        print(f"[OpenFDA] Error enriching {name}: {e}")
    return product


# ── Merge helper ──────────────────────────────────────────────────────────────

def _merge(primary: dict, fallback: dict) -> dict:
    """
    Merge two product dicts so the richest possible data is returned.

    Rules:
    - String fields  → primary wins; fallback fills only when primary is empty.
    - List fields    → union of both lists (e.g. labels_tags from two sources).
    - All other types → primary wins unconditionally.
    """
    result = dict(primary)
    for key, fb_val in fallback.items():
        pri_val = result.get(key)

        if isinstance(pri_val, list) and isinstance(fb_val, list):
            # Union: keep all unique tags/labels from both sources
            seen = set(pri_val)
            result[key] = list(pri_val) + [v for v in fb_val if v not in seen]
        elif not pri_val and fb_val:
            # Primary field is empty — use fallback value
            result[key] = fb_val

    # Record that both sources contributed
    sources = [primary.get("_source", ""), fallback.get("_source", "")]
    result["_source"] = " + ".join(s for s in sources if s)
    return result


# ── Public API ────────────────────────────────────────────────────────────────

def get_product(barcode: str) -> dict | None:
    """
    Fetch and return product data for a given barcode.

    Database priority:
      1. Open Food Facts  — primary for food/grocery (richest eco + nutrition data)
      2. Open Beauty Facts — primary for cosmetics; also fills gaps in OFF results
      3. Go-UPC            — general fallback; used only when both above return nothing
                             (conserves the 150-request monthly quota)

    When both OFF and OBF find the same product, their data is merged so that
    certifications (labels_tags) and any missing text fields are combined rather
    than discarded.
    """
    # These independent open databases are queried together, cutting the normal
    # lookup wait from two sequential requests to roughly one request timeout.
    with ThreadPoolExecutor(max_workers=2) as executor:
        off_future = executor.submit(_fetch_open_food_facts, barcode)
        obf_future = executor.submit(_fetch_open_beauty_facts, barcode)
        off = off_future.result()
        obf = obf_future.result()

    if off and obf:
        # Both sources found the product — merge for maximum richness
        return enrich_with_openfda(_merge(off, obf))

    if off:
        return enrich_with_openfda(off)

    if obf:
        return enrich_with_openfda(obf)

    # Neither open database found the product — try Go-UPC as last resort
    print(f"[product_data] OFF and OBF both missed {barcode}. Trying Go-UPC (quota: 150).")
    upcitemdb = _fetch_upcitemdb(barcode)
    if upcitemdb:
        return enrich_with_openfda(upcitemdb)

    go_upc = _fetch_go_upc(barcode)
    return enrich_with_openfda(go_upc) if go_upc else None
