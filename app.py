from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data (Streamlit Cloud safe path)
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv("data/train.csv")

st.title("📊 E-commerce Sales Dashboard")

# KPIs
total_revenue = df["Sales"].sum()
total_orders = df["Order ID"].nunique()

col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)

# Fix de datas (IMPORTANTE)
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)

# Monthly revenue
monthly = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
monthly["Order Date"] = monthly["Order Date"].astype(str)

st.plotly_chart(
    px.line(monthly, x="Order Date", y="Sales", title="Monthly Revenue")
)

# Top products
top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

st.plotly_chart(
    px.bar(top_products.head(10), x="Product Name", y="Sales", title="Top Products")
)

# Revenue by country
country = df.groupby("Country")["Sales"].sum().reset_index()

st.plotly_chart(
    px.bar(country, x="Country", y="Sales", title="Revenue by Country")
)