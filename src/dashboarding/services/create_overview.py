from datetime import timedelta, datetime, date
from zoneinfo import ZoneInfo

import streamlit as st
import pandas as pd

from dashboarding.models.Commodity import Commodity
from dashboarding.models.Globals import TIME_ZONE
from dashboarding.models.SideBarContent import OVERVIEW_SIDEBAR_CONTENT
from dashboarding.models.TabNames import TabNames

st.set_page_config(layout="wide")

# handling of external css
with open('./dashboard.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def create_overview(
    all_prices,
    electricity_prices,
    fuel_prices,
):
    st.markdown(f"""
    Thinking about taking a trip and want to choose the cheapest option from our car fleet?   
    Use the **Date Picker** to select a specific date and get an instant snapshot of commodity prices on that day and their change from the day before.
    
    **Note**: We assume that you will be using **our on-site loading facilities for electric cars**, so the cost of electricity is based on the energy market price, not company-specific load prices. 
    """)
    today = pd.Timestamp(datetime.now(ZoneInfo(TIME_ZONE)))
    chosen_date = st.session_state.get("overview_date") if st.session_state.get("overview_date") else today
    overview_date = st.date_input(
        label="Overview date",
        min_value=all_prices.index[0],
        max_value=all_prices.index[-1],
        value=chosen_date,
    )
    assert overview_date is not None
    overview_date = pd.Timestamp(overview_date).replace(
        tzinfo=ZoneInfo(TIME_ZONE) if today is today else None,
        hour=0,
        minute=0,
        second=0,
        microsecond=0)

    st.session_state.overview_date = overview_date

    st.markdown(f"## Commodity prices on {overview_date.strftime('%Y-%m-%d')}")
    # check if overview date is in the future - if yes, add a warning that prices are based on predictions and not actual prices
    if overview_date > today:
        st.warning("The selected date is in the future. The displayed prices are based on predictions and may not reflect actual market conditions.")


    col1, col2 = st.columns(2)
    

    value = electricity_prices.loc[overview_date].iloc[0]
    delta = value - electricity_prices.loc[overview_date - timedelta(days=1)].iloc[0]
    st.metric(
        label=f"{Commodity.ELETRICITY.value}",
        value=get_formatted(value),
        delta=get_formatted(delta),
        border=True,
    )

    for commodity in Commodity:
        if commodity == Commodity.ELETRICITY:
            continue
        
        col = col1 if commodity in [Commodity.DIESEL, Commodity.NORMAL] else col2
        with col: 
            value = fuel_prices.loc[overview_date,commodity]
            delta = value - fuel_prices.loc[overview_date - timedelta(days=1),commodity]
            st.metric(f"{commodity.value}",get_formatted(value,False), delta=get_formatted(delta,False), 
                      border=True)
            
    if st.session_state.tabs_by_name[TabNames.OVERVIEW].open:
        with st.sidebar:
            st.markdown(OVERVIEW_SIDEBAR_CONTENT)
    st.markdown("**Source:** *[ENTSOE Transparency Database](https://transparency.entsoe.eu/) for electricity prices, and [Austrian Federal Ministry Economy, Energy and Tourism](https://www.bmwet.gv.at/Themen/Energie/kosten.html) for fuel prices.*")

def get_formatted(value,is_electric=True):
    per_unit = "kWh" if is_electric else "liter"
    return f"{value:.4f} EUR / {per_unit}"