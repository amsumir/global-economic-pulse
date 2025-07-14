📈 How the Forecast Works
Forecasting is done using the Prophet library from Meta, which is great for time series with seasonal and trend components.

For each country:

We pull historical GDP data

Train a model

Forecast the next 5 years

Save both the forecast and the visual chart

🖼️ Outputs You Can Use
.csv files per country: ready to load into Power BI or Excel

.html interactive charts: open in any browser

SQLite database: can be queried directly or connected to a BI tool

📊 Power BI Dashboard (Optional)
You can connect either:

The data/forecasts/*.csv files

Or the SQLite database directly (db/economic_data.db)

From there you can build slicers, KPIs, time series visuals, and compare actual vs predicted GDP for any country.

🤖 ML Techniques Used
Time series forecasting with Prophet

Auto handling of trend and seasonality

Confidence intervals for uncertainty

Can be extended to:

Compare actual vs forecast

Combine multiple indicators

📌 Why This Project Matters
This is not just a tutorial. It’s a project that simulates real-world work:

Building data pipelines

Using live APIs

Managing environments and code structure

Applying machine learning to real data

Preparing outputs for decision-making tools

You can list this on your resume or show it in interviews as a real, production-style project.

🙋‍♂️ About Me
This project was created by me.
I'm a data analyst and developer interested in solving real-world problems using data and AI. I mean we can't ignore it's existence right?

You can find me on GitHub: @amsumir

📌 Future Improvements
Automate ETL with scheduling (e.g., cron, Airflow)

Add support for inflation, unemployment, and population forecasting

Build a web-based dashboard with Streamlit or Flask

Deploy the pipeline to the cloud (AWS, Azure, etc.)

