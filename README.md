# Sales Data Analysis (Pandas + SQL)

A data analysis project on e-commerce sales data - cleans messy data,
answers business questions using both Pandas and raw SQL, and produces
visual reports. Built to demonstrate Python, Pandas, and SQL skills for
data analyst roles.

## Tech Stack
- **Data handling:** Pandas
- **Database/SQL:** SQLite3
- **Visualization:** Matplotlib

## Dataset
1500 synthetic but realistic e-commerce orders across 5 categories
(Electronics, Fashion, Home, Beauty, Sports), with intentionally messy
data (some missing region values) to practice real-world data cleaning.

## Project Structure
```
sales-data-analysis/
├── data/
│   ├── generate_data.py     # builds the dataset
│   └── sales_data.csv       # generated dataset (1500 orders)
├── charts/                   # output charts (generated on run)
├── analyze_pandas.py         # Pandas-based cleaning + analysis + charts
├── analyze_sql.py            # SQL-based analysis (SQLite)
├── sales.db                  # SQLite database (generated on run)
└── README.md
```

## What it answers
- Total revenue, total orders, average order value
- Revenue breakdown by category and region
- Top-selling products by quantity and by revenue
- Most-used payment modes
- Monthly revenue trend (with running total, via SQL window function)
- Which region gives the highest average discount
- High-value orders (top 10%, using a SQL percentile-style query)

## Setup & Usage

```bash
# 1. Install dependencies
pip install pandas matplotlib

# 2. Generate the dataset
python3 data/generate_data.py

# 3. Run the Pandas analysis (prints summary, saves charts to charts/)
python3 analyze_pandas.py

# 4. Run the SQL analysis (loads into SQLite, runs SQL queries)
python3 analyze_sql.py
```

## Sample Insight (from this dataset)
Electronics is the highest-revenue category (~34% of total revenue),
driven mainly by Headphones and Smartwatch. Revenue peaked in August,
and the Central region gives the highest average discount despite not
being the top revenue region - worth flagging as a discount-policy
question in a real business setting.

## Skills Demonstrated
- Data cleaning (handling missing values)
- Pandas groupby, aggregation, datetime handling
- SQL: GROUP BY, subqueries, window functions (`SUM() OVER`)
- Data visualization (bar, line, pie charts)
- Translating raw data into business insights

## Possible Extensions
- Build an interactive dashboard (Streamlit or Power BI, since that's
  already on the "currently learning" list)
- Add cohort/retention analysis if customer_id were included
- Connect to a real dataset (Kaggle "Superstore Sales" or similar)

## Author
Kishan Kumar
