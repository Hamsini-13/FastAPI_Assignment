from fastapi import FastAPI

app = FastAPI()

# Product list
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": False},
    {"id": 4, "name": "Monitor", "price": 8999, "category": "Electronics", "in_stock": True},
    {"id": 5, "name": "Laptop Stand", "price": 799, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1499, "category": "Electronics", "in_stock": False}
]

# Q1 - Show all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# Q2 - Filter by category
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):

    filtered_products = [
        p for p in products if p["category"].lower() == category_name.lower()
    ]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {"products": filtered_products}


# Q3 - Show only in-stock products
@app.get("/products/instock")
def get_instock_products():

    instock = [p for p in products if p["in_stock"]]

    return {
        "in_stock_products": instock,
        "count": len(instock)
    }


# Q4 - Store summary
@app.get("/store/summary")
def store_summary():

    total_products = len(products)
    in_stock = len([p for p in products if p["in_stock"]])
    out_of_stock = total_products - in_stock
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }


# Q5 - Search products by name
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = [
        p for p in products if keyword.lower() in p["name"].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "total_matches": len(matched_products)
    }


# ⭐ Bonus - Cheapest and most expensive product
@app.get("/products/deals")
def get_deals():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }