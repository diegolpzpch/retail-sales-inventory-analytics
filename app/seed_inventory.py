import random

from app.database import get_connection


def seed_inventory():
    random.seed(42)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM stores")
    store_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]

    inventory_records = []

    for store_id in store_ids:
        for product_id in product_ids:
            stock_quantity = random.randint(5, 150)

            inventory_records.append(
                (store_id, product_id, stock_quantity)
            )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO inventory
        (store_id, product_id, stock_quantity)
        VALUES (?, ?, ?)
        """,
        inventory_records
    )

    connection.commit()
    connection.close()

    print("Inventory created successfully.")


if __name__ == "__main__":
    seed_inventory()