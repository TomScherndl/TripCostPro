from dashboarding.models.CarColumns import CarColumns
from dashboarding.models.Commodity import Commodity
from dashboarding.models.Globals import FUEL_KWH_PER_L, TIME_ZONE


import plotly.express as px
import streamlit as st


from datetime import timedelta
from zoneinfo import ZoneInfo

def create_trip_calculator(all_prices):
    st.markdown("## Savings calculator")

    st.markdown("### Trip information")
    trip_date = st.datetime_input(
        label="Trip date",
        min_value=all_prices.index[0],
        max_value=all_prices.index[-1],
        value=all_prices.index[0],
        step=timedelta(hours=1),
    )
    assert trip_date is not None

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