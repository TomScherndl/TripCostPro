import itertools
import logging
from typing import Any
from zoneinfo import ZoneInfo
from code.entsoe_download import load_data_from_entsoe
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
from enum import StrEnum
from dataclasses import dataclass
from datetime import timedelta

TIME_ZONE = "Europe/Brussels"
FREQUENCY = "h"
DATE_FORMAT = "YYYY-MM-DD HH:mm"
MIN_TIME = pd.Timestamp("20241201", tz=TIME_ZONE)
MAX_TIME = pd.Timestamp("20250101", tz=TIME_ZONE)


class Commodity(StrEnum):
    DIESEL = "Diesel"
    EUROSUPER = "Eurosuper"
    NORMAL = "Normal"
    SUPER_PLUS = "Super Plus"
    ELETRICITY = "Electricity"


class CarColumns(StrEnum):
    NAME = "Name"
    COMMODITY = "Commodity"
    Consumption = "Consumption"
    TRIP_COST = "Trip cost (EUR)"
    IN_BUDGET = "In budget"


FUEL_KWH_PER_L = {
    Commodity.DIESEL.value: 9.7,
    Commodity.EUROSUPER.value: 8.9,
    Commodity.NORMAL.value: 8.9,
    Commodity.SUPER_PLUS.value: 8.9,
}


def main(download_data: bool = True):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dashboard!")

    initialize_session()

    electricity_prices = get_electricity_prices()
    fuel_prices = get_fuel_prices()
    all_prices = get_all_prices(electricity_prices,fuel_prices)

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
                options=[c.value for c in Commodity],
                required=True,
                default=Commodity.DIESEL.value,
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
    electricity_prices = load_data_from_entsoe(start=MIN_TIME, end=MAX_TIME)
    electricity_prices = electricity_prices.reindex(
        st.session_state.time_index
    ).interpolate(method="linear")
    electricity_prices = electricity_prices.to_frame(name=Commodity.ELETRICITY.value)
    electricity_prices = electricity_prices.sort_index()
    return electricity_prices


@st.cache_data
def get_fuel_prices():
    fuel_2024 = pd.read_csv("data/fuel_prices_2024.csv", sep=";", decimal=",")
    fuel_2025 = pd.read_csv("data/fuel_prices_2025.csv", sep=";", decimal=",")

    # fuel = pd.concat([fuel_2024, fuel_2025])
    fuel = fuel_2024
    fuel = fuel.loc[
        :,
        [
            "Stichtag",
            Commodity.DIESEL.value,
            Commodity.EUROSUPER.value,
            Commodity.NORMAL.value,
            Commodity.SUPER_PLUS.value,
        ],
    ]
    fuel = fuel.set_index("Stichtag")
    fuel.index = pd.to_datetime(fuel.index, dayfirst=True)
    fuel = fuel.tz_localize(TIME_ZONE)
    fuel = fuel.resample(FREQUENCY).mean()

    fuel = fuel.reindex(st.session_state.time_index).interpolate(method="linear")

    for col, kwh_l in FUEL_KWH_PER_L.items():
        fuel[col] = fuel[col] * (1000.0 / kwh_l)

    fuel = fuel.sort_index()
    return fuel

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
                CarColumns.COMMODITY: [Commodity.DIESEL.value],
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
    commodity = row[CarColumns.COMMODITY.value]

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
