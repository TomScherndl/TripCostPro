from datetime import timedelta, datetime, date
from zoneinfo import ZoneInfo

import streamlit as st
import pandas as pd

from dashboarding.models.Commodity import Commodity
from dashboarding.models.Globals import TIME_ZONE
from dashboarding.models.TabNames import TabNames

import time


def create_overview(
    all_prices,
    electricity_prices,
    fuel_prices,
):
    today = pd.Timestamp(datetime.now(ZoneInfo(TIME_ZONE)))

    overview_date = st.date_input(
        label="Overview date",
        min_value=all_prices.index[0],
        max_value=all_prices.index[-1],
        value=today,
    )
    assert overview_date is not None
    overview_date = pd.Timestamp(overview_date).replace(
        tzinfo=ZoneInfo(TIME_ZONE) if today is today else None,
        hour=0,
        minute=0,
        second=0,
        microsecond=0)


    st.markdown(f"## Commodity prices on {overview_date.strftime('%Y-%m-%d')}")

    value = electricity_prices.loc[overview_date].iloc[0]
    delta = value - electricity_prices.loc[overview_date - timedelta(days=1)].iloc[0]
    st.metric(
        label=Commodity.ELETRICITY.value,
        value=value,
        delta=delta,
        format="euro"
    )

    for commodity in Commodity:
        if commodity == Commodity.ELETRICITY:
            continue
        
        value = fuel_prices.loc[overview_date,commodity]
        delta = value - fuel_prices.loc[overview_date - timedelta(days=1),commodity]
        st.metric(
            label=commodity.value,
            value=value,
            delta=delta,
            format="euro"
        )

    if st.session_state.tabs_by_name[TabNames.OVERVIEW].open:
        with st.sidebar:
            st.markdown("Sidebar content for Overview")
