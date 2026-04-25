import streamlit as st
import pandas as pd

st.set_page_config(page_title="POS Payment AI System", layout="wide")

st.title("AI-Powered POS & Payment Automation Platform")

# Load data
transactions = pd.read_csv("pos_payments/data/transactions.csv")
risk = pd.read_csv("pos_payments/data/payment_risk_alerts.csv")
decisions = pd.read_csv("pos_payments/data/payment_decisions.csv")
actions = pd.read_csv("pos_payments/data/payment_agent_actions.csv")
audit = pd.read_csv("pos_payments/data/audit_log.csv")

# KPIs
st.subheader("System KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", len(transactions))
col2.metric("Failed Payments", len(risk[risk["risk_type"] == "Failed Payment"]))
col3.metric("High Risk Cases", len(risk[risk["severity"] == "High"]))
col4.metric("Manual Approvals", len(decisions[decisions["approval_status"] == "Pending"]))

# Monitoring Metrics
st.subheader("Monitoring Metrics")

automation_rate = len(actions[actions["action_status"] == "Completed"]) / len(actions)
st.write(f"Automation Rate: {round(automation_rate * 100, 2)}%")

# Risk chart
st.subheader("Risk Breakdown")
st.bar_chart(risk["risk_type"].value_counts())

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Transactions",
    "Risk Alerts",
    "Decisions",
    "Agent Actions",
    "Audit Logs"
])

with tab1:
    st.dataframe(transactions)

with tab2:
    st.dataframe(risk)

with tab3:
    st.dataframe(decisions)

with tab4:
    st.dataframe(actions)

with tab5:
    st.dataframe(audit)