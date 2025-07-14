import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.offline as py

# Connect to the SQLite database
engine = create_engine("sqlite:///db/economic_data.db")

# Define the country and indicator to forecast
country = "United States"
indicator_code = "NY.GDP.MKTP.CD"

# Query GDP data for that country
query = f"""
SELECT date, indicator_value AS GDP
FROM economic_indicators
WHERE country = '{country}'
  AND indicator_code = '{indicator_code}'
ORDER BY date
"""

df = pd.read_sql(query, engine)
df = df.dropna()
df["date"] = pd.to_datetime(df["date"])
df = df.rename(columns={"date": "ds", "GDP": "y"})

# Ensure data is sorted
df = df.sort_values("ds")

# Initialize and train Prophet model
model = Prophet()
model.fit(df)

# Forecast next 5 years (periods = 5, yearly frequency)
future = model.make_future_dataframe(periods=5, freq='Y')
forecast = model.predict(future)

# Save forecast to CSV (optional)
forecast_output = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
forecast_output.to_csv("data/us_gdp_forecast.csv", index=False)

# Plot the forecast
fig = plot_plotly(model, forecast)
py.plot(fig, filename="data/us_gdp_forecast.html")

print("✅ Forecast saved to data/us_gdp_forecast.csv and HTML plot generated.")
