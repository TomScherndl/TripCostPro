import itertools
import logging
from typing import Any
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
from dataclasses import dataclass

from dashboarding.models.TabNames import TabNames
from dashboarding.models.CarColumns import CarColumns
from dashboarding.models.Commodity import Commodity

from dashboarding.models.Globals import FREQUENCY, DATE_FORMAT, MIN_TIME, MAX_TIME, TIME_ZONE

from dashboarding.services.load_data import (
    get_electricity_prices,
    get_fuel_prices_comparable,
)
from dashboarding.services.load_data import get_fuel_prices
from dashboarding.services.load_data import get_all_prices

from dashboarding.services.create_prices import create_prices
from dashboarding.services.create_trip_calculator import create_trip_calculator
from dashboarding.services.create_cars import create_cars
from dashboarding.services.create_overview import create_overview

def create_dashboard():    
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dashboard!")

    initialize_session()

    electricity_prices = get_electricity_prices()
    fuel_prices = get_fuel_prices()
    fuel_prices_comparable = get_fuel_prices_comparable()
    all_prices = get_all_prices(
        electricity_prices,
        fuel_prices_comparable,
    )

    st.markdown("# Optimal Car Choice and Fleet Management Dashboard")

    tabs = st.tabs(
        tabs=[t.value for t in TabNames],
        on_change="rerun")
    tabs_by_name = dict(zip(TabNames, tabs))
    st.session_state.tabs_by_name = tabs_by_name

    with tabs_by_name[TabNames.OVERVIEW]:
        create_overview(
            all_prices,
            electricity_prices,
            fuel_prices
        )

    with tabs_by_name[TabNames.PRICES]:
        create_prices(
            all_prices,
            electricity_prices,
            fuel_prices,
        )

    with tabs_by_name[TabNames.TRIP_PLANNER]:
        create_trip_calculator(all_prices)

    with tabs_by_name[TabNames.CARS]:
        create_cars()


def initialize_session():
    # hide sidebar on first load
    st.set_page_config(initial_sidebar_state="collapsed")
    
    st.session_state.active_tab = TabNames.OVERVIEW
    if "time_range" not in st.session_state:
        st.session_state.time_range = [
            MIN_TIME,
            MAX_TIME,
        ]

        st.session_state.time_index = pd.date_range(
            start=st.session_state.time_range[0],
            end=st.session_state.time_range[1],
            freq=FREQUENCY,
            tz=TIME_ZONE
        )