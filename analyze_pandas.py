"""
Sales Data Analysis - Pandas
Cleans the raw sales data, analyzes it, and saves charts + a summary report.

Run: python3 analyze_pandas.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = "data/sales_data.csv"
CHARTS_DIR = "charts"

os.makedirs(CHARTS_DIR, exist_ok=True)


def load_and_clean(path):
    df = pd.read_csv(path, parse_dates=["order_date"])
    print(f"Loaded {len(df)} rows, {df.isnull().sum().sum()} missing values before cleaning")

    # handle missing region values (real-world data cleaning step)
    missing_region = df["region"].isnull().sum()
    df["region"] = df["region"].fillna("Unknown")
    print(f"Filled {missing_region} missing region values with 'Unknown'")

    # basic sanity checks
    df = df[df["total_amount"] > 0]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    return df


def analyze(df):
    print("\n" + "=" * 50)
    print("SALES SUMMARY")
    print("=" * 50)

    total_revenue = df["total_amount"].sum()
    total_orders = len(df)
    avg_order_value = df["total_amount"].mean()
    print(f"Total Revenue: Rs {total_revenue:,.2f}")
    print(f"Total Orders: {total_orders}")
    print(f"Average Order Value: Rs {avg_order_value:,.2f}")

    print("\n--- Revenue by Category ---")
    category_revenue = df.groupby("category")["total_amount"].sum().sort_values(ascending=False)
    print(category_revenue.to_string())

    print("\n--- Top 5 Best-Selling Products (by quantity) ---")
    top_products = df.groupby("product")["quantity"].sum().sort_values(ascending=False).head(5)
    print(top_products.to_string())

    print("\n--- Revenue by Region ---")
    region_revenue = df.groupby("region")["total_amount"].sum().sort_values(ascending=False)
    print(region_revenue.to_string())

    print("\n--- Most Used Payment Mode ---")
    payment_counts = df["payment_mode"].value_counts()
    print(payment_counts.to_string())

    print("\n--- Monthly Revenue Trend ---")
    monthly_revenue = df.groupby("month")["total_amount"].sum()
    print(monthly_revenue.to_string())

    return {
        "category_revenue": category_revenue,
        "top_products": top_products,
        "region_revenue": region_revenue,
        "payment_counts": payment_counts,
        "monthly_revenue": monthly_revenue,
    }


def make_charts(results):
    plt.style.use("seaborn-v0_8-whitegrid")

    # 1. Revenue by category (bar chart)
    plt.figure(figsize=(8, 5))
    results["category_revenue"].plot(kind="bar", color="#4C72B0")
    plt.title("Revenue by Category")
    plt.ylabel("Revenue (Rs)")
    plt.xlabel("Category")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/revenue_by_category.png", dpi=120)
    plt.close()

    # 2. Monthly revenue trend (line chart)
    plt.figure(figsize=(9, 5))
    results["monthly_revenue"].plot(kind="line", marker="o", color="#DD8452")
    plt.title("Monthly Revenue Trend")
    plt.ylabel("Revenue (Rs)")
    plt.xlabel("Month")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/monthly_revenue_trend.png", dpi=120)
    plt.close()

    # 3. Payment mode distribution (pie chart)
    plt.figure(figsize=(6, 6))
    results["payment_counts"].plot(kind="pie", autopct="%1.1f%%")
    plt.title("Payment Mode Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/payment_mode_distribution.png", dpi=120)
    plt.close()

    # 4. Revenue by region (bar chart)
    plt.figure(figsize=(7, 5))
    results["region_revenue"].plot(kind="bar", color="#55A868")
    plt.title("Revenue by Region")
    plt.ylabel("Revenue (Rs)")
    plt.xlabel("Region")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/revenue_by_region.png", dpi=120)
    plt.close()

    print(f"\nSaved 4 charts to {CHARTS_DIR}/")


if __name__ == "__main__":
    df = load_and_clean(DATA_PATH)
    results = analyze(df)
    make_charts(results)
