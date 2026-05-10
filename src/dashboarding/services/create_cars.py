import pandas as pd
import streamlit as st
from dashboarding.models.CarColumns import CarColumns
from dashboarding.models.Commodity import Commodity

from dashboarding.models.TabNames import TabNames

def create_cars():
    need_default_cars = "cars" not in st.session_state
    if need_default_cars:
        st.session_state.cars = get_default_cars()

    st.markdown("## Car Management")
    updated_cars = st.data_editor(
        st.session_state.cars,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            CarColumns.NAME.value: st.column_config.TextColumn(
                label=CarColumns.NAME.value,
                required=True,
                default="Ford Ka",
            ),
            CarColumns.COMMODITY.value: st.column_config.SelectboxColumn(
                label=CarColumns.COMMODITY.value,
                options=[c for c in Commodity],
                required=True,
                default=Commodity.DIESEL,
            ),
            CarColumns.CONSUMPTION.value: st.column_config.NumberColumn(
                label=CarColumns.CONSUMPTION.value,
                min_value=0.0,
                step=0.1,
                help="kWh/100km for EV, l/100km for fuel cars",
                required=True,
                default=5.0,
            ),
        },
    )

    ## TODO: Trigger recalculations in trip planner if something changed here
    if need_default_cars or not updated_cars.equals(st.session_state.cars):
        st.session_state.cars = updated_cars
        st.rerun()

    if st.session_state.tabs_by_name[TabNames.CARS].open:
        with st.sidebar:
            st.markdown("Sidebar content for Car Management")


def get_default_cars():
    default_data =[
        {
            CarColumns.NAME.value: "Ford Ka",
            CarColumns.COMMODITY.value: Commodity.NORMAL,
            CarColumns.CONSUMPTION.value: 6.2,
        },
        {
            CarColumns.NAME.value: "Volkswagen Golf",
            CarColumns.COMMODITY.value: Commodity.DIESEL,
            CarColumns.CONSUMPTION.value: 4.8,
        },
        {
            CarColumns.NAME.value: "BMW 3 Series",
            CarColumns.COMMODITY.value: Commodity.DIESEL,
            CarColumns.CONSUMPTION.value: 5.1,
        },
        {
            CarColumns.NAME.value: "Audi A4",
            CarColumns.COMMODITY.value: Commodity.DIESEL,
            CarColumns.CONSUMPTION.value: 5.4,
        },
        {
            CarColumns.NAME.value: "Mercedes A-Class",
            CarColumns.COMMODITY.value: Commodity.EUROSUPER,
            CarColumns.CONSUMPTION.value: 6.7,
        },
        {
            CarColumns.NAME.value: "Opel Corsa",
            CarColumns.COMMODITY.value: Commodity.NORMAL,
            CarColumns.CONSUMPTION.value: 5.9,
        },
        {
            CarColumns.NAME.value: "Peugeot 208",
            CarColumns.COMMODITY.value: Commodity.EUROSUPER,
            CarColumns.CONSUMPTION.value: 5.6,
        },
        {
            CarColumns.NAME.value: "Renault Clio",
            CarColumns.COMMODITY.value: Commodity.DIESEL,
            CarColumns.CONSUMPTION.value: 4.5,
        },
        {
            CarColumns.NAME.value: "Toyota Yaris",
            CarColumns.COMMODITY.value: Commodity.SUPER_PLUS,
            CarColumns.CONSUMPTION.value: 5.3,
        },
        {
            CarColumns.NAME.value: "Honda Civic",
            CarColumns.COMMODITY.value: Commodity.EUROSUPER,
            CarColumns.CONSUMPTION.value: 6.0,
        },
        {
            CarColumns.NAME.value: "Skoda Octavia",
            CarColumns.COMMODITY.value: Commodity.DIESEL,
            CarColumns.CONSUMPTION.value: 4.9,
        },
        {
            CarColumns.NAME.value: "Mazda 3",
            CarColumns.COMMODITY.value: Commodity.SUPER_PLUS,
            CarColumns.CONSUMPTION.value: 6.1,
        },
        {
            CarColumns.NAME.value: "Hyundai i30",
            CarColumns.COMMODITY.value: Commodity.NORMAL,
            CarColumns.CONSUMPTION.value: 5.8,
        },
        {
            CarColumns.NAME.value: "Kia Ceed",
            CarColumns.COMMODITY.value: Commodity.EUROSUPER,
            CarColumns.CONSUMPTION.value: 5.7,
        },
        {
            CarColumns.NAME.value: "Fiat Panda",
            CarColumns.COMMODITY.value: Commodity.NORMAL,
            CarColumns.CONSUMPTION.value: 5.2,
        },
        {
            CarColumns.NAME.value: "Tesla Model 3",
            CarColumns.COMMODITY.value: Commodity.ELETRICITY,
            CarColumns.CONSUMPTION.value: 15.5,
        },
        {
            CarColumns.NAME.value: "Tesla Model Y",
            CarColumns.COMMODITY.value: Commodity.ELETRICITY,
            CarColumns.CONSUMPTION.value: 16.8,
        },
        {
            CarColumns.NAME.value: "Nissan Leaf",
            CarColumns.COMMODITY.value: Commodity.ELETRICITY,
            CarColumns.CONSUMPTION.value: 17.2,
        },
        {
            CarColumns.NAME.value: "Renault Zoe",
            CarColumns.COMMODITY.value: Commodity.ELETRICITY,
            CarColumns.CONSUMPTION.value: 14.9,
        },
        {
            CarColumns.NAME.value: "BMW i3",
            CarColumns.COMMODITY.value: Commodity.ELETRICITY,
            CarColumns.CONSUMPTION.value: 15.8,
        },
    ]

    default_cars = pd.DataFrame(default_data)
    default_cars.columns = default_cars.columns.astype(str)
    return default_cars