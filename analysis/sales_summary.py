from app.database import get_connection


def sales_summary():
    connection = get_connection()
    cursor = connection.cursor()

    # Total number of orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    # Total number of order lines
    cursor.execute("SELECT COUNT(*) FROM order_items")
    total_order_items = cursor.fetchone()[0]

    # Total units sold
    cursor.execute("""
        SELECT SUM(quantity)
        FROM order_items
    """)
    total_units = cursor.fetchone()[0]

    # Total revenue
    cursor.execute("""
        SELECT SUM(quantity * unit_price)
        FROM order_items
    """)
    total_revenue = cursor.fetchone()[0]

    # Average ticket
    average_ticket = total_revenue / total_orders

    print("SALES SUMMARY")
    print("-----------------------------")
    print(f"Orders: {total_orders}")
    print(f"Order lines: {total_order_items}")
    print(f"Units sold: {total_units}")
    print(f"Revenue: ${total_revenue:,.2f}")
    print(f"Average ticket: ${average_ticket:,.2f}")

    connection.close()


if __name__ == "__main__":
    sales_summary()