import streamlit as st
import pandas as pd
from forecast import forecast_demand

st.set_page_config(page_title="Merch Planning AI", layout="wide")
st.title("📦 Merchandise Planning AI Agent")

st.markdown("""
Upload your sales data and get smarter inventory planning.

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

        if st.button("📊 Analyze & Recommend"):
            sku_df = df[df["sku"] == selected_sku].copy()

            forecast = forecast_demand(sku_df[['date', 'units_sold']])
            avg_forecast_per_week = forecast["yhat"].mean()

            current_inventory = sku_df["current_inventory"].iloc[-1]
            weeks_cover_target = sku_df["weeks_cover_target"].iloc[-1]

            recommended_inventory = round(avg_forecast_per_week * weeks_cover_target)
            reorder_quantity = max(recommended_inventory - current_inventory, 0)

            st.subheader(f"🧠 Recommendations for {selected_sku}")
            col1, col2, col3 = st.columns(3)
            col1.metric("📦 Avg Weekly Demand", round(avg_forecast_per_week))
            col2.metric("🏷️ Current Inventory", current_inventory)
            col3.metric("📌 Reorder Qty Needed", reorder_quantity)

            st.subheader("📈 Forecast Chart (Weekly)")
            st.line_chart(forecast.set_index("ds")[["yhat", "yhat_lower", "yhat_upper"]])

            csv_download = forecast.to_csv(index=False)
            st.download_button("⬇️ Download Forecast CSV", csv_download, file_name="forecast.csv")
    else:
        st.error("CSV must include: sku, date, units_sold, current_inventory, weeks_cover_target")
else:
    st.info("👆 Upload a CSV file to begin.")
