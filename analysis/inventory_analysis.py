from app.database import get_connection


def inventory_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            stores.name,
            products.name,
            inventory.stock_quantity,
            COALESCE(SUM(order_items.quantity), 0) AS units_sold
        FROM inventory
        JOIN stores
            ON inventory.store_id = stores.id
        JOIN products
            ON inventory.product_id = products.id
        LEFT JOIN orders
            ON orders.store_id = stores.id
        LEFT JOIN order_items
            ON order_items.order_id = orders.id
            AND order_items.product_id = products.id
        GROUP BY
            stores.name,
            products.name,
            inventory.stock_quantity
        ORDER BY units_sold DESC
    """)

    results = cursor.fetchall()

    print("\nINVENTORY ANALYSIS")
    print("------------------------------------------------------------")

    for store, product, stock, units_sold in results:

        average_monthly_sales = units_sold / 12

        if average_monthly_sales > 0:
            months_of_stock = stock / average_monthly_sales
        else:
            months_of_stock = 999

        if months_of_stock < 1:
            status = "LOW STOCK"
        elif months_of_stock > 3:
            status = "OVERSTOCK"
        else:
            status = "HEALTHY"

        print(
            f"{store} | {product} | "
            f"Stock: {stock} | "
            f"Units sold: {units_sold} | "
            f"Status: {status}"
        )

    connection.close()


if __name__ == "__main__":
    inventory_analysis()