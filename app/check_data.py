from app.database import get_connection


def check_data():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM stores")
    stores_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers_count = cursor.fetchone()[0]

    print("DATABASE SUMMARY")
    print("----------------")
    print(f"Products: {products_count}")
    print(f"Stores: {stores_count}")
    print(f"Customers: {customers_count}")

    connection.close()


if __name__ == "__main__":
    check_data()