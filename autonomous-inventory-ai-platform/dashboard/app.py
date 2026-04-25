import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Inventory AI Platform",
    layout="wide"
)

st.title("Autonomous Inventory Optimization Platform")
st.write("AI-powered inventory monitoring, forecasting, decisions, and agent actions")


def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "error" in data:
            st.error(data["error"])
            return pd.DataFrame()

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"API connection error: {e}")
        return pd.DataFrame()


inventory_df = fetch_data("/inventory")
risk_df = fetch_data("/risk-alerts")
forecast_df = fetch_data("/forecast")
decisions_df = fetch_data("/decisions")
actions_df = fetch_data("/agent-actions")


st.sidebar.header("Filters")

selected_store = "All"
selected_product = "All"

if not inventory_df.empty:
    store_options = ["All"] + sorted(inventory_df["store_id"].astype(str).unique().tolist())
    selected_store = st.sidebar.selectbox("Select Store", store_options)

    product_options = ["All"] + sorted(inventory_df["product"].unique().tolist())
    selected_product = st.sidebar.selectbox("Select Product", product_options)


def apply_filters(df):
    if df.empty:
        return df

    filtered = df.copy()

    if selected_store != "All" and "store_id" in filtered.columns:
        filtered = filtered[filtered["store_id"].astype(str) == selected_store]

    if selected_product != "All" and "product" in filtered.columns:
        filtered = filtered[filtered["product"] == selected_product]

    return filtered


inventory_filtered = apply_filters(inventory_df)
risk_filtered = apply_filters(risk_df)
forecast_filtered = apply_filters(forecast_df)
decisions_filtered = apply_filters(decisions_df)
actions_filtered = apply_filters(actions_df)


st.subheader("Executive Summary")

total_items = len(inventory_filtered)
risk_items = len(risk_filtered[risk_filtered["risk_type"] != "Normal"]) if not risk_filtered.empty else 0
stockout_risks = len(risk_filtered[risk_filtered["risk_type"] == "Stockout Risk"]) if not risk_filtered.empty else 0
high_priority = len(decisions_filtered[decisions_filtered["priority"] == "High"]) if not decisions_filtered.empty else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Inventory Items", total_items)
col2.metric("Risk Items", risk_items)
col3.metric("Stockout Risks", stockout_risks)
col4.metric("High Priority Actions", high_priority)


st.subheader("Risk Breakdown")

if not risk_filtered.empty and "risk_type" in risk_filtered.columns:
    risk_counts = risk_filtered["risk_type"].value_counts()
    st.bar_chart(risk_counts)
else:
    st.info("No risk data available.")


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Inventory",
    "Risk Alerts",
    "Forecast",
    "Decisions",
    "Agent Actions"
])

with tab1:
    st.subheader("Inventory Data")
    st.dataframe(inventory_filtered, use_container_width=True)

with tab2:
    st.subheader("Risk Alerts")
    st.dataframe(risk_filtered, use_container_width=True)

with tab3:
    st.subheader("Demand Forecast")
    st.dataframe(forecast_filtered, use_container_width=True)

with tab4:
    st.subheader("Decision Engine Output")
    st.dataframe(decisions_filtered, use_container_width=True)

with tab5:
    st.subheader("Agent Actions")
    st.dataframe(actions_filtered, use_container_width=True)