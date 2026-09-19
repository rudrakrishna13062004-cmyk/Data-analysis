"""
Sales Data Analysis - SQL
Loads the CSV into an SQLite database and runs SQL queries to answer
business questions. Shows SQL skills (GROUP BY, JOIN-ready schema,
window functions) alongside the Pandas analysis.

Run: python3 analyze_sql.py
"""
import sqlite3

import pandas as pd

DATA_PATH = "data/sales_data.csv"
DB_PATH = "sales.db"


def load_to_sqlite():
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["region"] = df["region"].fillna("Unknown")

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    return conn


def run_query(conn, title, query):
    print(f"\n--- {title} ---")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result


if __name__ == "__main__":
    conn = load_to_sqlite()
    print(f"Loaded data into {DB_PATH} (table: sales)")

    run_query(conn, "Total revenue and orders", """
        SELECT
            COUNT(*) AS total_orders,
            ROUND(SUM(total_amount), 2) AS total_revenue,
            ROUND(AVG(total_amount), 2) AS avg_order_value
        FROM sales;
    """)

    run_query(conn, "Top 5 products by revenue", """
        SELECT product, category,
               ROUND(SUM(total_amount), 2) AS revenue,
               SUM(quantity) AS units_sold
        FROM sales
        GROUP BY product, category
        ORDER BY revenue DESC
        LIMIT 5;
    """)

    run_query(conn, "Monthly revenue with running total", """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            ROUND(SUM(total_amount), 2) AS monthly_revenue,
            ROUND(SUM(SUM(total_amount)) OVER (ORDER BY strftime('%Y-%m', order_date)), 2) AS running_total
        FROM sales
        GROUP BY month
        ORDER BY month;
    """)

    run_query(conn, "Region-wise average discount given", """
        SELECT region,
               ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
               COUNT(*) AS orders
        FROM sales
        GROUP BY region
        ORDER BY avg_discount_pct DESC;
    """)

    run_query(conn, "High value orders (above 90th percentile)", """
        SELECT order_id, product, category, total_amount, order_date
        FROM sales
        WHERE total_amount > (
            SELECT total_amount FROM sales
            ORDER BY total_amount DESC
            LIMIT 1 OFFSET (SELECT CAST(COUNT(*) * 0.1 AS INT) FROM sales)
        )
        ORDER BY total_amount DESC
        LIMIT 10;
    """)

    conn.close()
    print(f"\nDone. Database saved at {DB_PATH} - open it with any SQLite viewer to explore further.")
