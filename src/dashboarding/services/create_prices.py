import plotly.express as px
import streamlit as st

from dashboarding.models.Commodity import Commodity

def create_prices(
        all_prices,
        electricity_prices,
        fuel_prices):
    st.markdown("## Price comparison")

    fig = px.line(
        all_prices,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (EUR per MWh)",
        legend_title_text="Commodity",
        hovermode="closest",
        dragmode=False,
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_yaxes(autorange=True)
    
    st.plotly_chart(fig)
    
    st.markdown("## Electricity")
    fig = px.line(
        electricity_prices,
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (EUR per MWh)",
        hovermode="closest",
        dragmode=False,
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_yaxes(autorange=True)
    
    st.plotly_chart(fig)

    for commodity in Commodity:
        if commodity == Commodity.ELETRICITY:
            continue
        
        st.markdown(f"## {commodity}")
        commodity_prices = fuel_prices[commodity]
        fig = px.line(commodity_prices)
    
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (EUR per liter)",
            hovermode="closest",
            dragmode=False,
        )
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(autorange=True)

        st.plotly_chart(fig)
