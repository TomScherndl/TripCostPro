# Energy and Petrol Price Dashboard:

Muhammed Ali Tosun & Thomas Scherndl (**Team MATS**)

Task: Prepare a question (+data) to answer with a dashboard (maturity level 3+) and identify the tech stack you would use for this

## Research Question

We will investigate the following:

-   **Cost Comparison:** What are the historical cost deltas between Electric Vehicles (EV) and Fuel Vehicles (FV) per 100km?

-   **Fueling Strategy:** What are the predicted prices for the next 48 hours? How much would it cost for a given vehicle (chosen from a small given list of cars)

-   **Actionable Insight:** Based on price trends, should a user charge/refill today or wait for a predicted dip?

```         
Note: 
We are absolutely aware that especially the petrol prices will not be easily forecasted and may depend on a lot of [unknown](??), [unpredictable](https://www.whitehouse.gov/administration/donald-j-trump/) or [irrational](https://www.whitehouse.gov/administration/donald-j-trump/) factors. However, the scope of this project is not making it accurate but flashy and nice to look at. 
```

## Data Sources

### ENTSOE

The European Network of Transmission System Operators for Electricity provides real-time and day-ahead load, generation, and price data via their Transparency Platform API.

### Tankerkönig

This is a German gas station price API providing historical and live retail prices for Diesel, Super E5, and E10 across Germany under Creative Commons licenses.

## Dashboard

The dashboard will feature:

-   **Current Price Toggle:** Live comparison of average kWh vs. fuel liter prices and 48h (day-ahead) prediction.

-   **Savings Calculator**: A "What-If" tool to see historical savings based on specific car models/efficiency. Possibility to indicate number of km driven; choice between different car model types (SUV vs. small car type; radio button boxes have influence on saved € amount).

-   **A "Buy-Wait" Signal**: A color-coded recommendation (Green/Yellow/Red) based on the 48h forecast. This will be based on the user input of how much money they still have left and current and predicted prices for the next days. Green indicates a suggestion to buy now, yellow to buy within 2 days, red to postpone filling up your tank given current and predicted prices and the given budget.

## Tech Stack

-   **Data Retrieval:** `entsoe-py` for electricity day-ahead prices and historical electricity data (Tankerkönig’s data is a simple csv obtained from their internal git).

-   **Data Processing:** `pandas` and `numpy` for cleaning and feature engineering.

-   **Modeling:** `TiRex` (xLSTM distillation) for time-series forecasting.

-   **Visualization:** `plotly` for interactive time-series and `streamlit` for the web-based UI.