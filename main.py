import logging
from code.entsoe_download import load_data_from_entsoe
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd

TIME_ZONE = "Europe/Brussels"
FREQUENCY = "h"
DATE_FORMAT = "YYYY-MM-DD HH:mm"
MIN_TIME = pd.Timestamp("20241201", tz=TIME_ZONE)
MAX_TIME = pd.Timestamp("20250101", tz=TIME_ZONE)


def main(download_data: bool = True):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Dashboard!")

    initialize_session()

    electricity_prices = get_electricity_prices(download_data)
    fuel_prices = get_fuel_prices()

    st.markdown("# Dashboard Content")

    time_range = setup_and_get_time_range_slider()

    st.line_chart(data=electricity_prices)
    st.line_chart(data=fuel_prices)

    buy_window = st.slider(
        "Buy window",
        min_value=MIN_TIME.to_pydatetime(),
        max_value=MAX_TIME.to_pydatetime(),
        value=(MIN_TIME.to_pydatetime(), MAX_TIME.to_pydatetime()),
        format="YYYY-MM-DD HH:mm",
    )

    age = st.number_input("Enter your age", min_value=0, max_value=120, value=25)

    plt.show()


def get_electricity_prices(download_data):
    if download_data:
        electricity_prices = load_data_from_entsoe()
        logging.info("Data downloaded successfully.")
    
    electricity_prices = (electricity_prices
                          .reindex(st.session_state.time_index)
                          .interpolate(method="linear"))
    electricity_prices = electricity_prices.to_frame(name="electricity")
    return electricity_prices


def get_fuel_prices():
    fuel_2024 = pd.read_csv("data/fuel_prices_2024.csv", sep=";", decimal=",")
    fuel_2025 = pd.read_csv("data/fuel_prices_2025.csv", sep=";", decimal=",")

    # fuel = pd.concat([fuel_2024, fuel_2025])
    fuel = fuel_2024
    fuel = fuel.loc[:, ["Stichtag", "Diesel", "Eurosuper", "Normal", "Super Plus"]]
    fuel = fuel.set_index("Stichtag")
    fuel.index = pd.to_datetime(fuel.index, dayfirst=True)
    fuel = fuel.tz_localize(TIME_ZONE)
    fuel = fuel.resample(FREQUENCY).mean()

    fuel = (fuel
            .reindex(st.session_state.time_index)
            .interpolate(method="linear"))

    return fuel


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

def setup_and_get_time_range_slider():
    time_range = st.slider(
        "Time range",
        min_value=MIN_TIME.to_pydatetime(),
        max_value=MAX_TIME.to_pydatetime(),
        value=(MIN_TIME.to_pydatetime(), MAX_TIME.to_pydatetime()),
        format=DATE_FORMAT,
    )

    st.session_state.time_range = [
        pd.Timestamp(time_range[0]).tz_convert(tz=TIME_ZONE),
        pd.Timestamp(time_range[1]).tz_convert(tz=TIME_ZONE),
    ]

    st.session_state.time_index = pd.date_range(
        start=st.session_state.time_range[0],
        end=st.session_state.time_range[1],
        freq=FREQUENCY,
    )


if __name__ == "__main__":
    main()
