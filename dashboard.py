import streamlit as st
import pandas as pd
import os
from pathlib import Path

st.set_page_config(page_title="Distributed Log Monitoring", layout="wide")
st.title("📊 Distributed Log Monitoring Dashboard")

# ==========================
# Absolute path for logs.csv
# ==========================
BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "server" / "logs.csv"  # assumes server/logs.csv relative to this dashboard.py

# Load CSV safely
def load_data():
    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE)
    else:
        return pd.DataFrame(columns=["timestamp","client_ip","level","category","service","component","message"])

df = load_data()

# ==========================
# Metrics
# ==========================
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
col1.metric("Total Logs", len(df))
col2.metric("Unique Clients", df["client_ip"].nunique())
col3.metric("Unique Categories", df["category"].nunique())
col4.metric("Unique Services", df["service"].nunique())
col5.metric("Unique Components", df["component"].nunique())
col6.metric("Unique Levels", df["level"].nunique())
col7.metric("Most Common Level", df["level"].mode()[0] if not df.empty else "N/A")


st.divider()

# ==========================
# Logs Table
# ==========================
st.subheader("📋 Logs Table")
st.dataframe(df, use_container_width=True)

st.divider()

# ==========================
# Filter Logs
# ==========================
st.subheader("🔍 Filter Logs")
selected_level = st.selectbox("Filter by Level", ["All"] + list(df["level"].unique()))
selected_client = st.selectbox("Filter by Client", ["All"] + list(df["client_ip"].unique()))

filtered_df = df.copy()

if selected_level != "All":
    filtered_df = filtered_df[filtered_df["level"] == selected_level]

if selected_client != "All":
    filtered_df = filtered_df[filtered_df["client_ip"] == selected_client]

st.dataframe(filtered_df, use_container_width=True)

# ==========================
# Auto-refresh safely
# ==========================
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=2000, key="refresh")  # refresh every 2 seconds