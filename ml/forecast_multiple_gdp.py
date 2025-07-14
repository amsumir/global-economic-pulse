import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.offline as py
import os

# Create output directories
os.makedirs("data/forecasts", exist_ok=True)
os.makedirs("data/charts", exist_ok=True)

# Connect to the database
engine = create_engine("sqlite:///db/economic_data.db")

# List of top 10 countries by GDP for demo
countries = [
    "United States", "China", "Japan", "Germany", "India",
    "United Kingdom", "France", "Brazil", "Italy", "Canada"
]

indicator_code = "NY.GDP.MKTP.CD"  # GDP (Current US$)

for country in countries:
    print(f"📈 Forecasting GDP for: {country}")

    # Fetch historical GDP data
    query = f"""
    SELECT date, indicator_value AS GDP
    FROM economic_indicators
    WHERE country = '{country}'
      AND indicator_code = '{indicator_code}'
    ORDER BY date
    """
    df = pd.read_sql(query, engine)
    df.dropna(inplace=True)

    if df.empty:
        print(f"⚠️ No data for {country}")
        continue

    # Prepare data for Prophet
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"date": "ds", "GDP": "y"})
    df = df.sort_values("ds")

    # Fit the Prophet model
    model = Prophet()
    model.fit(df)

    # Forecast next 5 years
    future = model.make_future_dataframe(periods=5, freq="Y")
    forecast = model.predict(future)

    # Save forecast to CSV
    out_csv = f"data/forecasts/{country.lower().replace(' ', '_')}_gdp_forecast.csv"
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(out_csv, index=False)

    # Save chart to HTML
    fig = plot_plotly(model, forecast)
    out_html = f"data/charts/{country.lower().replace(' ', '_')}_gdp_forecast.html"
    py.plot(fig, filename=out_html, auto_open=False)

    print(f"✅ Done: {country} → CSV + Chart saved")

print("🎉 All forecasts generated.")
