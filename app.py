import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

# Load data
df = pd.read_csv("SampleSuperstore.csv",encoding='ISO-8859-1')

st.title("📊 Sales Performance Dashboard")

# Sidebar filters
region = st.sidebar.multiselect("Select Region:", options=df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category:", options=df["Category"].unique(), default=df["Category"].unique())

df_filtered = df.query("Region == @region and Category == @category")

# KPIs
total_sales = int(df_filtered["Sales"].sum())
total_profit = int(df_filtered["Profit"].sum())
avg_discount = round(df_filtered["Discount"].mean(), 2)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,}")
col2.metric("Total Profit", f"${total_profit:,}")
col3.metric("Avg. Discount", f"{avg_discount*100}%")

# Charts
st.subheader("Sales by Region")
fig1 = px.bar(df_filtered.groupby("Region", as_index=False).sum(), x="Region", y="Sales", color="Region")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Sales by Category")
fig2 = px.pie(df_filtered, names="Category", values="Sales", title="Sales Distribution by Category")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Monthly Sales Trend")
df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"])
monthly_sales = df_filtered.groupby(df_filtered["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)
fig3 = px.line(monthly_sales, x="Order Date", y="Sales", title="Monthly Sales Trend")
st.plotly_chart(fig3, use_container_width=True)

df["Order Date"] = pd.to_datetime(df["Order Date"])
year = st.sidebar.multiselect(
    "Select Year:",
    options=df["Order Date"].dt.year.unique(),
    default=df["Order Date"].dt.year.unique()
)
df = df[df["Order Date"].dt.year.isin(year)]
st.subheader("Profit vs Sales by Category")
fig4 = px.scatter(
    df, x="Sales", y="Profit", color="Category", size="Quantity",
    title="Profit vs Sales by Category"
)
st.plotly_chart(fig4, use_container_width=True)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name='filtered_sales.csv',
    mime='text/csv'
)
st.markdown("---")
st.markdown("Developed by Sagar Pamalli |  Data Analysis using Python & Streamlit")
