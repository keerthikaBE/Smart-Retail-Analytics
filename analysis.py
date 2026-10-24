from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data" / "sales_data.csv", parse_dates=["order_date"])
print("Rows and columns:", df.shape)
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())

df = df.drop_duplicates().dropna(subset=["order_date", "product", "quantity", "unit_price"])
df["sales"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
df["month"] = df["order_date"].dt.to_period("M").astype(str)

print("\nTotal revenue: ₹{:,.2f}".format(df["sales"].sum()))
print("\nTop products by revenue:\n", df.groupby("product")["sales"].sum().sort_values(ascending=False).head(5))
print("\nMonthly revenue:\n", df.groupby("month")["sales"].sum().round(2))
