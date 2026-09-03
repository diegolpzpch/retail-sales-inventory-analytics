from app.database import get_connection


def business_rankings():
    connection = get_connection()
    cursor = connection.cursor()

    # Top stores by revenue
    cursor.execute("""
        SELECT
            stores.name,
            SUM(order_items.quantity * order_items.unit_price) AS revenue
        FROM orders
        JOIN stores
            ON orders.store_id = stores.id
        JOIN order_items
            ON orders.id = order_items.order_id
        GROUP BY stores.name
        ORDER BY revenue DESC
    """)

    top_stores = cursor.fetchall()

    print("\nTOP STORES BY REVENUE")
    print("-----------------------------")

    for store, revenue in top_stores:
        print(f"{store}: ${revenue:,.2f}")


    # Top products by revenue
    cursor.execute("""
        SELECT
            products.name,
            SUM(order_items.quantity * order_items.unit_price) AS revenue
        FROM order_items
        JOIN products
            ON order_items.product_id = products.id
        GROUP BY products.name
        ORDER BY revenue DESC
    """)

    top_products = cursor.fetchall()

    print("\nTOP PRODUCTS BY REVENUE")
    print("-----------------------------")

    for product, revenue in top_products:
        print(f"{product}: ${revenue:,.2f}")


    # Categories by revenue
    cursor.execute("""
        SELECT
            products.category,
            SUM(order_items.quantity * order_items.unit_price) AS revenue
        FROM order_items
        JOIN products
            ON order_items.product_id = products.id
        GROUP BY products.category
        ORDER BY revenue DESC
    """)

    categories = cursor.fetchall()

    print("\nREVENUE BY CATEGORY")
    print("-----------------------------")

    for category, revenue in categories:
        print(f"{category}: ${revenue:,.2f}")

    connection.close()


if __name__ == "__main__":
    business_rankings()