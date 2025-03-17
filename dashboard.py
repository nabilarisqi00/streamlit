import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
@st.cache_data
def load_data():
    order_items = pd.read_csv("order_items_dataset.csv")
    orders = pd.read_csv("orders_dataset.csv")
    products = pd.read_csv("products_dataset.csv")
    category_translation = pd.read_csv("product_category_name_translation.csv")
    
    # Convert datetime
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    orders["order_year"] = orders["order_purchase_timestamp"].dt.year
    orders["order_month"] = orders["order_purchase_timestamp"].dt.month
    
    # Merge datasets
    df = order_items.merge(orders, on="order_id", how="inner")
    df = df.merge(products, on="product_id", how="inner")
    df = df.merge(category_translation, on="product_category_name", how="left")
    
    # Handle missing category names
    df["product_category_name_english"].fillna("Unknown", inplace=True)
    
    return df

df = load_data()

# Streamlit UI
st.title("E-commerce Sales Dashboard")

# Sidebar for year selection
year = st.slider("Select Year", 2017, 2018, 2017)
st.subheader(f"Data Visualization for {year}")

# Filter dataset by selected year
df_filtered = df[df["order_year"] == year]

# Interactive selection of top N categories
num_categories = st.slider("Select number of top categories", 5, 20, 10)

# Visualisasi 1: Kategori produk yang paling sering dipesan
st.subheader(f"Top {num_categories} Most Ordered Product Categories")
category_counts = df_filtered["product_category_name_english"].value_counts().head(num_categories)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=category_counts.values, y=category_counts.index, palette="viridis", ax=ax)
ax.set_xlabel("Order Count")
ax.set_ylabel("Product Category")
ax.set_title(f"Top {num_categories} Product Categories")
st.pyplot(fig)

# Visualisasi 2: Tren jumlah pesanan per bulan
top_years = [2017, 2018]
selected_year = st.selectbox("Select year for monthly order trends", top_years)

df_selected_year = df[df["order_year"] == selected_year]
monthly_orders = df_selected_year.groupby("order_month").size()

# Interactive chart type selection
chart_type = st.selectbox("Select chart type", ["Line Chart", "Bar Chart"], key="chart_type")

fig, ax = plt.subplots(figsize=(10, 5))
if chart_type == "Line Chart":
    sns.lineplot(x=monthly_orders.index, y=monthly_orders.values, marker="o", color="b", ax=ax)
else:
    sns.barplot(x=monthly_orders.index, y=monthly_orders.values, palette="Blues", ax=ax)

ax.set_xlabel("Month")
ax.set_ylabel("Order Count")
ax.set_title(f"Order Trends by Month ({selected_year})")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
st.pyplot(fig)

# Additional Data Exploration
st.write("\n")
st.write("### Explore the Data")
if st.checkbox("Show Raw Data"):
    st.write(df_filtered)
