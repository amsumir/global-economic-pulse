import requests
import pandas as pd
from sqlalchemy import create_engine
import os

# Setup
os.makedirs("db", exist_ok=True)

countries = ["US", "CN", "JP", "DE", "IN", "GB", "FR", "BR", "IT", "CA",
             "RU", "KR", "AU", "ES", "MX", "ID", "NL", "SA", "TR", "CH"]

indicators = {
    "NY.GDP.MKTP.CD": "GDP (Current US$)",
    "NY.GDP.MKTP.KD.ZG": "GDP Growth (%)",
    "FP.CPI.TOTL.ZG": "Inflation (%)",
    "SL.UEM.TOTL.ZS": "Unemployment (%)",
    "SP.POP.TOTL": "Population"
}

all_data = []

# Loop through each country and each indicator
for ind_code, ind_name in indicators.items():
    for code in countries:
        url = f"https://api.worldbank.org/v2/country/{code}/indicator/{ind_code}?format=json&per_page=100"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Failed: {code}, {ind_code}")
            continue

        try:
            records = response.json()[1]
        except (IndexError, ValueError, TypeError):
            print(f"⚠️ No data: {code}, {ind_code}")
            continue

        df = pd.DataFrame(records)
        df = df[["country", "date", "value"]]
        df["indicator_code"] = ind_code
        df["indicator_name"] = ind_name
        df["country"] = df["country"].apply(lambda x: x["value"])
        df.dropna(inplace=True)
        all_data.append(df)

# Combine all data
final_df = pd.concat(all_data)
final_df["date"] = pd.to_datetime(final_df["date"], errors="coerce")
final_df.rename(columns={"value": "indicator_value"}, inplace=True)

# Save to SQLite
engine = create_engine("sqlite:///db/economic_data.db")
with engine.connect() as conn:
    final_df.to_sql("economic_indicators", conn, if_exists="replace", index=False)

print("✅ All indicators loaded into SQLite: db/economic_data.db → table: economic_indicators")
