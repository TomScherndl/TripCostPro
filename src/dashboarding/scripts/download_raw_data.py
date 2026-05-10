from dashboarding.scripts.entsoe_download import load_data_from_entsoe
import pandas as pd

TIME_ZONE = "Europe/Brussels"
FREQUENCY = "h"
DATE_FORMAT = "YYYY-MM-DD HH:mm"
MIN_TIME = pd.Timestamp("20240101", tz=TIME_ZONE)
MAX_TIME = pd.Timestamp("20270101", tz=TIME_ZONE)

def load_entsoe_data_raw():
    print(f"Getting prices from {MIN_TIME} to {MAX_TIME}")
    prices = load_data_from_entsoe(start=MIN_TIME, end=MAX_TIME)
    prices.to_csv("electricity_2024_2025_start_2026.csv")


if __name__ == "__main__":
    load_entsoe_data_raw()