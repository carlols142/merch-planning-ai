import pandas as pd
from prophet import Prophet

def forecast_demand(df: pd.DataFrame, periods=12):
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby(pd.Grouper(key='date', freq='W'))['units_sold'].sum().reset_index()
    df = df.rename(columns={"date": "ds", "units_sold": "y"})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods, freq='W')
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
