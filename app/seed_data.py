from app.database import get_connection


def seed_data():
    connection = get_connection()
    cursor = connection.cursor()

    products = [
        ("Laptop Pro", "Electronics", 999.99),
        ("Gaming Mouse", "Electronics", 49.99),
        ("Mechanical Keyboard", "Electronics", 89.99),
        ("27-inch Monitor", "Electronics", 249.99),
        ("Office Chair", "Furniture", 199.99),
        ("Standing Desk", "Furniture", 349.99),
        ("Air Fryer", "Home", 129.99),
        ("Coffee Maker", "Home", 79.99),
        ("Running Shoes", "Sports", 109.99),
        ("Yoga Mat", "Sports", 39.99)
    ]

    stores = [
        ("Providencia Store", "Santiago"),
        ("Las Condes Store", "Santiago"),
        ("Viña del Mar Store", "Viña del Mar"),
        ("Concepción Store", "Concepción")
    ]

    customers = [
        ("Diego López", "Regular"),
        ("Camila Soto", "Premium"),
        ("Matías Rojas", "Regular"),
        ("Fernanda Silva", "Premium"),
        ("Tomás González", "Regular"),
        ("Valentina Pérez", "Premium")
    ]

    cursor.executemany(
        "INSERT INTO products (name, category, unit_price) VALUES (?, ?, ?)",
        products
    )

    cursor.executemany(
        "INSERT INTO stores (name, city) VALUES (?, ?)",
        stores
    )

    cursor.executemany(
        "INSERT INTO customers (name, segment) VALUES (?, ?)",
        customers
    )

    connection.commit()
    connection.close()

    print("Sample data inserted successfully.")


if __name__ == "__main__":
    seed_data()