import streamlit as st
import pandas as pd
from forecast import forecast_demand

st.set_page_config(page_title="Merch Planning AI", layout="wide")
st.title("📦 Merchandise Planning AI Agent")

st.markdown("Upload your sales data and get inventory recommendations.")

uploaded_file = st.file_uploader("Upload your sales_data.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded.")

    if {'sku', 'date', 'units_sold'}.issubset(df.columns):
        skus = df["sku"].unique()
        selected_sku = st.selectbox("Select SKU", skus)

        if st.button("🔮 Forecast Inventory"):
            sku_df = df[df["sku"] == selected_sku]
            forecast = forecast_demand(sku_df)
            avg_forecast = round(forecast["yhat"].mean())

            st.subheader(f"📈 Forecast for {selected_sku}")
            st.write(f"**Suggested inventory for next 30 days:** `{avg_forecast}` units")
            st.line_chart(forecast.set_index("ds")["yhat"])
    else:
        st.error("CSV must include: sku, date, units_sold")
else:
    st.info("👆 Upload a CSV file to begin.")
