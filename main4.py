from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import math

app = FastAPI()

# -------------------------
# Sample Products Data
# -------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"}
]

# -------------------------
# Orders Storage
# -------------------------
orders = []
order_counter = 1


class Order(BaseModel):
    customer_name: str
    product_id: int
    quantity: int


# -------------------------
# POST Create Order
# -------------------------
@app.post("/orders")
def create_order(order: Order):
    global order_counter

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "quantity": order.quantity
    }

    orders.append(new_order)
    order_counter += 1

    return {
        "message": "Order placed successfully",
        "order": new_order
    }


# -------------------------
# Product Search
# -------------------------
@app.get("/products/search")
def search_products(keyword: str):

    result = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }


# -------------------------
# Product Sort
# -------------------------
@app.get("/products/sort")
def sort_products(
        sort_by: str = "price",
        order: str = "asc"
):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    result = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": result
    }


# -------------------------
# Products Pagination
# -------------------------
@app.get("/products/page")
def paginate_products(
        page: int = 1,
        limit: int = 2
):

    total = len(products)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    result = products[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_products": total,
        "total_pages": total_pages,
        "products": result
    }


# -------------------------
# Q4 — Search Orders
# -------------------------
@app.get("/orders/search")
def search_orders(customer_name: str):

    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# -------------------------
# Q5 — Sort by Category
# -------------------------
@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(products, key=lambda p: (p["category"], p["price"]))

    return {
        "products": result,
        "total": len(result)
    }


# -------------------------
# Q6 — Browse Products
# Search + Sort + Pagination
# -------------------------
@app.get("/products/browse")
def browse_products(
        keyword: Optional[str] = None,
        sort_by: str = "price",
        order: str = "asc",
        page: int = 1,
        limit: int = 4
):

    result = products

    # Search
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # Sort
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    total_found = len(result)
    total_pages = math.ceil(total_found / limit)

    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paginated
    }


# -------------------------
# Bonus — Orders Pagination
# -------------------------
@app.get("/orders/page")
def paginate_orders(
        page: int = 1,
        limit: int = 3
):

    total = len(orders)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    result = orders[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_orders": total,
        "total_pages": total_pages,
        "orders": result
    }


# -------------------------
# Get Product by ID
# -------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Product not found"}
