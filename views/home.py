import os
import sys
import streamlit as st
from config.constants import *

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cwd)

# ----------- Load Custom CSS -----------
def load_css(file_path):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = os.path.join(cwd, "..", ASSETS_PATH, "styles.css")
load_css(css_path)

# ----------- Dashboard Header -----------
st.title("📦 MX Actual Time of Delivery (ATD) Dashboard")
st.markdown("### Welcome to the ATD performance dashboard for Uber Eats Mexico")

st.markdown("""
At Uber Eats, delivering food at the right time isn’t just about logistics — **it’s about trust**.  
Every late delivery risks a poor customer experience, while every minute of inefficiency affects the bottom line.  
In a marketplace defined by real-time demand, weather variability, and courier availability, **understanding and improving delivery accuracy is a constant challenge — and a major opportunity**.

This dashboard provides insights and trends on Actual Time of Delivery (ATD), empowering teams focused on:
- 🧭 Dispatch planning
- 💸 Courier incentives
- 🕓 ETA accuracy
- 📈 Operational reliability

---

## 🗂 Explore the Dashboard

- 🔍 **[ATD Overview](#Actual-Time-of-Delivery/ATD-Overview)**  
  Analyze ATD trends by courier type, merchant surface, weekday, territory, geo strategy, and more.

---

## 📁 Download the Data

You can download the latest processed dataset here:  
➡️ [**Download BC_A&A_with_ATD.parquet**](data/BC_A&A_with_ATD.parquet)

Or access the original source:  
📄 [**BC_A&A_with_ATD.csv**](data/BC_A&A_with_ATD.csv)

---

## 🧾 Key Metrics (From the Original Source)

### Source: `BC_A&A_with_ATD.csv`

1. **Region** – Broad regional label *(e.g. "Mexico")*  
2. **Territory** – Operational subdivision *(e.g. "North", "Central")*  
3. **Courier Flow** – Type of courier *(e.g. "Motorbike", "Logistics")*  
4. **Merchant Surface** – Platform used *(e.g. "Tablet", "POS")*  
5. **Pickup & Dropoff Distances** – In kilometers  
6. **Timestamps** – Restaurant offer time, delivery completion time, eater request time  
7. **ATD** – Total minutes from restaurant offer to final delivery

---

## 🧮 Additional Metrics (Enriched in `.parquet`)

- **Hour**, **Weekday**, **Day**, **Week**, **Month**
- **Time of Day Bucket** (Breakfast, Lunch, Dinner, Late Night)
- **Is Weekend?** – Boolean
- **Is Holiday?** – Based on custom calendar
- **Total Distance** – Pickup + Dropoff distance in KM

---
""")