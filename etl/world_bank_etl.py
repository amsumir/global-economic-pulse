import requests
import pandas as pd
import os

# Create the output folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# List of top 20 economies by ISO country code
countries = ["US", "CN", "JP", "DE", "IN", "GB", "FR", "BR", "IT", "CA",
             "RU", "KR", "AU", "ES", "MX", "ID", "NL", "SA", "TR", "CH"]

indicator = "NY.GDP.MKTP.CD"  # GDP (current US$)

all_data = []

for country_code in countries:
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=100"
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to get data for {country_code}")
        continue

    data = response.json()
    if len(data) < 2:
        print(f"No data for {country_code}")
        continue

    records = data[1]
    df = pd.DataFrame(records)
    df = df[["country", "date", "value"]]
    df["country"] = df["country"].apply(lambda x: x["value"])
    df = df.rename(columns={"value": "GDP"})
    df = df.dropna()
    all_data.append(df)

# Combine all into one DataFrame
final_df = pd.concat(all_data)
final_df["date"] = pd.to_datetime(final_df["date"])

# Save to CSV
final_df.to_csv("data/top_20_gdp.csv", index=False)
print("Saved top 20 GDP data to data/top_20_gdp.csv")
