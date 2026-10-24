from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
DB_PATH = BASE_DIR / "data" / "retail_sales.db"

st.set_page_config(page_title="Smart Retail Analytics", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    data = data.drop_duplicates()
    data = data.dropna(subset=["order_date", "product", "quantity", "unit_price"])
    data["sales"] = data["quantity"] * data["unit_price"] * (1 - data["discount"])
    data["sales"] = data["sales"].round(2)
    data["month"] = data["order_date"].dt.to_period("M").astype(str)
    return data

def save_to_sqlite(data):
    with sqlite3.connect(DB_PATH) as conn:
        data.to_sql("sales", conn, if_exists="replace", index=False)

data = load_data()
save_to_sqlite(data)

st.title("📊 Smart Retail Analytics & Sales Forecasting")
st.caption("Beginner-friendly demonstration project | Dataset is synthetic sample data, not real business data.")
with st.sidebar:
    st.header("Filters")
    min_date = data["order_date"].min().date()
    max_date = data["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions = ["All"] + sorted(data["region"].dropna().unique().tolist())
    region = st.selectbox("Region", regions)
    categories = ["All"] + sorted(data["category"].dropna().unique().tolist())
    category = st.selectbox("Category", categories)

filtered = data.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[(filtered["order_date"].dt.date >= date_range[0]) & (filtered["order_date"].dt.date <= date_range[1])]
if region != "All":
    filtered = filtered[filtered["region"] == region]
if category != "All":
    filtered = filtered[filtered["category"] == category]

if filtered.empty:
    st.warning("No records match these filters. Please choose a wider date range or another filter.")
    st.stop()

total_sales = filtered["sales"].sum()
orders = filtered["order_id"].nunique()
avg_order_value = total_sales / orders if orders else 0
estimated_profit = (filtered["sales"] - filtered["estimated_cost"]).sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{total_sales:,.0f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Average Order Value", f"₹{avg_order_value:,.0f}")
c4.metric("Illustrative Estimated Profit", f"₹{estimated_profit:,.0f}", help="Uses assumed synthetic cost values; not a real accounting figure.")

left, right = st.columns(2)
with left:
    monthly = filtered.groupby("month", as_index=False)["sales"].sum().sort_values("month")
    fig = px.line(monthly, x="month", y="sales", markers=True, title="Monthly Sales Trend")
    fig.update_layout(xaxis_title="Month", yaxis_title="Sales (₹)")
    st.plotly_chart(fig, use_container_width=True)
with right:
    product_sales = filtered.groupby("product", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    fig = px.bar(product_sales.head(10), x="product", y="sales", title="Top Products by Sales", text_auto=".2s")
    fig.update_layout(xaxis_title="Product", yaxis_title="Sales (₹)")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    cat_sales = filtered.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    fig = px.bar(cat_sales, x="category", y="sales", title="Sales by Category", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)
with right:
    region_sales = filtered.groupby("region", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    fig = px.pie(region_sales, names="region", values="sales", title="Revenue Share by Region")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Sales Forecast (simple baseline comparison)")
st.write("This demonstration aggregates sales by month and compares a simple linear trend with a naive previous-month baseline. Forecasts are estimates, not guarantees.")
monthly_all = data.groupby("month", as_index=False)["sales"].sum().sort_values("month").reset_index(drop=True)
monthly_all["month_number"] = range(len(monthly_all))
if len(monthly_all) >= 6:
    split = max(3, int(len(monthly_all) * 0.8))
    train = monthly_all.iloc[:split]
    test = monthly_all.iloc[split:]
    model = LinearRegression()
    model.fit(train[["month_number"]], train["sales"])
    model_pred = model.predict(test[["month_number"]])
    naive_pred = monthly_all["sales"].shift(1).iloc[split:].values
    model_mae = mean_absolute_error(test["sales"], model_pred)
    naive_mae = mean_absolute_error(test["sales"], naive_pred)
    st.write(f"Hold-out MAE — Linear trend: ₹{model_mae:,.0f} | Previous-month baseline: ₹{naive_mae:,.0f}")
    model.fit(monthly_all[["month_number"]], monthly_all["sales"])
    next_number = [[len(monthly_all)]]
    next_month = (pd.Period(monthly_all["month"].iloc[-1], freq="M") + 1).strftime("%Y-%m")
    forecast = max(0, float(model.predict(pd.DataFrame(next_number, columns=["month_number"]))[0]))
    st.metric(f"Illustrative forecast for {next_month}", f"₹{forecast:,.0f}")
else:
    st.info("At least six months of sales history is needed for this demo forecast.")

st.subheader("Filtered Sales Records")
st.dataframe(filtered.drop(columns=["month"], errors="ignore"), use_container_width=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_sales.csv", "text/csv")

st.subheader("Business recommendations (review these against your results)")
st.markdown("""
- Review the highest-revenue products before planning replenishment.
- Compare monthly sales trends before seasonal promotions.
- Compare category and region performance before allocating marketing effort.
- Check whether discounts are associated with higher quantities and revenue.
- Treat the forecast as an estimate; validate it with more real historical data before making business decisions.
""")
st.caption("Synthetic dataset generated for learning. Profit is illustrative because cost values are assumptions.")
