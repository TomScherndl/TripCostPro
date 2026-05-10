import itertools
import logging
from typing import Any
from zoneinfo import ZoneInfo
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
from dataclasses import dataclass
from datetime import timedelta

from src.dashboarding.models.CarColumns import CarColumns
from src.dashboarding.models.Commodity import Commodity
from src.dashboarding.models.Globals import (
    TIME_ZONE,
    FREQUENCY,
    DATE_FORMAT,
    MIN_TIME,
    MAX_TIME,
    FUEL_KWH_PER_L
)

def main(download_data: bool = True):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dashboard!")

    initialize_session()

    electricity_prices = get_electricity_prices()
    fuel_prices = get_fuel_prices()
    all_prices = get_all_prices(electricity_prices, fuel_prices)

    st.markdown("# Energy prices dashboard")

    st.markdown("## Price comparison")
    fig = px.line(
        all_prices,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (EUR/MWh)",
        legend_title_text="Commodity",
        hovermode="closest",
        dragmode=False,
    )
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    st.markdown("## Savings calculator")

    st.markdown("### Trip information")
    trip_date = st.datetime_input(
        label="Trip date",
        min_value=all_prices.index[0],
        max_value=all_prices.index[-1],
        value=all_prices.index[0],
        step=timedelta(hours=1),
    )
    trip_date = trip_date.replace(tzinfo=ZoneInfo(TIME_ZONE))
    trip_distance_km = st.number_input(
        label="Trip distance (km)",
        min_value=1,
        value=100,
    )

    trip_budget_eur = st.number_input(
        label="Trip budget (EUR)",
        min_value=1,
        value=500,
    )

    commodity_prices_at_trip_date = all_prices.loc[trip_date]
    fig = px.bar(commodity_prices_at_trip_date)
    fig.update_layout(
        xaxis_title=CarColumns.COMMODITY,
        yaxis_title="Price (EUR/MWh)",
        legend_title_text="Trip time",
        hovermode="closest",
        dragmode=False,
    )
    st.plotly_chart(fig)

    st.markdown("### Car information")
    updated_cars = st.data_editor(
        st.session_state.cars,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            CarColumns.NAME: st.column_config.TextColumn(
                label=CarColumns.NAME, required=True, default="Ford Ka"
            ),
            CarColumns.COMMODITY: st.column_config.SelectboxColumn(
                label=CarColumns.COMMODITY,
                options=[c for c in Commodity],
                required=True,
                default=Commodity.DIESEL,
            ),
            CarColumns.Consumption: st.column_config.NumberColumn(
                label=CarColumns.Consumption,
                min_value=0.0,
                step=0.1,
                help="kWh/100km for EV, l/100km for fuel cars",
                required=True,
                default=5.0,
            ),
            CarColumns.TRIP_COST: st.column_config.NumberColumn(
                label=CarColumns.TRIP_COST,
                disabled=True,
                format="€ %.2f",
                default=0.0,
            ),
            CarColumns.IN_BUDGET: st.column_config.CheckboxColumn(
                label=CarColumns.IN_BUDGET,
                disabled=True,
                default=False,
            ),
        },
    )
    updated_cars = updated_cars.apply(
        lambda row: calculate_outputs(
            row,
            commodity_prices_at_trip_date,
            trip_distance_km,
            trip_budget_eur,
        ),
        axis=1,
    )

    if not updated_cars.equals(st.session_state.cars):
        st.session_state.cars = updated_cars
        st.rerun()


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


def initialize_session():
    if "time_range" not in st.session_state:
        st.session_state.time_range = [
            MIN_TIME,
            MAX_TIME,
        ]

        st.session_state.time_index = pd.date_range(
            start=st.session_state.time_range[0],
            end=st.session_state.time_range[1],
            freq=FREQUENCY,
        )

    if "cars" not in st.session_state:
        st.session_state.cars = pd.DataFrame(
            {
                CarColumns.NAME: ["Ford Ka"],
                CarColumns.COMMODITY: [Commodity.DIESEL],
                CarColumns.Consumption: [5.0],
                CarColumns.TRIP_COST: 0,
                CarColumns.IN_BUDGET: False,
            }
        )


def calculate_outputs(
    row,
    commodity_prices_at_trip_date,
    trip_distance_km,
    trip_budget_eur,
):
    commodity = row[CarColumns.COMMODITY]

    cost_eur_per_wh = commodity_prices_at_trip_date[commodity] / (1000 * 1000)

    if commodity == Commodity.ELETRICITY:
        wh_consumption_per_km = 1000 * row[CarColumns.Consumption] / (100)
    else:
        l_consumption_per_km = row[CarColumns.Consumption] / 100
        fuel_wh_per_l = FUEL_KWH_PER_L[commodity] * 1000
        wh_consumption_per_km = l_consumption_per_km * fuel_wh_per_l

    trip_price_eur = cost_eur_per_wh * wh_consumption_per_km * trip_distance_km
    is_trip_in_budget = trip_price_eur <= trip_budget_eur

    row[CarColumns.TRIP_COST] = trip_price_eur
    row[CarColumns.IN_BUDGET] = is_trip_in_budget

    return row


if __name__ == "__main__":
    main()
