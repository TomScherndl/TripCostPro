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
from streamlit import session_state as ss


# Declare and initialize the layout session variable.
if 'layout' not in ss:
	ss.layout = 'wide'

def create_trip_calculator(all_prices):
    st.markdown("## Trip planner")

    st.markdown("### Trip information")
    cols = st.columns(4)
    with cols[0]:    
        today = pd.Timestamp(datetime.now(ZoneInfo(TIME_ZONE)))
        # choose trip date - default to overview date if set, otherwise to today
        if overview_date := ss.get("overview_date"):
            current_date = overview_date
        else:
            current_date = today

        trip_date = st.date_input(
            label="Trip date",
            min_value=all_prices.index[0],
            max_value=all_prices.index[-1],
            value=current_date,
        )
        assert trip_date is not None
        
        trip_date = pd.Timestamp(trip_date).replace(
        tzinfo=ZoneInfo(TIME_ZONE) if today is today else None,
        hour=0,
        minute=0,
        second=0,
        microsecond=0)
        st.session_state.trip_date = trip_date
        
    with cols[1]:
        trip_distance_km = st.number_input(
            label="Trip distance (km)",
            min_value=1.0,
            value=300.0,
            )
    with cols[2]:
        trip_budget_eur = st.number_input(
            label="Trip budget (EUR)",
            min_value=1.0,
            value=5.0,
        )
    with cols[3]:
        num_cars = st.number_input(
            label="Number of cars to show in table",
            min_value=1,
            value=6,
        )
    st.markdown(
        """
        <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px;">
            <strong>Note:</strong> The trip planner calculates the estimated cost of a trip based on the selected trip date, distance, and budget. 
            It considers the current cars in our garage and their respective fuel or electricity consumption to determine the most cost-efficient option for your trip.
        </div>
        <br>
        """,
        unsafe_allow_html=True,
    )
    if trip_date > today:
        st.warning("The selected date is in the future. The displayed prices are based on predictions and may not reflect actual market conditions.")

    commodity_prices_at_trip_date = all_prices.loc[trip_date]
    expander_prices = st.expander(f"Show commodity prices at trip date")
    with expander_prices:
        fig = px.bar(commodity_prices_at_trip_date)
        fig.update_layout(
            xaxis_title=TripCalculatorColumns.COMMODITY,
            yaxis_title="Price (EUR/kWh)",
            title = f"Commodity Prices on {trip_date.strftime('%d.%m.%Y')}",
            showlegend=False, 
            hovermode="closest",
            dragmode=False,
        )
        st.plotly_chart(fig)
        
    create_trip_data(
        commodity_prices_at_trip_date,
        trip_distance_km,
        trip_budget_eur,
        num_cars
    )

    if st.session_state.tabs_by_name[TabNames.TRIP_PLANNER].open:
        with st.sidebar:
            st.markdown(TRIP_PLANNER_SIDEBAR_CONTENT)


def create_trip_data(
    commodity_prices_at_trip_date,
    trip_distance_km,
    trip_budget_eur,
    num_cars=10
):
    st.markdown("### Trip calculation")

    st.session_state.trip_planner_data = get_trip_data(
        commodity_prices_at_trip_date,
        trip_distance_km,
        trip_budget_eur,
    )

    st.markdown(f"#### Most efficient car for the trip on {st.session_state.trip_date.strftime('%d.%m.%Y')}")
    if st.session_state.trip_planner_data.empty:
        st.markdown("No cars available. Please add cars in the Cars tab to see trip calculations.")
    else:
        most_efficient_car = st.session_state.trip_planner_data.loc[
            st.session_state.trip_planner_data[TripCalculatorColumns.TRIP_COST.value].idxmin()
        ]
        cols = st.columns(3)
        with cols[0]:
            st.metric(label="Most efficient car", value=most_efficient_car[TripCalculatorColumns.NAME.value])
        with cols[1]:
            st.metric(label="Estimated trip cost",value=f"€ {most_efficient_car[TripCalculatorColumns.TRIP_COST.value]:.2f}")
        with cols[2]:
            st.metric(label="Is the trip within budget?",
                  value="✅ Yes" if most_efficient_car[TripCalculatorColumns.IN_BUDGET.value] else "❌ No")   
        st.markdown(f"#### Top {num_cars} cost by car")
    st.dataframe(data=st.session_state.trip_planner_data.reset_index(drop=True).sort_values(by=TripCalculatorColumns.TRIP_COST.value).head(num_cars),
                hide_index=True,)
    expander = st.expander("How is the trip cost calculated?")
    with expander:
        st.markdown(
            """
            The trip cost is calculated based on the following formula:

            **Trip Cost (EUR) = Cost per Wh (EUR/Wh) * Wh Consumption per km (Wh/km) * Trip Distance (km)**

            Where:
            - **Cost per Wh** is derived from the commodity price at the trip date, converted from EUR/MWh to EUR/Wh.
            - **Wh Consumption per km** is calculated based on the vehicle's consumption and the energy content of the fuel or electricity.
            - **Trip Distance** is the distance of the trip in kilometers.

            The resulting trip cost is then compared to the trip budget to determine if it is within budget.
            """
        )
    expander2 = st.expander("How to interpret the 'In budget' column?")
    with expander2:
        st.markdown(
            f"""
            The 'In budget' column indicates whether the calculated trip cost is within the specified trip budget (set at **{trip_budget_eur} EUR**). 
            
            - A **✅ Checkmark** means that the trip cost is less than or equal to the trip budget, indicating that the trip is budget-approved.
            - A **❌ Cross** means that the trip cost exceeds the trip budget, suggesting that you may want to consider a different vehicle or adjust your trip parameters to stay within your budget.
            """
        )
    expander_fulltable = st.expander("Show all cars trip data table")
    with expander_fulltable:
        st.dataframe(
            data=st.session_state.trip_planner_data.reset_index(drop=True).sort_values(by=TripCalculatorColumns.TRIP_COST.value),
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

    cost_eur_per_wh = commodity_prices_at_trip_date[commodity] / (1000)

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
