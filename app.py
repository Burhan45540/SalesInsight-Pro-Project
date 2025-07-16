#import a library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


#setup a page
st.set_page_config(page_title="SalesInsight Pro", layout="wide")
st.title("📊 SalesInsight Pro - Interactive Sales Dashboard")

#Read csv files
df=pd.read_csv("Sales_April_2019.csv")
df.dropna(how="all",inplace=True)

#clean the data
df=df[df["Quantity Ordered"].str.isnumeric()]
df["Quantity Ordered"]=df["Quantity Ordered"].astype(int)
df["Price Each"]=df["Price Each"].astype(float)
df['Sales']=df["Quantity Ordered"] * df["Price Each"]
df["City"]=df["Purchase Address"].apply(lambda x : x.split(',')[1])

st.write("Product And Its Info : ")
st.write(df)

#filtering
st.sidebar.header("🔍 Filter Sales Data")
selected_city=st.sidebar.multiselect("Select City",df["City"].unique())
selected_product=st.sidebar.multiselect("Select Product",df["Product"].unique())


if selected_city and selected_product:
  filtered_df=df[
    (df["City"].isin(selected_city)) & (df["Product"].isin(selected_product))
  ]
  st.subheader(f"After Selecting Product : {selected_product} in City : {selected_city}")
  st.write(filtered_df)

  st.subheader("Total Sales By a Product")
  sales=filtered_df.groupby("Product")["Sales"].sum()
  st.bar_chart(sales)

#KPI
  total_sales = filtered_df["Sales"].sum()
  total_orders = filtered_df["Quantity Ordered"].sum()
  unique_cities = filtered_df["City"].nunique()

  col1, col2, col3 = st.columns(3)
  col1.metric("💰 Total Sales of Selected City", f"${total_sales:.2f}")
  col2.metric("📦 Total Orders", total_orders)
  col3.metric("🏙️ Cities", unique_cities)


else:
  st.warning("Please select at least one city and one product")

