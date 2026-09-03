from fastapi import FastAPI

from app.database import get_connection


app = FastAPI(
    title="Retail Sales & Inventory API",
    description="API for retail sales and inventory analytics",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Retail Sales & Inventory API is running"
    }


@app.get("/kpis")
def get_kpis():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(DISTINCT orders.id),
            SUM(order_items.quantity),
            SUM(order_items.quantity * order_items.unit_price)
        FROM orders
        JOIN order_items
            ON orders.id = order_items.order_id
    """)

    orders, units_sold, revenue = cursor.fetchone()

    connection.close()

    average_ticket = revenue / orders

    return {
        "orders": orders,
        "units_sold": units_sold,
        "revenue": round(revenue, 2),
        "average_ticket": round(average_ticket, 2)
    }


@app.get("/products")
def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            unit_price
        FROM products
    """)

    products = cursor.fetchall()

    connection.close()

    return [
        {
            "id": product[0],
            "name": product[1],
            "category": product[2],
            "unit_price": product[3]
        }
        for product in products
    ]