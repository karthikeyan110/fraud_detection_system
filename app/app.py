import streamlit as st
import pandas as pd
import time
import random
import requests
import sqlite3
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.predict import predict_transaction
from src.database import insert_transaction

st.set_page_config(page_title="Fraud Detection System", layout="wide")

def generate_transaction():
    return {
        "Time": random.uniform(0, 200000),
        "Amount": random.choice([100, 500, 2000, 10000, 50000, 80000]),
        **{f"V{i}": random.uniform(-3, 3) for i in range(1, 29)}
    }

st.title("🚨 AI-Powered Fraud Detection Dashboard")

# -------------------------------
# DATABASE FUNCTION
# -------------------------------
def load_data():
    conn = sqlite3.connect("transactions.db")
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df


# -------------------------------
# SIDEBAR INPUT
# -------------------------------
st.sidebar.header("🔍 Test Transaction")

amount = st.sidebar.number_input("Amount", 1.0, 100000.0, 5000.0)
time_val = st.sidebar.number_input("Time", 0.0, 200000.0, 10000.0)


# -------------------------------
# PREDICT BUTTON (API CALL)
# -------------------------------
if st.sidebar.button("Predict"):

    sample = {
        "Time": time_val,
        "Amount": amount,
        **{f"V{i}": random.uniform(-3, 3) for i in range(1, 29)}
    }

    try:
        res = requests.post("http://127.0.0.1:8000/predict", json=sample)

        if res.status_code == 200:
            result = res.json()

            if result["prediction"] == "FRAUD":
                st.sidebar.error(f"🚨 FRAUD (Score: {result['fraud_score']:.2f})")
            else:
                st.sidebar.success(f"✅ NORMAL (Score: {result['fraud_score']:.2f})")

        else:
            st.sidebar.error("API Error")

    except:
        st.sidebar.error("Cannot connect to API")


# -------------------------------
# KPI SECTION
# -------------------------------
st.subheader("📊 System Overview")

# -------------------------------
# AUTO-GENERATE NEW DATA (REAL-TIME SIMULATION)
# -------------------------------
new_data = generate_transaction()

columns_order = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]
df_new = pd.DataFrame([new_data])[columns_order]

score, label, reasons = predict_transaction(df_new)
insert_transaction(new_data, score, label)

# Now load updated data
df = load_data()

col1, col2, col3 = st.columns(3)

total_tx = len(df)
fraud_tx = len(df[df["label"] == "FRAUD"]) if not df.empty else 0
normal_tx = total_tx - fraud_tx

with col1:
    st.metric("Total Transactions", total_tx)

with col2:
    st.metric("Fraud Detected 🚨", fraud_tx)

with col3:
    st.metric("Normal Transactions ✅", normal_tx)

if fraud_tx > 0:
    st.warning("⚠️ Fraud transactions detected!")

if not df.empty:
    latest = df.iloc[-1]
    if latest["label"] == "FRAUD":
        st.toast(f"🚨 FRAUD DETECTED! Amount: ${latest['Amount']:,.2f}", icon="🚨")
        st.error(f"🚨 FRAUD DETECTED! Amount: ${latest['Amount']:,.2f}")


# -------------------------------
# REAL-TIME DASHBOARD
# -------------------------------
st.header("📡 Auto-Monitoring Active")

col1, col2 = st.columns(2)

# -------------------------------
# RECENT TRANSACTIONS
# -------------------------------
with col1:
    st.subheader("📊 Recent Transactions")
    if not df.empty:
        st.dataframe(df.tail(10), width="stretch")
    else:
        st.info("No data yet")


# -------------------------------
# FRAUD ALERTS
# -------------------------------
with col2:
    st.subheader("🚨 High Risk Alerts")

    if not df.empty:
        frauds = df[df["label"] == "FRAUD"]

        if not frauds.empty:
            st.dataframe(
                frauds.tail(5).style.map(
                    lambda x: "background-color: red; color: white"
                ),
                width="stretch"
            )
        else:
            st.info("No fraud detected yet")


# --- GRAPH ---
st.subheader("📈 Fraud Trends")

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        # ----------- PIE CHART -----------
        st.markdown("### 🥧 Fraud Distribution")

        counts = df["label"].value_counts()

        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(
            counts.values,
            labels=counts.index,
            autopct='%1.1f%%',
            startangle=90
        )
        ax1.set_title("Fraud vs Normal Transactions")
        fig1.patch.set_alpha(0)
        st.pyplot(fig1)

        # ----------- REASON VISUALIZATION -----------
        st.markdown("### 🔍 Fraud Reason Breakdown")

        frauds_df = df[df["label"] == "FRAUD"]

        if not frauds_df.empty:

            all_reasons = []

            for _, row in frauds_df.iterrows():

                # ✅ Allow multiple reasons (NOT elif)
                if row["Amount"] > 50000:
                    all_reasons.append("Very large transaction")

                if row["Amount"] > 10000:
                    all_reasons.append("High transaction amount")

                if row["Time"] < 10000:
                    all_reasons.append("Odd time")

                if row["Amount"] <= 10000 and row["Time"] >= 10000:
                    all_reasons.append("ML Model Detection")

            # ✅ Sort properly
            reason_counts = (
                pd.Series(all_reasons)
                .value_counts()
                .sort_values(ascending=True)
            )

            # ✅ Better sized graph
            fig3, ax3 = plt.subplots(figsize=(6, 3))

            bars = ax3.barh(
                reason_counts.index,
                reason_counts.values,
                color="#ff4b4b"
            )

            # ✅ Add numbers on bars
            for i, v in enumerate(reason_counts.values):
                ax3.text(v + 0.2, i, str(v), va='center')

            ax3.set_xlabel("Count")
            ax3.set_title("Top Fraud Reasons")

            # ✅ Clean look
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)

            fig3.tight_layout()
            st.pyplot(fig3)

        else:
            st.info("No fraud data to visualize.")

    with col2:
        # ----------- TREND BAR CHART -----------
        st.markdown("### 📊 Transaction Trend (Smoothed)")

        df_sorted = df.sort_values(by="Time").reset_index(drop=True)

        # Create batch groups (every 10 transactions)
        df_sorted["batch"] = df_sorted.index // 10

        # Aggregate (mean fraud score per batch)
        grouped = df_sorted.groupby(["batch", "label"])["fraud_score"].mean().unstack()

        fig2, ax2 = plt.subplots(figsize=(5, 3))

        if "FRAUD" in grouped.columns:
            ax2.plot(grouped.index, grouped["FRAUD"], marker='o', label="FRAUD")

        if "NORMAL" in grouped.columns:
            ax2.plot(grouped.index, grouped["NORMAL"], marker='o', label="NORMAL")

        ax2.axhline(y=0.5, linestyle='--', color='red', label='Fraud Threshold')

        ax2.set_title("Smoothed Transaction Trend")
        ax2.set_xlabel("Transaction Batches")
        ax2.set_ylabel("Average Fraud Score")
        fig2.patch.set_alpha(0)

        ax2.legend()

        st.pyplot(fig2)

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------
st.markdown("---")
st.download_button(
    label="📥 Download Transactions CSV",
    data=df.to_csv(index=False),
    file_name="transactions.csv",
    mime="text/csv"
)

time.sleep(2)
st.rerun()
