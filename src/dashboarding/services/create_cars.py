import pandas as pd
import streamlit as st
from dashboarding.models.CarColumns import CarColumns
from dashboarding.models.Commodity import Commodity

def create_cars():
    if "cars" not in st.session_state:
        st.session_state.cars = pd.DataFrame(get_default_cars())

    st.markdown("## Car Management")
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
            CarColumns.CONSUMPTION: st.column_config.NumberColumn(
                label=CarColumns.CONSUMPTION,
                min_value=0.0,
                step=0.1,
                help="kWh/100km for EV, l/100km for fuel cars",
                required=True,
                default=5.0,
            ),
        },
    )
    
    ## TODO: Trigger recalculations in trip planner if something changed here
    # updated_cars = updated_cars.apply(
    #     lambda row: calculate_outputs(
    #         row,
    #         commodity_prices_at_trip_date,
    #         trip_distance_km,
    #         trip_budget_eur,
    #     ),
    #     axis=1,
    # )
# 
    # if not updated_cars.equals(st.session_state.cars):
    #     st.session_state.cars = updated_cars
    #     st.rerun()


def get_default_cars():
    return [
    {CarColumns.NAME: "Ford Ka", CarColumns.COMMODITY: Commodity.NORMAL, CarColumns.CONSUMPTION: 6.2},
    {CarColumns.NAME: "Volkswagen Golf", CarColumns.COMMODITY: Commodity.DIESEL, CarColumns.CONSUMPTION: 4.8},
    {CarColumns.NAME: "BMW 3 Series", CarColumns.COMMODITY: Commodity.DIESEL, CarColumns.CONSUMPTION: 5.1},
    {CarColumns.NAME: "Audi A4", CarColumns.COMMODITY: Commodity.DIESEL, CarColumns.CONSUMPTION: 5.4},
    {CarColumns.NAME: "Mercedes A-Class", CarColumns.COMMODITY: Commodity.EUROSUPER, CarColumns.CONSUMPTION: 6.7},
    {CarColumns.NAME: "Opel Corsa", CarColumns.COMMODITY: Commodity.NORMAL, CarColumns.CONSUMPTION: 5.9},
    {CarColumns.NAME: "Peugeot 208", CarColumns.COMMODITY: Commodity.EUROSUPER, CarColumns.CONSUMPTION: 5.6},
    {CarColumns.NAME: "Renault Clio", CarColumns.COMMODITY: Commodity.DIESEL, CarColumns.CONSUMPTION: 4.5},
    {CarColumns.NAME: "Toyota Yaris", CarColumns.COMMODITY: Commodity.SUPER_PLUS, CarColumns.CONSUMPTION: 5.3},
    {CarColumns.NAME: "Honda Civic", CarColumns.COMMODITY: Commodity.EUROSUPER, CarColumns.CONSUMPTION: 6.0},
    {CarColumns.NAME: "Skoda Octavia", CarColumns.COMMODITY: Commodity.DIESEL, CarColumns.CONSUMPTION: 4.9},
    {CarColumns.NAME: "Mazda 3", CarColumns.COMMODITY: Commodity.SUPER_PLUS, CarColumns.CONSUMPTION: 6.1},
    {CarColumns.NAME: "Hyundai i30", CarColumns.COMMODITY: Commodity.NORMAL, CarColumns.CONSUMPTION: 5.8},
    {CarColumns.NAME: "Kia Ceed", CarColumns.COMMODITY: Commodity.EUROSUPER, CarColumns.CONSUMPTION: 5.7},
    {CarColumns.NAME: "Fiat Panda", CarColumns.COMMODITY: Commodity.NORMAL, CarColumns.CONSUMPTION: 5.2},
    {CarColumns.NAME: "Tesla Model 3", CarColumns.COMMODITY: Commodity.ELETRICITY, CarColumns.CONSUMPTION: 15.5},
    {CarColumns.NAME: "Tesla Model Y", CarColumns.COMMODITY: Commodity.ELETRICITY, CarColumns.CONSUMPTION: 16.8},
    {CarColumns.NAME: "Nissan Leaf", CarColumns.COMMODITY: Commodity.ELETRICITY, CarColumns.CONSUMPTION: 17.2},
    {CarColumns.NAME: "Renault Zoe", CarColumns.COMMODITY: Commodity.ELETRICITY, CarColumns.CONSUMPTION: 14.9},
    {CarColumns.NAME: "BMW i3", CarColumns.COMMODITY: Commodity.ELETRICITY, CarColumns.CONSUMPTION: 15.8},
]