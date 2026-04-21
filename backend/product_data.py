import requests

def get_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"
    headers = {"User-Agent": "ClarityX/1.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        if data.get("status") == 1:
            return data["product"]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None