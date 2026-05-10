from dashboarding.models.Commodity import Commodity
from dashboarding.models.Globals import (
    FREQUENCY,
    FUEL_KWH_PER_L,
    MAX_TIME,
    MIN_TIME,
    TIME_ZONE,
)

import pandas as pd
import streamlit as st


@st.cache_data
def get_electricity_prices():
    # ENTSOE data until 09.05.2026. Rest is predicted by Gemini
    prices = pd.read_csv("data/electricity_2024_2025_2026.csv")
    prices = prices.rename(columns={"Unnamed: 0": "date", "0": Commodity.ELETRICITY})

    prices = prices.set_index("date")
    prices.index = pd.to_datetime(
        prices.index,
        format="%Y-%m-%d %H:%M:%S%z",
        utc=True,
    )

    prices = normalize_to_same_timeseries(prices)
    return prices


@st.cache_data
def get_fuel_prices():
    # Original from bundesministerium
    prices_2024 = pd.read_csv("data/fuel_prices_2024.csv", sep=";", decimal=",")
    # Original from bundesministerium, but "Normal" has been predicted by Gemini
    prices_2025 = pd.read_csv(
        "data/fuel_prices_2025_with_normal.csv", sep=";", decimal=","
    )
    # Original from bundesministerium until 10.05. "Normal" and rest of 2026 has been predicted by Gemini.
    prices_2026 = pd.read_csv(
        "data/fuel_prices_2026_full_year.csv", sep=";", decimal=","
    )

    prices = pd.concat([prices_2024, prices_2025, prices_2026])
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
    prices.index = pd.to_datetime(
        prices.index,
        dayfirst=True,
        utc=True,
    )

    prices = normalize_to_same_timeseries(prices)
    return prices


@st.cache_data
def get_fuel_prices_comparable():
    prices = get_fuel_prices().copy()
    for col, kwh_l in FUEL_KWH_PER_L.items():
        prices[col] = prices[col] * (1000.0 / kwh_l)
    return prices


@st.cache_data
def get_all_prices(electricity_prices, fuel_prices_comparable):
    all_prices = pd.concat(
        [electricity_prices, fuel_prices_comparable],
        axis=1,
        join="inner",
    )
    all_prices = all_prices.sort_index()
    return all_prices


def normalize_to_same_timeseries(df):
    if df.index.tz is None:
        df.index = df.index.tz_localize(TIME_ZONE)
    else:
        df.index = df.index.tz_convert(TIME_ZONE)

    df = df.resample(FREQUENCY).mean()
    df = df.reindex(st.session_state.time_index).interpolate(method="linear")
    df = df.sort_index()
    df = df.loc[MIN_TIME:MAX_TIME]
    return df
