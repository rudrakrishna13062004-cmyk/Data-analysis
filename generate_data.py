"""
Generates a synthetic but realistic e-commerce sales dataset for
practicing data analysis (Pandas + SQL).

Run: python3 data/generate_data.py
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

categories = {
    "Electronics": ["Headphones", "Smartwatch", "Bluetooth Speaker", "Power Bank", "Webcam"],
    "Fashion": ["T-Shirt", "Sneakers", "Backpack", "Sunglasses", "Wallet"],
    "Home": ["Table Lamp", "Coffee Mug", "Cushion Cover", "Wall Clock", "Storage Box"],
    "Beauty": ["Face Wash", "Lip Balm", "Hair Oil", "Sunscreen", "Perfume"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Water Bottle", "Resistance Band", "Cap"],
}

regions = ["North", "South", "East", "West", "Central"]
payment_modes = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking"]

price_ranges = {
    "Electronics": (500, 4000),
    "Fashion": (300, 2500),
    "Home": (200, 1800),
    "Beauty": (150, 900),
    "Sports": (250, 3000),
}

start_date = datetime(2025, 1, 1)
rows = []
order_id = 1000

for _ in range(1500):
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    low, high = price_ranges[category]
    price = round(random.uniform(low, high), 2)
    quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 12, 8, 5])[0]

    # simulate occasional missing / messy data (realistic for a data cleaning exercise)
    region = random.choice(regions) if random.random() > 0.02 else ""
    payment_mode = random.choice(payment_modes)

    days_offset = random.randint(0, 270)
    order_date = start_date + timedelta(days=days_offset)

    # occasional discount
    discount_pct = random.choices([0, 5, 10, 15, 20], weights=[40, 20, 20, 12, 8])[0]
    total_amount = round(price * quantity * (1 - discount_pct / 100), 2)

    rows.append([
        order_id, order_date.strftime("%Y-%m-%d"), category, product,
        price, quantity, discount_pct, total_amount, region, payment_mode
    ])
    order_id += 1

with open("/home/claude/sales-data-analysis/data/sales_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "order_id", "order_date", "category", "product", "price",
        "quantity", "discount_pct", "total_amount", "region", "payment_mode"
    ])
    writer.writerows(rows)

print(f"Generated {len(rows)} orders -> data/sales_data.csv")
