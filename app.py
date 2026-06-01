import streamlit as st
import pandas as pd
from data_processor import estimate_vehicle_worth_range, load_and_clean_dataset

st.set_page_config(page_title="Sri Lankan Market Appraiser", page_icon="🇱🇰", layout="wide")

st.title("🇱🇰 Dynamic Market Intelligence Vehicle Appraiser")
st.write("Querying live extracted web indexes to generate data-driven secondary market price ranges.")
st.markdown("---")

# --- COLLAPSIBLE LIVE DATABASE PREVIEW PANEL ---
with st.expander("📦 View Verified Web Scraper Source Database Ledger"):
    try:
        preview_df = load_and_clean_dataset()
        st.dataframe(
            preview_df[['model_name', 'clean_price', 'manufacture_year', 'clean_km']], 
            column_config={
                "model_name": "Scraped Model Label",
                "clean_price": "Clean Market Price (LKR)",
                "manufacture_year": "Year",
                "clean_km": "Recorded Mileage (KM)"
            },
            use_container_width=True,
            hide_index=True
        )
    except Exception as error_context:
        st.error(f"Failed to read data ledger index file. Ensure 'riyasewana-com-2026-05-29-2_partial.xlsx' is present.")

# --- ANALYTICAL MATRIX CONTROLS ---
st.subheader("🔍 Query Target Asset Characteristics")

current_year = 2026
years = list(range(current_year, 1979, -1))

c1, c2, c3 = st.columns(3)
with c1:
    search_model = st.text_input("Type Car Model (e.g., 'Axio', 'Wagon R')", value="Axio")
with c2:
    input_year = st.selectbox("Manufacture Registration Year", options=years, index=years.index(2014))
with c3:
    input_km = st.number_input("Total Mileage Odometer Log (KM)", min_value=0, value=75000, step=5000)

st.markdown("---")

if st.button("📊 Evaluate Statistical Market Worth", type="primary"):
    with st.spinner("Processing local spreadsheet data arrays..."):
        metrics, error = estimate_vehicle_worth_range(search_model, input_year, input_km)
        
    if error:
        st.error(f"❌ Valuation Blocked: {error}")
    else:
        st.success(f"### 📈 Comprehensive Evaluation Report for: '{search_model.upper()}' ({input_year})")
        
        # Render visual KPI metric card blocks
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Target Market Low-End Range", value=f"Rs. {metrics['min_range']:,.2f}")
            st.caption("Common boundary pricing for rapid sales or vehicles requiring minor reconditioning.")
        with m2:
            st.metric(label="Calculated Statistical Average Price", value=f"Rs. {metrics['average']:,.2f}", delta=f"{input_km:,} KM Adjusted")
            st.caption(f"Calculated base normalization average compiled across {metrics['samples_found']} data coordinates.")
        with m3:
            st.metric(label="Target Market Premium Range", value=f"Rs. {metrics['max_range']:,.2f}")
            st.caption("Expected listing price thresholds for vehicles in excellent, mint, or single-owner condition.")