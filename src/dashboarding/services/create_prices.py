import plotly.express as px
import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

from dashboarding.models.Globals import TIME_ZONE
 
from dashboarding.models.SideBarContent import PRICES_SIDEBAR_CONTENT
from dashboarding.models.TabNames import TabNames
from dashboarding.models.Commodity import Commodity

ANNOT_TODAY = f"Today: afterwards predicted values!"
if "layout_preference" not in st.session_state:
    st.session_state["layout_preference"] = "wide"
st.set_page_config(page_title="TripCostPro", layout=st.session_state["layout_preference"])

def create_prices(
        all_prices,
        electricity_prices,
        fuel_prices):
    st.markdown("""## Price Comparison of Commodities
The line charts below allow you to visualize trends in electricity and fuel prices. All prices are transformed to **EUR/kWh** for a consistent comparison.
* Change the slider below the graph to **limit the time range**.
* **Hover over the lines** to see exact price values on specific dates. 
* Use the **legend to toggle the visibility of commodities** for a clearer view.
""")
    today = pd.Timestamp(datetime.now(ZoneInfo(TIME_ZONE)))

    fig = px.line(
        all_prices,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="EUR / kWh",
        legend_title_text="Commodity",
        hovermode="closest",
        dragmode=False,
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_yaxes(autorange=True)
    fig.add_vline(x=today.timestamp()*1000, line_width=3, line_color="red", line_dash="dash", 
                  annotation_text=ANNOT_TODAY, annotation_position="top right")
    st.plotly_chart(fig)
    
        
    expander = st.expander("Show individual fuel prices")
    with expander: 

        st.markdown("## Electricity")
        fig = px.line(
            electricity_prices,
        )
        fig.add_vline(x=today.timestamp()*1000, line_width=3, line_color="red", line_dash="dash", 
                  annotation_text=ANNOT_TODAY, annotation_position="top right")
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="EUR / kwh",
            legend_title_text="Commodity",
            hovermode="closest",
            dragmode=False,
            showlegend=False,
        )
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(autorange=True)
        
        st.plotly_chart(fig)

        cols = st.columns(2)
        for commodity in Commodity:
            if commodity == Commodity.ELETRICITY:
                continue
            
            col = cols[0] if commodity in [Commodity.DIESEL, Commodity.NORMAL] else cols[1]
            with col: 
                st.markdown(f"## {commodity}")
                commodity_prices = fuel_prices[commodity]
                fig = px.line(commodity_prices)
                fig.add_vline(x=today.timestamp()*1000, line_width=3, line_color="red", line_dash="dash", 
                  annotation_text=ANNOT_TODAY, annotation_position="top right")
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="EUR / liter",
                    legend_title_text="Commodity",
                    hovermode="closest",
                    dragmode=False,
                    showlegend=False,
                )
                fig.update_xaxes(rangeslider_visible=True)
                fig.update_yaxes(autorange=True)

                st.plotly_chart(fig)

    if st.session_state.tabs_by_name[TabNames.PRICES].open:
        with st.sidebar:
            st.markdown(PRICES_SIDEBAR_CONTENT)
