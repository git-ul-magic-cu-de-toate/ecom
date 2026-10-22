import requests
import csv
import json

SHOP_NAME = 'IceFit'
ACCESS_TOKEN = 'SHOPIFY_TOKEN_AICI'

BASE_URL = f"https://dyxifg-aj.myshopify.com/admin/api/2025-04"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json; charset=utf-8"
}

def get_all_products():
    url = f"{BASE_URL}/products.json?limit=250"
    products_response = requests.get(url, headers=HEADERS)
    products_data = products_response.json().get("products", [])

    products_export = []

    for product in products_data:
        title = product.get("title")
        vendor = product.get("vendor")
        category = product.get("product_type")
        image_url = product.get("image", {}).get("src", "")
        handle = product.get("handle", "")
        base_url = f"https://{SHOP_NAME.lower()}.myshopify.com/products/{handle}"

        for variant in product.get("variants", []):
            products_export.append({
                "Title": title,
                "SKU": variant.get("sku"),
                "Vendor": vendor,
                "Category": category,
                "Price": variant.get("price"),
                "Product URL": base_url,
                "Image URL": image_url,
                "Variant Title": variant.get("title"),
                "Option1": variant.get("option1"),
                "Option2": variant.get("option2"),
                "Option3": variant.get("option3")
            })

    return products_export

def export_to_csv(products, filename="export_all_variants.csv"):
    if not products:
        print("Data not found")
        return

    fieldnames = list(products[0].keys())

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

    print(f"Data export complete in CSV: {filename}")

def export_to_json(products, filename="export_all_variants.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=2, ensure_ascii=False)

    print(f"Data export complete in JSON: {filename}")

products = get_all_products()
export_to_csv(products)
export_to_json(products)
