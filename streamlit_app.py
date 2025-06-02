import streamlit as st
import pandas as pd
from forecast import forecast_demand

st.set_page_config(page_title="Merch Planning AI", layout="wide")
st.title("📦 Merchandise Planning AI Agent")

st.markdown("""
Upload your sales data and get inventory and reorder recommendations.

**CSV format required:**
- `sku`: Product identifier
- `date`: Daily sales date (YYYY-MM-DD)
- `units_sold`: Units sold per day
- `current_inventory`: Current stock on hand
- `weeks_cover_target`: Desired weeks of coverage
""")

uploaded_file = st.file_uploader("Upload your sales_data.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded.")

    required_columns = {'sku', 'date', 'units_sold', 'current_inventory', 'weeks_cover_target'}
    if required_columns.issubset(df.columns):
        skus = df["sku"].unique()
        selected_sku = st.selectbox("Select SKU", skus)

        if st.button("🔮 Get Inventory Recommendation"):
            sku_df = df[df["sku"] == selected_sku].copy()
            forecast = forecast_demand(sku_df[['date', 'units_sold']])
            avg_forecast_per_day = forecast["yhat"].mean()
            avg_forecast_per_week = avg_forecast_per_day * 7

            current_inventory = sku_df["current_inventory"].iloc[-1]
            weeks_cover_target = sku_df["weeks_cover_target"].iloc[-1]

            recommended_inventory = round(avg_forecast_per_week * weeks_cover_target)
            reorder_quantity = max(recommended_inventory - current_inventory, 0)

            st.subheader(f"📈 Forecast & Recommendation for {selected_sku}")
            st.write(f"**Average Weekly Demand:** `{round(avg_forecast_per_week)}` units")
            st.write(f"**Current Inventory:** `{current_inventory}` units")
            st.write(f"**Weeks Cover Target:** `{weeks_cover_target}` weeks")
            st.write(f"**Recommended Inventory:** `{recommended_inventory}` units")
            st.write(f"🔁 **Reorder Quantity Needed:** `{reorder_quantity}` units")

            st.line_chart(forecast.set_index("ds")["yhat"])
    else:
        st.error("CSV must include: sku, date, units_sold, current_inventory, weeks_cover_target")
else:
    st.info("👆 Upload a CSV file to begin.")
