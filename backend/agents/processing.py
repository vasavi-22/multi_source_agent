from typing import List, Dict
from datetime import datetime

def normalize_price(price: str):
    if not price:
        return None
    # Remove any non-digit and non-dot characters
    cleaned = "".join(c for c in price if c.isdigit() or c == ".")
    try: 
        return float(cleaned)
    except ValueError:
        return None
    
def clean_products(products: List[Dict]):
    seen = set()
    cleaned_data = []

    for product in products:
        name = product.get("title")
        price = normalize_price(product.get("price"))
        store = product.get("url", "Test Store")
        timestamp = timestamp = product.get("timeStamp") or product.get("timestamp")

        if not name or price is None:
            continue

        # Remove duplicates (same name + store)
        unique_key = (name.lower(), store.lower())
        if unique_key in seen:
            continue
        seen.add(unique_key)
        cleaned_data.append({
            "name": name,
            "price": price,
            "store": store,
            "timestamp": timestamp or datetime.now().isoformat()
        })
    return cleaned_data

def structure_products_data(products: List[Dict]):
    cleaned_products = clean_products(products)
    structured = []

    for product in cleaned_products:
        structured.append({
            "product_node": {
                "name": product.get("name"),
                "price": product.get("price"),
                "store": product.get("store"),
                "timestamp": product.get("timestamp")
            }
        })
    return structured

# FINANCE PROCESSING
def structure_stock_data(stock_data):
    structured = []
    for item in stock_data:
        structured.append({
            "stock_node": item
        })
    return structured


def structure_forex_data(forex_data):
    structured = []
    for item in forex_data:
        structured.append({
            "forex_node": item
        })
    return structured
