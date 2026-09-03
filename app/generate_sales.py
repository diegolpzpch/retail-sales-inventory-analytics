import random
from datetime import datetime, timedelta

from app.database import get_connection


def generate_sales():
    random.seed(42)

    connection = get_connection()
    cursor = connection.cursor()

    # Avoid generating duplicate sales
    cursor.execute("SELECT COUNT(*) FROM orders")
    existing_orders = cursor.fetchone()[0]

    if existing_orders > 0:
        print("Sales already exist. No new sales were generated.")
        connection.close()
        return

    # Get customers
    cursor.execute("SELECT id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]

    # Get stores
    cursor.execute("SELECT id FROM stores")
    store_ids = [row[0] for row in cursor.fetchall()]

    # Get products and their prices
    cursor.execute("SELECT id, unit_price FROM products")
    products = cursor.fetchall()

    start_date = datetime(2025, 9, 1)
    end_date = datetime(2026, 8, 31)

    number_of_orders = 1500

    for _ in range(number_of_orders):

        customer_id = random.choice(customer_ids)
        store_id = random.choice(store_ids)

        random_days = random.randint(
            0,
            (end_date - start_date).days
        )

        order_date = start_date + timedelta(days=random_days)

        cursor.execute(
            """
            INSERT INTO orders
            (customer_id, store_id, order_date)
            VALUES (?, ?, ?)
            """,
            (
                customer_id,
                store_id,
                order_date.strftime("%Y-%m-%d")
            )
        )

        order_id = cursor.lastrowid

        number_of_products = random.randint(1, 4)

        selected_products = random.sample(
            products,
            number_of_products
        )

        for product_id, unit_price in selected_products:

            quantity = random.randint(1, 3)

            cursor.execute(
                """
                INSERT INTO order_items
                (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
                """,
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
            )

    connection.commit()
    connection.close()

    print(f"{number_of_orders} sales created successfully.")


if __name__ == "__main__":
    generate_sales()