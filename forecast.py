import pandas as pd
from prophet import Prophet

def forecast_demand(df: pd.DataFrame, periods=30):
    df = df.rename(columns={"date": "ds", "units_sold": "y"})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].tail(periods)
