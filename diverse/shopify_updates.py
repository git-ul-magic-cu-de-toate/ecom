import requests

ACCESS_TOKEN = 'SHOPIFY_TOKEN_AICI'
SKU_TO_UPDATE = 'PROT-GOLD-C-3'
NEW_PRICE = 10000
NEW_STOCK = 10000

BASE_URL = f"https://dyxifg-aj.myshopify.com/admin/api/2025-04"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json; charset=utf-8",
}

product_id = None
variant_id = None
inventory_item_id = None

products = requests.get(f"{BASE_URL}/products.json", headers=HEADERS)
products_data = products.json().get("products", [])

for product in products_data:
    for variant in product.get("variants", []):
        if variant.get("sku") == SKU_TO_UPDATE:
            product_id = product["id"]
            variant_id = variant["id"]
            inventory_item_id = variant["inventory_item_id"]
            print(f"Product: {product['title']}")
            print(f"Variant ID: {variant_id}")
            break
    if variant_id:
        break

if not variant_id:
    print("Variant ID not found for SKU:", SKU_TO_UPDATE)
    exit()

if NEW_PRICE is not None:
    update_price = {
        "variant": {
            "id": variant_id,
            "price": str(NEW_PRICE)
        }
    }

    response = requests.put(
        f"{BASE_URL}/variants/{variant_id}.json",
        headers=HEADERS,
        json=update_price
    )

    if response.status_code == 200:
        print(f"Price updated to {NEW_PRICE} RON")
    else:
        print("Error updating price:", response.text)

if NEW_STOCK is not None:
    loc_resp = requests.get(f"{BASE_URL}/locations.json", headers=HEADERS)
    location_id = loc_resp.json()["locations"][0]["id"]

    update_stock = {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": NEW_STOCK
    }

    stock_response = requests.post(
        f"{BASE_URL}/inventory_levels/set.json",
        headers=HEADERS,
        json=update_stock
    )

    if stock_response.status_code == 200:
        print(f"Stock updated to {NEW_STOCK} units")
    else:
        print("Error updating stock:", stock_response.text)
