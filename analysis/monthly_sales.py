from app.database import get_connection


def monthly_sales():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            strftime('%Y-%m', orders.order_date) AS month,
            SUM(order_items.quantity * order_items.unit_price) AS revenue
        FROM orders
        JOIN order_items
            ON orders.id = order_items.order_id
        GROUP BY month
        ORDER BY month
    """)

    results = cursor.fetchall()

    print("\nMONTHLY SALES PERFORMANCE")
    print("----------------------------------------")

    previous_revenue = None

    for month, revenue in results:

        if previous_revenue is None:
            growth = None
        else:
            growth = (
                (revenue - previous_revenue)
                / previous_revenue
            ) * 100

        if growth is None:
            print(f"{month}: ${revenue:,.2f}")
        else:
            print(
                f"{month}: ${revenue:,.2f} "
                f"| Growth: {growth:+.2f}%"
            )

        previous_revenue = revenue

    connection.close()


if __name__ == "__main__":
    monthly_sales()