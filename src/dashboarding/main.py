import itertools
import logging
from typing import Any
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
from dataclasses import dataclass

from dashboarding.models.CarColumns import CarColumns
from dashboarding.models.Commodity import Commodity
from dashboarding.services.create_prices import create_prices
from dashboarding.services.create_trip_calculator import create_trip_calculator
from dashboarding.services.load_data import get_electricity_prices
from dashboarding.services.load_data import get_fuel_prices
from dashboarding.services.load_data import get_all_prices
from dashboarding.models.Globals import (
    FREQUENCY,
    DATE_FORMAT,
    MIN_TIME,
    MAX_TIME
)

def main(download_data: bool = True):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dashboard!")

    initialize_session()

    electricity_prices = get_electricity_prices()
    fuel_prices = get_fuel_prices()
    all_prices = get_all_prices(electricity_prices, fuel_prices)

    st.markdown("# Energy prices dashboard")

    create_prices(all_prices)
    create_trip_calculator(all_prices)

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


if __name__ == "__main__":
    main()
