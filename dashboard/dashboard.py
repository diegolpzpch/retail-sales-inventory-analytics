import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "retail.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales & Inventory Analytics")
st.write("Interactive dashboard for sales performance and inventory analysis")


connection = get_connection()


# --------------------------------------------------
# LOAD SALES DATA
# --------------------------------------------------

sales_query = """
SELECT
    orders.id AS order_id,
    orders.order_date,
    stores.id AS store_id,
    stores.name AS store,
    products.id AS product_id,
    products.name AS product,
    products.category,
    order_items.quantity,
    order_items.unit_price,
    order_items.quantity * order_items.unit_price AS revenue
FROM orders
JOIN stores
    ON orders.store_id = stores.id
JOIN order_items
    ON orders.id = order_items.order_id
JOIN products
    ON order_items.product_id = products.id
"""

sales = pd.read_sql_query(sales_query, connection)

sales["month"] = sales["order_date"].str[:7]


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

store_options = ["All"] + sorted(sales["store"].unique().tolist())

selected_store = st.sidebar.selectbox(
    "Store",
    store_options
)

category_options = ["All"] + sorted(
    sales["category"].unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Category",
    category_options
)

month_options = ["All"] + sorted(
    sales["month"].unique().tolist()
)

selected_month = st.sidebar.selectbox(
    "Month",
    month_options
)


# Apply filters
filtered_sales = sales.copy()

if selected_store != "All":
    filtered_sales = filtered_sales[
        filtered_sales["store"] == selected_store
    ]

if selected_category != "All":
    filtered_sales = filtered_sales[
        filtered_sales["category"] == selected_category
    ]

if selected_month != "All":
    filtered_sales = filtered_sales[
        filtered_sales["month"] == selected_month
    ]


# --------------------------------------------------
# KPIs
# --------------------------------------------------

total_revenue = filtered_sales["revenue"].sum()

total_orders = filtered_sales["order_id"].nunique()

units_sold = filtered_sales["quantity"].sum()

if total_orders > 0:
    average_ticket = total_revenue / total_orders
else:
    average_ticket = 0


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Units Sold",
    f"{units_sold:,}"
)

col4.metric(
    "Average Ticket",
    f"${average_ticket:,.2f}"
)


st.divider()


# --------------------------------------------------
# MONTHLY REVENUE
# --------------------------------------------------

st.subheader("📈 Monthly Revenue")

monthly_sales = (
    filtered_sales
    .groupby("month")["revenue"]
    .sum()
    .reset_index()
)

st.line_chart(
    monthly_sales.set_index("month")["revenue"]
)


# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

st.subheader("🏆 Top 5 Products by Revenue")

top_products = (
    filtered_sales
    .groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(top_products)


# --------------------------------------------------
# REVENUE BY STORE
# --------------------------------------------------

st.subheader("🏪 Revenue by Store")

store_sales = (
    filtered_sales
    .groupby("store")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(store_sales)


st.divider()


# --------------------------------------------------
# INVENTORY ANALYSIS
# --------------------------------------------------

st.header("📦 Inventory Analysis")

inventory_query = """
SELECT
    inventory.store_id,
    stores.name AS store,
    inventory.product_id,
    products.name AS product,
    products.category,
    inventory.stock_quantity
FROM inventory
JOIN stores
    ON inventory.store_id = stores.id
JOIN products
    ON inventory.product_id = products.id
"""

inventory = pd.read_sql_query(
    inventory_query,
    connection
)


# Apply store/category filters to inventory

if selected_store != "All":
    inventory = inventory[
        inventory["store"] == selected_store
    ]

if selected_category != "All":
    inventory = inventory[
        inventory["category"] == selected_category
    ]


# Calculate sales per product/store

units_by_product = (
    filtered_sales
    .groupby(
        ["store_id", "product_id"]
    )["quantity"]
    .sum()
    .reset_index()
)

units_by_product.rename(
    columns={"quantity": "units_sold"},
    inplace=True
)


inventory_analysis = inventory.merge(
    units_by_product,
    on=["store_id", "product_id"],
    how="left"
)

inventory_analysis["units_sold"] = (
    inventory_analysis["units_sold"]
    .fillna(0)
)


# Number of months included in current analysis

months_analyzed = max(
    filtered_sales["month"].nunique(),
    1
)

inventory_analysis["avg_monthly_sales"] = (
    inventory_analysis["units_sold"]
    / months_analyzed
)


def calculate_months_of_stock(row):

    if row["avg_monthly_sales"] == 0:
        return 999

    return (
        row["stock_quantity"]
        / row["avg_monthly_sales"]
    )


inventory_analysis["months_of_stock"] = (
    inventory_analysis.apply(
        calculate_months_of_stock,
        axis=1
    )
)


def inventory_status(months):

    if months < 1:
        return "LOW STOCK"

    elif months > 3:
        return "OVERSTOCK"

    else:
        return "HEALTHY"


inventory_analysis["status"] = (
    inventory_analysis[
        "months_of_stock"
    ].apply(inventory_status)
)


# --------------------------------------------------
# INVENTORY KPIs
# --------------------------------------------------

low_stock = (
    inventory_analysis["status"]
    == "LOW STOCK"
).sum()

healthy = (
    inventory_analysis["status"]
    == "HEALTHY"
).sum()

overstock = (
    inventory_analysis["status"]
    == "OVERSTOCK"
).sum()


col1, col2, col3 = st.columns(3)

col1.metric(
    "🔴 Low Stock",
    low_stock
)

col2.metric(
    "🟢 Healthy",
    healthy
)

col3.metric(
    "🟡 Overstock",
    overstock
)


# --------------------------------------------------
# INVENTORY TABLE
# --------------------------------------------------

st.subheader("Inventory Detail")

inventory_table = inventory_analysis[
    [
        "store",
        "product",
        "category",
        "stock_quantity",
        "units_sold",
        "months_of_stock",
        "status"
    ]
].copy()

inventory_table["months_of_stock"] = (
    inventory_table["months_of_stock"]
    .round(2)
)

inventory_table.rename(
    columns={
        "store": "Store",
        "product": "Product",
        "category": "Category",
        "stock_quantity": "Stock",
        "units_sold": "Units Sold",
        "months_of_stock": "Months of Stock",
        "status": "Status"
    },
    inplace=True
)

st.dataframe(
    inventory_table,
    use_container_width=True,
    hide_index=True
)


connection.close()