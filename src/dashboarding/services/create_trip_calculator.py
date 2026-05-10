from dashboarding.models.SideBarContent import TRIP_PLANNER_SIDEBAR_CONTENT
from dashboarding.models.TripCalculatorColumns import TripCalculatorColumns
from dashboarding.models.Commodity import Commodity
from dashboarding.models.Globals import FUEL_KWH_PER_L, TIME_ZONE
from dashboarding.models.TabNames import TabNames

from datetime import timedelta, datetime, date
import plotly.express as px
import streamlit as st
import pandas as pd

from zoneinfo import ZoneInfo


def create_trip_calculator(all_prices):
    st.markdown("## Savings calculator")

    st.markdown("### Trip information")
    today = pd.Timestamp(datetime.now(ZoneInfo(TIME_ZONE)))
    trip_date = st.date_input(
        label="Trip date",
        min_value=all_prices.index[0],
        max_value=all_prices.index[-1],
        value=today,
    )
    assert trip_date is not None

    trip_date = pd.Timestamp(trip_date).replace(
    tzinfo=ZoneInfo(TIME_ZONE) if today is today else None,
    hour=0,
    minute=0,
    second=0,
    microsecond=0)
    trip_distance_km = st.number_input(
        label="Trip distance (km)",
        min_value=1,
        value=100,
    )

    trip_budget_eur = st.number_input(
        label="Trip budget (EUR)",
        min_value=1,
        value=5,
    )

    commodity_prices_at_trip_date = all_prices.loc[trip_date]
    fig = px.bar(commodity_prices_at_trip_date)
    fig.update_layout(
        xaxis_title=TripCalculatorColumns.COMMODITY,
        yaxis_title="Price (EUR/MWh)",
        legend_title_text="Trip time",
        hovermode="closest",
        dragmode=False,
    )
    st.plotly_chart(fig)
    
    create_trip_data(
        commodity_prices_at_trip_date,
        trip_distance_km,
        trip_budget_eur,
    )

    if st.session_state.tabs_by_name[TabNames.TRIP_PLANNER].open:
        with st.sidebar:
            st.markdown(TRIP_PLANNER_SIDEBAR_CONTENT)


def create_trip_data(
    commodity_prices_at_trip_date,
    trip_distance_km,
    trip_budget_eur,
):
    st.markdown("### Trip calculation")

    st.session_state.trip_planner_data = get_trip_data(
        commodity_prices_at_trip_date,
        trip_distance_km,
        trip_budget_eur,
    )

    st.dataframe(
        data=st.session_state.trip_planner_data,
        hide_index=True,
        column_config={
            TripCalculatorColumns.NAME.value: st.column_config.TextColumn(
                label=TripCalculatorColumns.NAME.value,
            ),
            TripCalculatorColumns.COMMODITY.value: st.column_config.TextColumn(
                label=TripCalculatorColumns.COMMODITY.value,
            ),
            TripCalculatorColumns.CONSUMPTION.value: st.column_config.NumberColumn(
                label=TripCalculatorColumns.CONSUMPTION.value,
            ),
            TripCalculatorColumns.TRIP_COST.value: st.column_config.NumberColumn(
                label=TripCalculatorColumns.TRIP_COST.value,
                format="€ %.2f",
            ),
            TripCalculatorColumns.IN_BUDGET.value: st.column_config.CheckboxColumn(
                label=TripCalculatorColumns.IN_BUDGET.value,
                default=False,
            ),
        },
    )



def get_trip_data(
    commodity_prices_at_trip_date,
    trip_distance_km,
    trip_budget_eur,
):
    if "cars" in st.session_state:
        df = st.session_state.cars.copy()
        df[TripCalculatorColumns.TRIP_COST.value] = 0.0
        df[TripCalculatorColumns.IN_BUDGET.value] = False
    else:
        df = pd.DataFrame(columns=[t.value for t in TripCalculatorColumns])

    df = df.apply(
        lambda row: calculate_trip_data_rowwise(
            row,
            commodity_prices_at_trip_date,
            trip_distance_km,
            trip_budget_eur,
        ),
        axis=1,
    )

    return df


def calculate_trip_data_rowwise(
    row,
    commodity_prices_at_trip_date,
    trip_distance_km,
    trip_budget_eur,
):
    commodity = row[TripCalculatorColumns.COMMODITY.value]

    cost_eur_per_wh = commodity_prices_at_trip_date[commodity] / (1000 * 1000)

    if commodity == Commodity.ELETRICITY.value:
        wh_consumption_per_km = 1000 * row[TripCalculatorColumns.CONSUMPTION.value] / (100)
    else:
        l_consumption_per_km = row[TripCalculatorColumns.CONSUMPTION.value] / 100
        fuel_wh_per_l = FUEL_KWH_PER_L[commodity] * 1000
        wh_consumption_per_km = l_consumption_per_km * fuel_wh_per_l

    trip_price_eur = cost_eur_per_wh * wh_consumption_per_km * trip_distance_km
    is_trip_in_budget = trip_price_eur <= trip_budget_eur

    row[TripCalculatorColumns.TRIP_COST.value] = trip_price_eur
    row[TripCalculatorColumns.IN_BUDGET.value] = is_trip_in_budget

    return row
