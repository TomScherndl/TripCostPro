from dashboarding.models.Commodity import Commodity
from dashboarding.models.Globals import FREQUENCY, FUEL_KWH_PER_L, MAX_TIME, MIN_TIME, TIME_ZONE


import pandas as pd
import streamlit as st


@st.cache_data
def get_electricity_prices():
    prices = pd.read_csv("data/electricity_2024_2025.csv")
    prices = prices.rename(columns={"Unnamed: 0": "date", "0": Commodity.ELETRICITY})

    prices = prices.set_index("date")
    prices.index = pd.to_datetime(prices.index, format="%Y-%m-%d %H:%M:%S%z",utc=True)

    prices = prices.resample(FREQUENCY).mean()
    prices = prices.reindex(st.session_state.time_index).interpolate(method="linear")

    prices = prices.sort_index()

    prices = prices.loc[MIN_TIME:MAX_TIME]
    return prices


@st.cache_data
def get_fuel_prices():
    prices_2024 = pd.read_csv("data/fuel_prices_2024.csv", sep=";", decimal=",")
    prices_2025 = pd.read_csv("data/fuel_prices_2025.csv", sep=";", decimal=",")

    prices = pd.concat([prices_2024, prices_2025])
    prices = prices_2024
    prices = prices.loc[
        :,
        [
            "Stichtag",
            Commodity.DIESEL,
            Commodity.EUROSUPER,
            Commodity.NORMAL,
            Commodity.SUPER_PLUS,
        ],
    ]
    prices = prices.set_index("Stichtag")
    prices.index = pd.to_datetime(prices.index, dayfirst=True)
    prices = prices.tz_localize(TIME_ZONE)
    prices = prices.resample(FREQUENCY).mean()

    prices = prices.reindex(st.session_state.time_index).interpolate(method="linear")

    for col, kwh_l in FUEL_KWH_PER_L.items():
        prices[col] = prices[col] * (1000.0 / kwh_l)

    prices = prices.sort_index()

    prices = prices.loc[MIN_TIME:MAX_TIME]
    return prices


@st.cache_data
def get_all_prices(electricity_prices, fuel_prices):
    all_prices = pd.concat(
        [electricity_prices, fuel_prices], axis=1, join="inner"
    ).dropna()
    all_prices = all_prices.sort_index()
    return all_prices